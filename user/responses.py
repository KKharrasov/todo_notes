from typing import Tuple, Union, Callable
from enum import Enum
from fastapi import HTTPException
from pydantic import BaseModel


def with_errors(*errors: Tuple[Union[HTTPException, Callable[..., HTTPException]]]):
    d = {}
    for err in errors:
        if callable(err):
            err = err()
        d[err.status_code] = {'description': err.detail}
    return d


class ResultResponse(BaseModel):

    class status(str, Enum):
        ok = 'ok'

    result: status = status.ok
