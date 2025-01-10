import hashlib
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()
urls: dict[str, str] = {}


class ToShort(BaseModel):
    url: str


class Shorted(BaseModel):
    url: str
    key: str


schema: dict[int | str, dict[str, Any]] | None = {
    307: {
        'description': 'Successful Response',
        'content': {
            'application/json': {
                'schema': {'title': 'Response Redirect To Url Go  Key  Get'}
            }
        }
    }
}


def _hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:8]


@app.post("/shorten", status_code=201)
def short_url(link: ToShort) -> Shorted:
    key: str = _hash(link.url)
    urls[key] = link.url
    return Shorted(url=link.url, key=key)


@app.get('/go/{key}', responses=schema, status_code=307)
def redirect_to_url(key: str) -> RedirectResponse:
    if key not in urls.keys():
        raise HTTPException(status_code=404, detail='Key not found')

    return RedirectResponse(url=urls[key])
