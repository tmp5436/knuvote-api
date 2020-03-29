from rest_framework.utils import json

from knuvote_app.enums import ResponseMsg
from knuvote_app.permissions import *
from knuvote_app.models import Category, User
from rest_framework.status import *
from rest_framework.authtoken.models import Token
from django.core.mail import BadHeaderError, send_mail
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import logging
from django.http import JsonResponse
import json

from knuvote_app.validators import Validators

logger = logging.getLogger(__name__)

@csrf_exempt
def registration(request):
    requestData = json.loads(request.readline())
    user = User(username=requestData['username'],
                email=requestData['email'],
                password=requestData['password'], )


    if not Validators.userValidate(user):
        return ResponseMsg.INCORRECT_DATA

    user.set_password(requestData['password'])

    try:
        existUser = User.objects.get(email=user.email)
    except User.DoesNotExist:
        existUser = None

    if existUser:
        return ResponseMsg.EMAIL_IN_USE

    user.is_active = True # TODO remove
    user.save()
    token, _ = Token.objects.get_or_create(user=user)
    try:
        send_mail('Вам Повестка',
                    'Please click here : \n'
                    + 'https://knuvote.herokuapp.com/auth?token=' + token.key,
                    'voenkomat.ukr@gmail.com', [user.email])

    except BadHeaderError:
        return ResponseMsg.UNEXPECTED_ERROR

    return JsonResponse({'message': 'Check your email'}, status = HTTP_200_OK)

@csrf_exempt
def login(request):
    requestData = json.loads(request.readline())
    email = requestData['email']
    password = requestData['password']
    user = auth.authenticate(email=email, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key,
                             'username': user.username,
                             'email': user.email,
                             'id': user.id, })
    else:
        return ResponseMsg.INVALID_CRED

@csrf_exempt
def socialLogin(request):
    requestData = json.loads(request.readline())

    if not Validators.accessTokenValidate(requestData):
        return ResponseMsg.INCORRECT_DATA
    try:
        user = User.objects.get(email=requestData['email'])
    except User.DoesNotExist:
        user = None

    if user is None:
        user = User(username=requestData['name'],
                    email=requestData['email'],
                    is_active=True, )
        user.set_password(User.objects.make_random_password())
        user.save()

    token, _ = Token.objects.get_or_create(user=user)
    return JsonResponse({'token': token.key,
                         'username': user.username,
                         'email': user.email,
                         'id': user.id, })


@csrf_exempt
def verificationAccount(request):
    requestData = json.loads(request.readline())
    token = requestData['token']
    userId = Token.objects.get(key=token).user_id
    user = User.objects.get(id=userId)
    user.is_active = True
    user.save()
    return ResponseMsg.OK


@csrf_exempt
def getProfile(request):
    try:
        user = User.objects.get(id=request.GET['id'])
    except User.DoesNotExist:
        return ResponseMsg.NOT_FOUND
    return JsonResponse({'email': user.email,
                         'username': user.username,
                         'id': user.id, }, status=HTTP_200_OK)

@csrf_exempt
def editProfile(request):
    requestData = json.loads(request.readline())
    try:
        user = User.objects.get(id=requestData['id'])
    except User.DoesNotExist:
        return ResponseMsg.NOT_FOUND

    if not IsOwner.has_object_permission(request, user):
        return ResponseMsg.ACCESS_FORBIDDEN

    user.username = requestData['username']
    user.username = requestData['email']
    if not Validators.userValidate(user):
        return ResponseMsg.INCORRECT_DATA
    user.save()
    return ResponseMsg.OK