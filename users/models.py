from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('user', 'Utilisateur'),
    ]

    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    prenom     = models.CharField(max_length=100, blank=True, null=True)
    telephone  = models.CharField(max_length=20, blank=True, null=True)
    avatar     = models.ImageField(upload_to='avatars/', blank=True, null=True)
    reset_password_token   = models.CharField(max_length=100, blank=True, null=True)
    reset_password_expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.username} - {self.email}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def is_admin(self):
        return self.role == 'admin'
