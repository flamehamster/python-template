from fastapi import APIRouter

from services.rpc_service import RpcService

router = APIRouter()


@router.post('/example')
async def example():
    return await RpcService.example()
