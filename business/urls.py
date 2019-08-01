from django.urls import path

from .views import (
    ItemListFilteredByReport,
    ItemRetrieveUpdate,
    ReportCreate,
    ReportList,
    ReportRetrieveUpdate,
    ReportDestroy,
)

app_name = "business"


urlpatterns = [
    
    # Item
    path('items/item/<int:pk>/', ItemRetrieveUpdate.as_view(), name='item-retrieve-update'),
    path('items/no-report/', ItemListFilteredByReport.as_view(), name='item-list-filtered-by-report'),
    path('reports/report/<int:report>/items/', ItemListFilteredByReport.as_view(), name='item-list-filtered-by-report'),
    
    # Report
    path('reports/<str:status>/', ReportList.as_view(), name='report-list'),
    path('reports/report/<int:id>/', ReportRetrieveUpdate.as_view(), name='report-retrieve-update'),
    path('reports/report/<int:id>/delete/', ReportDestroy.as_view(), name='report-destroy'),
    path('reports/report/create/', ReportCreate.as_view(), name='report-create'),
]