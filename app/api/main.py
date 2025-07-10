from fastapi import APIRouter

from app.api.routes.number import number_router
from app.api.routes.supervisor import supervisor_router
from app.api.routes.word import word_router
from app.api.routes.user import user_router
 

main_router = APIRouter()


main_router.include_router(supervisor_router, tags=["supervisor"])
main_router.include_router(number_router, tags=["number"])
main_router.include_router(word_router, tags=["word"])
main_router.include_router(user_router, tags=["user"])