from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
import websockets.exceptions


app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# WebSocket 엔드포인트
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()

    # 클라이언트 정보 저장
    client_info = {"id": client_id, "websocket": websocket}
    clients.append(client_info)

    try:
        while True:
            data = await websocket.receive_text()
            # 받은 메시지를 다른 클라이언트로 브로드캐스트
            await broadcast_message(data, client_id)
            await websocket.send_text(data)
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket 연결이 닫혔습니다.")
    except Exception as e:
        print(f"예외 발생: {e}")
    finally:
        if websocket.application_state == 'WebSocketState.CONNECTED':
            await websocket.close()

clients = []

# 메시지 브로드캐스트 함수
async def broadcast_message(message: str, sender_id: int):
    for client in clients:
        if client["id"] != sender_id:
            await client["websocket"].send_text(message)