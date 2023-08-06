from rest_framework import authentication
from rest_framework.request import Request
from django.core.cache import cache
from requests import Response
from .models import TokenUser
import os, requests, jwt, hashlib

VERIFY_URL = os.environ['VERIFY_URL']
TOKEN_EXPIRE_TIME = int(os.environ['TOKEN_EXPIRE_TIME'])

HEADERS = {
    'Content-Type': 'application/json', 
}

class MyJWTAuthentication(authentication.BaseAuthentication):
    def _verify(self, token: str) -> Response:
        return requests.post(VERIFY_URL, headers=HEADERS, json={"token": token})

    def _decode_token(self, token: str):
        decode_token = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])
        if decode_token != None:
            user = TokenUser()
            user.from_json(decode_token['user'])
            return user, None
            
        return None, None

    def _sercure_key(self, token: str) -> int:
        return int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)

    def authenticate(self, request: Request):
        if  'HTTP_AUTHORIZATION' in request.META:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token[7:]

            secure_token = self._sercure_key(token)

            if cache.get(secure_token) != None:
                return self._decode_token(token)

            response = self._verify(token)
            if response.status_code == 200:
                cache.set(secure_token, 1, TOKEN_EXPIRE_TIME * 60)
                return self._decode_token(token)
            
        return None, None
