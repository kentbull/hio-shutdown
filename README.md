# HIO Shutdown

Run with `python main.py`

Then send a curl request to `/health?shutdown=true` to trigger a shutdown.

Example:
```bash 
curl "http://localhost:8080/health?shutdown=true"
```

Sample log output:
```text
2024-05-17 17:34:14,370 - hio_shutdown - INFO - Starting server on port 8080
2024-05-17 17:34:19,348 - hio_shutdown - INFO - Shutdown requested
2024-05-17 17:34:19,370 - hio_shutdown - INFO - Server received shutdown signal
2024-05-17 17:34:19,370 - hio_shutdown - INFO - Server exiting
2024-05-17 17:34:19,405 - hio_shutdown - INFO - Server shutdown
```