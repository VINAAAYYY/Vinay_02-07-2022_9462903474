from django.urls import path
from .views import *

urlpatterns = [
    path('team/', teamView.as_view(), name="teamView"),
    path('task/', taskView.as_view(), name="taskView"),
    path("updateMembers/", updateMembers, name="updateMembers"),
    path("updateStatus/", updateStatus, name="updateStatus")
]
