from fastapi import HTTPException, status


def login_error():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )


def bad_token():
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='Bad authorization token',
    )


def token_expired():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Auth token is expired',
        headers={'WWW-Authenticate': 'Bearer'},
    )


def user_not_found():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='User is not found',
    )


def access_denied():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Access denied',
    )


def user_already_exists():
    return HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail='User already exists',
    )


def post_not_found():
    return HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail='Post is not found',
    )
