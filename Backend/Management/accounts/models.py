from django.db import models

class Admin(models.Model):
    keycloak_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)

    roles = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True