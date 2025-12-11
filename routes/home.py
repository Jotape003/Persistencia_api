from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["home"]
)

@router.get("/")
async def root():
    return {"message": "Bem vindo ao sistema de biblioteca!"}