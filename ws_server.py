import asyncio
import websockets
import cv2
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get server parameters from environment variables
SERVER_WIDTH = int(os.getenv("SERVER_WIDTH", 40))
SERVER_HEIGHT = int(os.getenv("SERVER_HEIGHT", 30))
SERVER_JPG_COMPRESSION = float(os.getenv("SERVER_JPG_COMPRESSION", 0.5))
HOST = os.getenv("HOST", "localhost")
WS_PORT = int(os.getenv("WS_PORT", 6969))

print(f"Server width: {SERVER_WIDTH}")
print(f"Server height: {SERVER_HEIGHT}")
print(f"Server JPG compression: {SERVER_JPG_COMPRESSION}")


async def process_image(websocket, path):
  async for message in websocket:
    # Decode the message to a numpy array
    nparr = np.frombuffer(message, np.uint8)
    # Decode the image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize
    img = cv2.resize(img, (SERVER_WIDTH, SERVER_HEIGHT))

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Encode the grayscale image to send back with compression
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),
                    int(SERVER_JPG_COMPRESSION * 100)]
    _, buffer = cv2.imencode('.jpg', gray_img, encode_param)
    await websocket.send(buffer.tobytes())


async def main():
  async with websockets.serve(process_image, HOST, WS_PORT):
    await asyncio.Future()  # run forever

if __name__ == "__main__":
  asyncio.run(main())
