from django.conf import settings
from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

# from transactions.models import Transaction

# Create your models here.


class ReportManager(models.Manager):
    """ QuerySet manager for Report model to add non-database, calculated fields. """
    
    def get_queryset(self):
        qs = super(ReportManager, self).get_queryset().annotate(report_total=Coalesce(Sum('item__report_amount'), 0)).annotate(nmbr_items=Coalesce(Count('item'), 0))
        return qs


class Report(models.Model):
    
    STATUS_CHOICES = (
        ('draft','Draft'), 
        ('submitted','Submitted'),
        ('paid-out','Paid-out'),
    )

    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='draft')
    start_date = models.DateField()
    end_date = models.DateField()
    
    submit_date = models.DateField(blank=True, null=True)
    submit_amount = models.DecimalField(decimal_places=4, max_digits=1000, default=0)
    payout_date = models.DateField(blank=True, null=True)
    payout_amount = models.DecimalField(decimal_places=4, max_digits=1000, default=0)
    d_payout_submit = models.DecimalField(decimal_places=4, max_digits=1000, default=0)

    objects = ReportManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['updated_at',]


class Item(models.Model):
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, blank=True, null=True, related_name='item') # related_name for source in serializer
    report_amount = models.DecimalField(decimal_places=2, max_digits=1000, default=0)
    transaction = models.OneToOneField(to='transactions.Transaction', on_delete=models.CASCADE, primary_key=True)
    active = models.BooleanField(default=True)
    has_receipt = models.BooleanField(default=False)
    has_system = models.BooleanField(default=False)
