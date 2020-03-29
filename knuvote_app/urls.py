from django.conf.urls import url, include
from django.contrib import admin
from knuvote_app.views import *
from django.urls import path
from . import views
from .views import user_view, candidate_view, category_view

app_name = 'KnuVote'

urlpatterns = [
    path('category/create/', category_view.categoryCreate),
    path('category/edit/', category_view.editCategory),
    path('category/all/', category_view.getCategories),
    path('category/', category_view.getCategory),
    path('category/stats', category_view.getStats),
    path('category/<int:categoryId>/vote/<int:candidateId>/', category_view.vote),
    path('category/<int:categoryId>/get-vote/', category_view.getVote),

    path('category/<int:categoryId>/add/', candidate_view.addCandidate),
    path('category/<int:categoryId>/remove/', candidate_view.removeCandidate),
    path('category/<int:categoryId>/edit/', candidate_view.editCandidate),
    path('category/candidates/<int:category>/', candidate_view.getCandidates),

    path('user/registration/', user_view.registration),
    path('user/verification-account/', user_view.verificationAccount),
    path('user/login/', user_view.login),
    path('user/social-login/', user_view.socialLogin),
    path('user/profile/', user_view.getProfile),
    path('user/edit-profile/', user_view.editProfile),

]