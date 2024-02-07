from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import price

app = FastAPI()


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
