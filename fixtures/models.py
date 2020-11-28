from django.db import models

# Create your models here.

class site_views(models.Model):
    page_name = models.CharField(max_length=100, primary_key=True)
    page_views = models.IntegerField(default=0)
