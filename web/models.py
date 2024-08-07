from django.db import models
import uuid
# Create your models here.
class Flan(models.Model):
    flan_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    image_url = models.URLField(default='https://acortar.link/Hs3SLR')
    slug = models.SlugField(max_length=64, unique=True, default='default-slug')
    is_private = models.BooleanField()
    price = models.IntegerField(default=2000)
    actual_offer = models.IntegerField(default=50)
    offer = models.JSONField(default=[10, 15, 20, 25, 30, 35]) 


class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()
