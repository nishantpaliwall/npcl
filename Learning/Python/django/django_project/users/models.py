from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}, Profile'


    # Overide Save method to add some functionality 
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        # Reducig the image size to save file sysytem space
        
        if img.height > 300 or img.width > 300:
            update_size = (300,300)
            img.thumbnail(update_size)
            img.save(self.image.path)
            