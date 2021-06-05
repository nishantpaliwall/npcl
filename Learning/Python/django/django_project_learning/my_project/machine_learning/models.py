from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class ml_models(models.Model):
    model_name =  models.CharField(max_length=100)
    description =  models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='created_by')

    def __str__(self):
        return self.model_name

    # Create get absolute url method using reverse to return back to detail page with the same primary key
    def get_absolute_url(self):
        return reverse('machine_learning-detail', kwargs={'pk': self.pk})    