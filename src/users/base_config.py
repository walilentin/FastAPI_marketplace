from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from src.config import SECRET_AUTH
from src.database import get_async_session
from src.users.manager import get_user_manager
from src.users.manager import User

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()
current_superuser = fastapi_users.current_user(active=True, superuser=True)


async def current_user_admin(user: User = Depends(current_user)):
    if user.role.name != 'ADMIN':
        raise HTTPException(status_code=401, detail="User is not a ADMIN")
    return user


async def current_user_seller(user: User = Depends(current_user)):
    if user.role.name != 'SELLER':
        raise HTTPException(status_code=401, detail="User is not a SELLER")
    return user


async def current_user_guest(user: User = Depends(current_user)):
    if user.role.name != 'GUEST':
        raise HTTPException(status_code=401, detail="User is not a GUEST")
    return user

async def current_user_buyer(user: User = Depends(current_user)):
    if user.role.name != 'BUYER':
        raise HTTPException(status_code=401, detail="User is not a BUYER")
    return user




