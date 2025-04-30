from django.db import models

# Create your models here.
class Product(models.Model): 
    name = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self): 
        return self.name


from django.db import models

class APIRight(models.Model):
    endpoint_name = models.CharField(max_length=100)  # Ex: 'get_all_products'
    token = models.CharField(max_length=100)  # Un token simple pour simuler l'authentification
    can_access = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.token} -> {self.endpoint_name} = {self.can_access}"
