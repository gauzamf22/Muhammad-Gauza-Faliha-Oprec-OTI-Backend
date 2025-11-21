from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from src.api.routes import user, kantin, warung, menuitem, order, orderitem, authentication

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(kantin.router, prefix="/api", tags=["kantin"])
app.include_router(warung.router, prefix="/api", tags=["warung"])
app.include_router(menuitem.router, prefix="/api", tags=["menuitem"])
app.include_router(order.router, prefix="/api", tags=["order"])
app.include_router(orderitem.router, prefix="/api", tags=["orderitem"])
app.include_router(authentication.router, prefix="/api", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "vercel anjg, mending big cloud"}