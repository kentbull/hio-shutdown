import logging

import falcon
from hio.base import doing
from hio.core import http, tcp
from hio.help import decking

logger = logging.getLogger("hio_shutdown")

class HealthEnd:
    def __init__(self, signal_queue):
        self.signal_queue: decking.Deck = signal_queue

    def on_get(self, req, resp):
        shutdown = req.get_param("shutdown")
        if shutdown:
            logger.info("Shutdown requested")
            resp.status = falcon.HTTP_200
            resp.media = {'status': 'ok', 'shutdown': True}
            self.signal_queue.push(True)
        else:
            logger.info("Health check requested")
            resp.status = falcon.HTTP_200
            resp.media = {'status': 'ok'}

def create_http_server(port, app, keypath=None, certpath=None, cafilepath=None):
    """
    Create an HTTP or HTTPS server depending on whether TLS key material is present

    Parameters:
        port (int)         : port to listen on for all HTTP(s) server instances
        app (falcon.App)   : application instance to pass to the http.Server instance
        keypath (string)   : the file path to the TLS private key
        certpath (string)  : the file path to the TLS signed certificate (public key)
        cafilepath (string): the file path to the TLS CA certificate chain file
    Returns:
        hio.core.http.Server
    """
    if keypath is not None and certpath is not None and cafilepath is not None:
        servant = tcp.ServerTls(certify=False,
                                keypath=keypath,
                                certpath=certpath,
                                cafilepath=cafilepath,
                                port=port)
        server = http.Server(port=port, app=app, servant=servant)
    else:
        server = http.Server(port=port, app=app)
    return server


def run_server():
    port=8080
    signal_queue = decking.Deck()
    app = falcon.App()
    app.add_route('/health', HealthEnd(signal_queue))

    server = create_http_server(port, app)

    # server_doer = http.ServerDoer(server)
    server_doer = MyServerDoer(server, signal_queue)

    logger.info(f"Starting server on port {port}")
    doist = doing.Doist(limit=0.0, tock=0.03125, doers=[server_doer], real=True)
    doist.do()


class MyServerDoer(http.ServerDoer):
    def __init__(self, server, signal_queue, **kwa):
        super(MyServerDoer, self).__init__(server, **kwa)
        self.signal_queue = signal_queue

    def recur(self, tyme):
        if len(self.signal_queue) > 0:
            logger.info("Server received shutdown signal")
            raise GeneratorExit("Shutdown signal received")
        super(MyServerDoer, self).recur(tyme)

    def exit(self):
        logger.info("Server exiting")
        super(MyServerDoer, self).exit()

    def abort(self, ex):
        logger.error(f"Server aborting: {ex}")
        super(MyServerDoer, self).abort(ex)
