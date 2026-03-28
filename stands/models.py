from django.db import models
from django.conf import settings
import secrets
import string

class Stand(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    nom_prop = models.CharField(max_length=100)
    prenom_prop = models.CharField(max_length=100)
    adresse = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    numero_stand = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    # Champs pour la validation
    validation_code = models.CharField(max_length=10, blank=True, null=True)
    validation_code_expires = models.DateTimeField(blank=True, null=True)
    validation_comment = models.TextField(blank=True, null=True)
    
    # Champ pour le mot de passe temporaire défini par l'admin
    temp_password = models.CharField(max_length=128, blank=True, null=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                             null=True, blank=True, related_name='stands')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stands'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.numero_stand} - {self.nom}"
    
    def generate_validation_code(self):
        """Génère un code de validation unique à 6 chiffres"""
        alphabet = string.digits
        code = ''.join(secrets.choice(alphabet) for _ in range(6))
        return code
    
    def save(self, *args, **kwargs):
        if not self.numero_stand:
            last_stand = Stand.objects.all().order_by('id').last()
            next_id = (last_stand.id + 1) if last_stand else 1
            self.numero_stand = f"STD-{next_id:04d}"
        super().save(*args, **kwargs)


class Validation(models.Model):
    """Modèle pour enregistrer les validations des stands"""
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name='validations')
    valide_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    password_validation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'validations'
        verbose_name = 'Validation'
        verbose_name_plural = 'Validations'
    
    def __str__(self):
        return f"Validation de {self.stand.nom} par {self.valide_par.username}"
