from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AbbUserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    def __str__(self) -> str:
        return self.username
