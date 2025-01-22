from django.urls import path
from .views import ListCreateTransferView, TransferDetailView, ListCreateMyTransferView, ListCreateRejectTransferView, ListCreateApproveTransferView

urlpatterns = [
    path('transfer-request/', ListCreateTransferView.as_view(), name="transfers-list-create"),
    path('my-transfer-request/', ListCreateMyTransferView.as_view(), name="my-transfers-list-create"),
    path('transfer-request/approve/', ListCreateApproveTransferView.as_view(), name="approve-transfers-list-create"),
    path('transfer-request/reject/', ListCreateRejectTransferView.as_view(), name="reject-transfers-list-create"),
    path('transfer-request/<int:pk>/', TransferDetailView.as_view(), name="transfers-detail"),

]
