from django.urls import path, include
from rest_framework.routers import DefaultRouter

from submissions.apis.SubmissionBatchMVS import SubmissionBatchMVS
from submissions.apis.SubmissionMVS import SubmissionMVS

router = DefaultRouter()

router.register(r'submission-batches', SubmissionBatchMVS, basename='submission-batch')
router.register(r'submissions', SubmissionMVS, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]
