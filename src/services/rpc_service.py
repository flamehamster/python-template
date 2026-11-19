from fastapi import Response


class RpcService:
    @staticmethod
    async def example():
        return Response(status_code=204)
