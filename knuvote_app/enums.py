from enum import Enum

from django.http import JsonResponse
from rest_framework.status import *


class Provider(Enum):
    FACEBOOK = 1
    GOOGLE = 2
    INSTAGRAM = 3

class Order(Enum):
    ASC = 0
    DESC = 1

class Params(Enum):
    RELEVANCE = 0
    NAME = 1

class ResponseMsg():
    INCORRECT_DATA = JsonResponse({'message':'Incorrect data'}, status=HTTP_400_BAD_REQUEST)
    EMAIL_IN_USE = JsonResponse({'message': 'Email already in use'}, status=HTTP_409_CONFLICT)
    UNEXPECTED_ERROR = JsonResponse({'message': 'Internal server error'}, status = HTTP_408_REQUEST_TIMEOUT)
    INVALID_CRED = JsonResponse({'message': 'Invalid email or password'}, status = HTTP_400_BAD_REQUEST)
    OK = JsonResponse({'message': 'Success'}, status=HTTP_200_OK)
    NOT_FOUND = JsonResponse({'message': 'Page not found'}, status=HTTP_404_NOT_FOUND)
    ACCESS_FORBIDDEN = JsonResponse({'message': 'Access forbidden'}, status=HTTP_403_FORBIDDEN)
    UNAUTHORIZED = JsonResponse({'message': 'Access forbidden'}, status=HTTP_401_UNAUTHORIZED)