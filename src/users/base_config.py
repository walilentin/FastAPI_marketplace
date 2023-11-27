from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi import Depends, HTTPException
from src.config import SECRET_AUTH
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


GUEST_ROLE = "GUEST"
SELLER_ROLE = "SELLER"
BUYER_ROLE = "BUYER"
ADMIN_ROLE = "ADMIN"

# Define permissions for each role
ROLES_PERMISSIONS = {
    GUEST_ROLE: ["get_reviews", "view_site"],
    SELLER_ROLE: ["create_product", "delete_product"],
    BUYER_ROLE: ["buy_product", "add_review", "get_reviews"],
    ADMIN_ROLE: ["manage_users", "manage_roles", "manage_products"],
}

# Custom Authentication Backend
class RBACAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, credentials):
        user = await super().authenticate(credentials)
        if user is not None:
            user.role_permissions = ROLES_PERMISSIONS.get(user.role.name, [])
        return user


def current_user_has_permission(permission: str = Depends()):
    async def _current_user_has_permission(user: User = Depends(current_user)):
        if permission not in user.role.role_permissions:
            raise HTTPException(status_code=403, detail="User does not have the required permission")
        return user

    return _current_user_has_permission