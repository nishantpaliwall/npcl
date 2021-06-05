from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class cls_view_details(models.Model):
    tittle = models.CharField(max_length=100)
    name = models.TextField()
    region = models.CharField(max_length=10)
    create_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.tittle
        
    # Create get absolute url method using reverse to return back to detail page with the same primary key
    def get_absolute_url(self):
        return reverse('dart-detail', kwargs={'pk': self.pk})    