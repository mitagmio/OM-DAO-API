from fastapi import HTTPException, status

from app.services import FrameworkAdapter


class FastapiAdapter(FrameworkAdapter):
    @staticmethod
    def http_exception_400(detail):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    @staticmethod
    def http_exception_200(detail):
        return HTTPException(status_code=status.HTTP_200_OK, detail=detail)
