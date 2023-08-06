from django.db import models


class FECConsumedLimit(models.Model):
    PersonId = models.CharField(max_length=1000, primary_key=True)
    NationalID = models.CharField(max_length=255, primary_key=True)
    NumberOfApplications = models.IntegerField(null=True)
    TotalConsumedLimit = models.BigIntegerField(null=True)
    TotalEMI = models.BigIntegerField(null=True)
    FromDate = models.CharField(max_length=8, null=True, default=None)
    ToDate = models.CharField(max_length=8, null=True, default=None)
    Status = models.CharField(max_length=32, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
