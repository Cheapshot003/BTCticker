import asyncio

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse

import price

app = FastAPI()

connections = []


# Function to send a message to all connected WebSocket clients
async def broadcast(message: str):
  for connection in connections:
    await connection.send_text(message)


# WebSocket route for clients to connect to
@app.websocket("/data")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  current_price = price.get_price()
  current_height = price.get_blockheight()
  connections.append(websocket)
  message = f'<h1 id="price" hx-swap-oob="true" class="price">{current_price}$</h1> <h1 id="height" hx-swap-oob="true" class="price">{current_height} Blocks</h1> <p id="halving" hx-swap-oob="true" class="halving1"> next halving in {840000 - current_height} blocks</p>'
  await websocket.send_text(message)
  try:
    while True:
      # Keep the connection open
      await websocket.receive_text()
  except WebSocketDisconnect:
    connections.remove(websocket)


# Background task to check for price and block height changes
async def check_for_changes():
  last_price = None
  last_height = None
  while True:
    current_price = price.get_price()
    current_height = price.get_blockheight()
    if current_price != last_price or current_height != last_height:
      last_price = current_price
      last_height = current_height
      message = f'<h1 id="price" hx-swap-oob="true" class="price">{current_price}$</h1> <h1 id="height" hx-swap-oob="true" class="price">{current_height} Blocks</h1> <p id="halving" hx-swap-oob="true"> next halving in {840000 - current_height} blocks</p>'
      await broadcast(message)
    await asyncio.sleep(0.5)  # Check every 10 seconds


@app.on_event("startup")
async def startup_event():
  asyncio.create_task(check_for_changes())


@app.get('/')
async def root():
  return FileResponse("./static/price.html")


@app.get("/price")
async def price_str():
  usd = str(price.get_price())
  print(usd)
  return HTMLResponse(f'<h1 class="price">{usd}$</h1>')


@app.get("/height")
async def height():
  height = price.get_blockheight()
  return HTMLResponse(f'<h2 class="price">{height} Blocks</h1>')


uvicorn.run(app, host="0.0.0.0", port="8080")
