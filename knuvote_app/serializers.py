from rest_framework import serializers
from knuvote_app.models import *


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', )

class CategoryDetailSerializer(serializers.ModelSerializer):
    creatorId = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Category
        fields = ('name', 'expirationTime','creatorId')

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'expirationTime', 'creatorId')

