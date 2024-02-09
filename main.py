import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

import price

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def root():
  return FileResponse("./static/price.html")


@app.get("/data", response_class=HTMLResponse)
async def get_data(request: Request):
  # Fetch your data
  price1 = str(price.get_price())
  height = str(price.get_blockheight())
  halving = 840000 - price.get_blockheight()

  # Render it using a template
  return templates.TemplateResponse("data.html", {
      "request": request,
      "price1": price1,
      "height": height,
      "halving": halving
  })


@app.get("/price")
async def price_str():
  usd = str(price.get_price())
  return HTMLResponse(f'<h1 class="price">{usd}$</h1>')


@app.get("/height")
async def height():
  height = price.get_blockheight()
  return HTMLResponse(f'<h2 class="price">{height} Blocks</h1>')


@app.get("/halving")
async def halving():
  height = price.get_blockheight()
  return HTMLResponse(
      f'<p id="halving" hx-swap-oob="true"> next halving in {840000 - height} blocks</p>'
  )


uvicorn.run(app, host="0.0.0.0", port="8080")
