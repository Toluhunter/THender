from urllib.parse import parse_qs

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async


Account = get_user_model()


@database_sync_to_async
def get_user(token):

    user = AnonymousUser()

    try:
        access = AccessToken(token=token)
        user_id = access.get("user_id")

        account = Account.objects.filter(id=user_id)

        if account.exists():
            user = account.first()
    except:
        pass

    return user


class JWTAuthMiddleWare:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, recieve, send):

        qs = parse_qs(scope["query_string"].decode())
        token = qs["token"][0]
        user = await get_user(token)

        scope["user"] = user

        return await self.app(scope, recieve, send)
