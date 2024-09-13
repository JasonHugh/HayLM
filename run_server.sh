#！/bin/bash
uvicorn server:app --ssl-certfile '/root/learning/FunASR/runtime/html5/ssl_key/server.crt' --ssl-keyfile '/root/learning/FunASR/runtime/html5/ssl_key/server.key'