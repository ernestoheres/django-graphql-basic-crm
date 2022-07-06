from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator

# Create your models here.
class User(models.Model):
    email = models.EmailField(validators=[EmailValidator()])
    name = models.CharField(max_length=30, validators=[MinLengthValidator(2)])
    password = models.CharField(max_length=256,validators=[MinLengthValidator(8)] )

    