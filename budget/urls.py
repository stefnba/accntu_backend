from django.urls import path

from .views import (
    BudgetListFilteredByPeriod,
)

app_name = "budget"


urlpatterns = [
    
    # Expense
    path('expenses/', BudgetListFilteredByPeriod.as_view(), name='expense-list'),
]