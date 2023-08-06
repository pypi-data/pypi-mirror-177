import uuid
import requests
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import MutableHeaders


class K9FastapiMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if (request.headers.get('X-Correlation-ID') == None or
            request.headers.get('X-Correlation-ID') == ''):
            new_headers = MutableHeaders(request._headers)
            request._headers = new_headers
            request.headers['X-Correlation-ID'] = str(uuid.uuid4())
            request.scope.update(headers=request.headers.raw)
        
        requests.Session().headers.update({'X-Correlation-ID': request.headers.get('X-Correlation-ID')})
        response = await call_next(request)
        response.headers['X-Correlation-ID'] = request.headers.get('X-Correlation-ID') 
        return response