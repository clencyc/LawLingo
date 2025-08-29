from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, game, content, social, progress

app = FastAPI(title="Constitution Learning Game API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/user", tags=["User Management"])
app.include_router(game.router, prefix="/game", tags=["Game Core"])
app.include_router(content.router, prefix="/content", tags=["Content & Learning"])
app.include_router(social.router, prefix="/social", tags=["Social & Competition"])
app.include_router(progress.router, prefix="/progress", tags=["Progress & Analytics"])

@app.get("/")
async def root():
    return {"message": "Constitution Learning Game API"}