from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class ActivateToken(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    activation_token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Token aktywacyjny"
        
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    
    class Meta:
        verbose_name = "Profil użytkownika"
        verbose_name_plural = "Profile użytkowników"
    
    def __str__(self):
        return self.user.username
    