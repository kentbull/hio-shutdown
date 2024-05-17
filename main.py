import logging.config

from hio_shutdown.core import run_server

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("hio_shutdown")

if __name__ == '__main__':
    run_server()
    logger.info("Server shutdown")
