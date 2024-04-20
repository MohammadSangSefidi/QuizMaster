from rest_framework.authentication import TokenAuthentication as BaseToken


class CustomTokenAuthentication(BaseToken):
    keyword = 'Karim'