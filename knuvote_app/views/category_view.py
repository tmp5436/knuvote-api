import os

from django.forms import model_to_dict
from rest_framework.utils import json
from django.core import serializers

from knuvote_app.enums import Order, Params
from knuvote_app.permissions import *
from rest_framework import generics
from knuvote_app.models import Category, User, Candidate, Vote
from rest_framework.status import *
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import logging
from django.http import JsonResponse
import json

from knuvote_app.validators import Validators
from django.core.paginator import Paginator
import configparser

thisfolder = os.path.abspath(__file__ + '/../..')
config = configparser.RawConfigParser()
config.read(os.path.join(thisfolder, 'app.properties'))

logger = logging.getLogger(__name__)


@csrf_exempt
def categoryCreate(request):
    requestData = json.loads(request.readline())
    if not IsAuthenticated.has_object_permission(request):
        return ResponseMsg.UNAUTHORIZED
    userId = Token.objects.get(key=request.headers['Authorization']).user_id
    user = User.objects.get(id=userId)
    category = Category(name = requestData['name'],
                       expiration_time = requestData['expiration_time'],
                       creator = user)
    if not Validators.categoryValidate(category):
        return ResponseMsg.INCORRECT_DATA
    category.save()
    return JsonResponse(model_to_dict(category), status=HTTP_200_OK)

@csrf_exempt
def getCategories(request):
    sought = request.GET.get('sought')
    order = 'asc' if request.GET.get('order') == str(Order.ASC.value) else 'desc'
    sortBy = 'Name' if request.GET.get('sortBy') == str(Params.NAME.value) else 'Votes'
    query = config.get('QueriesSection', 'query.getCategoriesBy{}.{}'.format(sortBy, order))
    categories = Category.objects.raw(query, ['%' + sought.lower() + '%',
                                              int(request.GET.get('page')) * int(request.GET.get('size')),
                                              int(request.GET.get('size'))])
    resList = list()
    for c in categories:
        resList.append(
            {'id': c.id, 'name': c.name, 'expiration_time': c.expiration_time, 'votes': c.votes, }
        )
    return JsonResponse(list(resList), safe=False, status = HTTP_200_OK, content_type='application/json')

@csrf_exempt
def getCategory(request):
    try:
        category = Category.objects.get(id=request.GET.get('id'))
    except Category.DoesNotExist:
        return ResponseMsg.NOT_FOUND
    return JsonResponse(model_to_dict(category), status=HTTP_200_OK)

@csrf_exempt
def editCategory(request):
    requestData = json.loads(request.readline())
    try:
        category = Category.objects.get(id=requestData['id'])
    except Category.DoesNotExist:
        return ResponseMsg.NOT_FOUND

    if not IsOwner.has_object_permission(request, category):
        return ResponseMsg.ACCESS_FORBIDDEN

    category.name = requestData['name']
    category.expiration_time = requestData['expiration_time']
    if not Validators.categoryValidate(category):
        return ResponseMsg.INCORRECT_DATA
    category.save()
    return ResponseMsg.OK

@csrf_exempt
def vote(request, categoryId, candidateId):
    try:
        userId = Token.objects.get(key=request.headers['Authorization']).user_id
    except Token.DoesNotExist:
        return ResponseMsg.UNAUTHORIZED
    user = User.objects.get(id=userId)
    query = config.get('QueriesSection', 'query.getVote')
    vote = Vote.objects.raw(query, [userId, categoryId])
    if len(vote) != 0:
        if vote[0].candidate.id != candidateId:
            makeVote(candidateId, user)
        candidate = Candidate.objects.get(id=vote[0].candidate.id)
        candidate.countvotes -= 1
        candidate.save()
        vote[0].delete()
    else:
        makeVote(candidateId, user)
    return ResponseMsg.OK

@csrf_exempt
def getVote(request, categoryId):
    try:
        userId = Token.objects.get(key=request.headers['Authorization']).user_id
    except Token.DoesNotExist:
        return ResponseMsg.UNAUTHORIZED
    query = config.get('QueriesSection', 'query.getVote')
    vote = Vote.objects.raw(query, [userId, categoryId])
    return JsonResponse({'id': vote[0].candidate.id if len(vote) != 0 else -1}, status=HTTP_200_OK)


@csrf_exempt
def getStats(request):
    countCategories = Category.objects.all().count()
    countVotes = Vote.objects.all().count()
    query = config.get('QueriesSection', 'query.getTopCategory')
    topCategory = Category.objects.raw(query)

    return JsonResponse({'countCategories': countCategories,
                         'countVotes': countVotes,
                         'topCategory': topCategory[0].name,
                         'topCategoryId': topCategory[0].id},
                        status=HTTP_200_OK)


def makeVote(candidateId, user):
    newCandidate = Candidate.objects.get(id=candidateId)
    newCandidate.countvotes += 1
    newVote = Vote(user=user, candidate=newCandidate)
    newCandidate.save()
    newVote.save()