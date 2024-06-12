from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import asyncio
import threading
import websockets
from pynput import mouse
import configparser
import cv2
import sqlite3

config = configparser.ConfigParser()
config.read('config.ini')

for i in range(10):
    cap = cv2.VideoCapture(i)
    if not cap.isOpened():
        break
    print(f"Camera {i}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

    cap.release()

print("")
cam_port = input("Camera dev port: ")
cam = cv2.VideoCapture(int(cam_port))
pos = (0, 0)


def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS images
                    (id INTEGER PRIMARY KEY, image_data BLOB, x INTEGER, y INTEGER)''')
    conn.commit()
    conn.close()


def on_move(x, y):
    global pos
    pos = (x, y)


def on_click(x, y, button, pressed):
    global pos
    if button != mouse.Button.left or pressed:
        return

    ret, frame = cam.read()
    if not ret:
        return

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    _, buffer = cv2.imencode('.png', frame)
    blob_data = sqlite3.Binary(buffer)

    cursor.execute("INSERT INTO images (image_data, x, y) VALUES (?, ?, ?)", (blob_data, pos[0], pos[1]))
    conn.commit()
    conn.close()
    print("Saved image")


async def socket_handler(websocket):
    print("Client connected to socket")
    while True:
        await asyncio.sleep(0.2)
        await websocket.send(f"{pos[0]}, {pos[1]}")


async def socket():
    async with websockets.serve(socket_handler, config['WebSocket']['Host'], int(config['WebSocket']['Port'])):
        print(F"Running websocket on {config['WebSocket']['Host']}:{config['WebSocket']['Port']}")
        await asyncio.Future()


async def http_server():
    # pass
    server = ThreadingHTTPServer((config['HttpServer']['Host'], int(config['HttpServer']['Port'])),
                                 SimpleHTTPRequestHandler)
    print(F"Running server on {config['HttpServer']['Host']}:{config['HttpServer']['Host']}")
    server.serve_forever()


def start_web_server_in_thread():
    asyncio.run(http_server())


async def main():
    init_db()

    listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click)
    listener.start()
    web_server = threading.Thread(target=start_web_server_in_thread)
    web_server.start()
    await socket()


if __name__ == '__main__':
    asyncio.run(main())
