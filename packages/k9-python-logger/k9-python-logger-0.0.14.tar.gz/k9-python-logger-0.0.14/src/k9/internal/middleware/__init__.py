import uuid
import requests

from fastapi import Request
from main import app

@app.middleware("http")
async def add_correlation_id_header(request: Request, call_next):
    if (request.headers['X-Correlation-ID'] == None or
        request.headers['X-Correlation-ID'] == ''):
        request.headers['X-Correlation-ID'] = str(uuid.uuid4())
    requests.Session().headers.update({'X-Correlation-ID': request.headers['X-Correlation-ID']})
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = request.headers['X-Correlation-ID']
    return response