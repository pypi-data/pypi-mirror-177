from typing import Optional, Dict, List

from pydantic import BaseModel

from avikus_response.model import StandardResponse


class Response:
    @staticmethod
    def _make_response(
        code: int,
        message: str,
        result: Optional[Dict] = None,
        detail: Optional[str] = None,
    ):
        if result and not isinstance(result, (BaseModel, Dict)):
            raise TypeError(f'result should be one of the type (BaseModel, Dict) not {type(result)}')

        if detail and not isinstance(detail, (str)):
            raise TypeError(f'detail should be str type not {type(detail)}')


        return dict(StandardResponse(
            code=code, message=message, result=result, detail=detail
        ))

    @classmethod
    def ok(cls, message: str, result: Optional[Dict] = None):
        return cls._make_response(code=200, message=message, result=result), 200

    @classmethod
    def create_success(cls, message: str, result: Optional[Dict] = None):
        return cls._make_response(code=201, message=message, result=result), 201

    @classmethod
    def update_success(cls, message: str, result: Optional[Dict] = None):
        return cls._make_response(code=204, message=message, result=result), 204

    @classmethod
    def bad_request(cls, message: str, detail: Optional[str] = None):
        return cls._make_response(code=400, message=message, detail=detail), 400

    @classmethod
    def unauthenticated(cls, message: str, detail: Optional[str] = None):
        return cls._make_response(code=401, message=message, detail=detail), 401

    @classmethod
    def forbidden(cls, message: str, detail: Optional[str] = None):
        return cls._make_response(code=403, message=message, detail=detail), 403

    @classmethod
    def not_found(cls, message: str, detail: Optional[str] = None):
        return cls._make_response(code=404, message=message, detail=detail), 404

    @classmethod
    def conflict(cls, message: str, detail: Optional[str] = None):
        return cls._make_response(code=409, message=message, detail=detail), 409

    @classmethod
    def server_error(cls, message: str, detail: Optional[str] = None):
        return cls._make_response(code=500, message=message, detail=detail), 500

    @classmethod
    def custom_success(cls, code: int, message: str, result: Optional[Dict] = None):
        return cls._make_response(code=code, message=message, result=result), code

    @classmethod
    def custom_error(
        cls,
        code: int,
        message: str,
        result: Optional[Dict] = None,
        detail: Optional[str] = None,
    ):
        return (
            cls._make_response(
                code=code, message=message, result=result, detail=detail
            ),
            code,
        )
