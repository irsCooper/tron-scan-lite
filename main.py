from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.tron.router import router as router_blockchain


app = FastAPI(
    title="Tron Address Info Service", 
    docs_url='/ui-swagger',
)

app.include_router(router_blockchain)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8081, reload=True)