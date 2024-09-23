#！/bin/bash
uvicorn server:app --ssl-certfile 'ssl_key/server.crt' --ssl-keyfile 'ssl_key/server.key' --host '0.0.0.0' --port 8000