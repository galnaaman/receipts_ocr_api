from django.urls import path
from .views import ReceiptUploadView

urlpatterns = [
    path('upload-receipt/', ReceiptUploadView.as_view(), name='upload-receipt'),
]
