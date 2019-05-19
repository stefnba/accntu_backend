from django.urls import path

from .views import (
    AssignableTransactionsList,
    ItemRetrieveUpdate,
    ReportListDraft,
    ReportListSubmitted,
    TransactionRetrieveUpdate,
)

app_name = "business"


urlpatterns = [
    path('assignable_transactions/', AssignableTransactionsList.as_view(), name='report-list-draft'),
    path('item/<int:pk>/', ItemRetrieveUpdate.as_view(), name='item-detail'),
    path('reports/draft/', ReportListDraft.as_view(), name='report-list-draft'),
    path('reports/submitted/', ReportListSubmitted.as_view(), name='report-list-submitted'),
    path('reports/report/<int:id>/', TransactionRetrieveUpdate.as_view(), name='report-detail'),
]