from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
