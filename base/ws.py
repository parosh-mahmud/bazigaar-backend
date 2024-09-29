
backend_token="serverUIO99GGRE46BCQOPQZIOPQ"

import environ

try:
    env = environ.Env()
    environ.Env.read_env(".env")
    ws_url=env("ws_url")
except:
    ws_url="ws://47.128.84.54:8090/ws/"

from websocket import create_connection

def wsMessageToUser(userid,message):
    try:
        ws = create_connection(f"{ws_url}listen/{userid}/{backend_token}/")
        # print(ws.recv())
        # print(f"Sending '{message}'...")
        ws.send(message)
        # print("Sent")
        # print("Receiving...")
        # result =  ws.recv()
        # print("Received '%s'" % result)
        ws.close()
    except Exception as e:
        print(e)
