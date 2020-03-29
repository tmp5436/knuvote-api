from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.contrib.auth import get_user_model

#User = get_user_model()
from django.http import JsonResponse
from rest_framework.status import *

class User(AbstractBaseUser):

    # user_id = models.IntegerField(verbose_name='user_id',
    #     #                             null=True,
    #     #                             unique=True, )

    username = models.CharField(verbose_name='username',
                                db_index=True,
                                max_length=66, )

    email = models.EmailField(verbose_name='email',
                              max_length=255,
                              unique=True, )

    is_active = models.BooleanField(verbose_name='is_active',
                                    default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(verbose_name='name',
                            db_index=True,
                            max_length=66, )

    expiration_time = models.DateTimeField(verbose_name='expiration_time')

    creator = models.ForeignKey(User,
                                  verbose_name='creator_id',
                                  on_delete=models.CASCADE, )

class Candidate(models.Model):
    name = models.CharField(verbose_name='name',
                            db_index=True,
                            max_length=66, )

    countvotes = models.IntegerField(verbose_name='count_votes')

    category = models.ForeignKey(Category,
                                   verbose_name='category_id',
                                   on_delete=models.CASCADE, )

class Vote(models.Model):
    user = models.ForeignKey(User,
                               verbose_name='user_id',
                               on_delete=models.CASCADE, )

    candidate = models.ForeignKey(Candidate,
                                    verbose_name='candidate_id',
                                    on_delete=models.CASCADE, )