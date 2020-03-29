from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.utils import json

from knuvote_app.enums import Order, Params
from django.core import serializers
from knuvote_app.permissions import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from knuvote_app.models import Category, User, Candidate
from rest_framework.status import *
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.core.mail import BadHeaderError, send_mail
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import logging
import facebook
from django.http import JsonResponse
import json
from knuvote_app.validators import Validators

logger = logging.getLogger(__name__)

@csrf_exempt
def addCandidate(request, categoryId):
    requestData = json.loads(request.readline())
    name = requestData['name']
    category = Category.objects.get(id=categoryId)
    if not IsOwner.has_object_permission(request, category):
        return ResponseMsg.ACCESS_FORBIDDEN
    candidate = Candidate(name=name, category=category, countvotes=0)
    candidate.save()
    return ResponseMsg.OK

@csrf_exempt
def editCandidate(request, categoryId):
    requestData = json.loads(request.readline())
    name = requestData['name']
    category = Category.objects.get(id=categoryId)
    if not IsOwner.has_object_permission(request, category):
        return ResponseMsg.ACCESS_FORBIDDEN
    candidate = Candidate.objectrs.get(id=requestData['id'])
    candidate.name = name
    candidate.save()
    return ResponseMsg.OK

@csrf_exempt
def removeCandidate(request, categoryId):
    requestData = json.loads(request.readline())
    category = Category.objects.get(id=categoryId)
    if not IsOwner.has_object_permission(request, category):
        return ResponseMsg.ACCESS_FORBIDDEN
    candidate = Candidate.objectrs.get(id=requestData['id'])
    candidate.delete()
    return ResponseMsg.OK

@csrf_exempt
def getCandidates(request, category):
    sought = request.GET.get('sought')
    order = '' if request.GET.get('order') == str(Order.ASC.value) else '-'
    sortBy = 'name' if request.GET.get('sortBy') == str(Params.NAME) else 'countvotes'
    candidates = Candidate.objects.filter(category=category).filter(name__icontains=sought)\
        .order_by(order + sortBy).values()
    return JsonResponse(list(candidates), safe=False, status=HTTP_200_OK)
