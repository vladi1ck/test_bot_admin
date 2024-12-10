from django.db import models

class FAQ(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    answer = models.TextField( blank=False, null=False)