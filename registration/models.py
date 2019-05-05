from django.db import models
from PIL import Image
# Create your models here.
class show_image(models.Model):
    s_image = models.ImageField(upload_to='pics',blank=True)