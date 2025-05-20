from django.db import models
from django.contrib.auth.models import User

class Product(models.Model): 
    name = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self): 
        return self.name


class APIRight(models.Model):
    endpoint_name = models.CharField(max_length=100)  # Ex: 'ProductListView'
    token = models.CharField(max_length=100)  # Le token de l'utilisateur
    can_access = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.token} -> {self.endpoint_name} = {self.can_access}"



from django.db import models
from django.contrib.auth.models import User

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    body = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user or self.token} | {self.method} {self.path} @ {self.timestamp}"
