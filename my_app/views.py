from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Product
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Product, APIRight



# Exemple d'une vue simple de test
def test_json_view(request):
    data = {
        'name': 'John Doe',
        'age': 30,
        'location': 'New York',
        'is_active': True,
    }
    return JsonResponse(data)


# Vue pour obtenir tous les produits avec pagination
def get_all_products(request):
    # Récupérer tous les produits
    products = Product.objects.all()

    # Pagination : obtenir la page actuelle et le nombre de produits par page
    page_number = request.GET.get('page', 1)  # Page par défaut 1
    paginator = Paginator(products, 3)  # 3 produits par page

    try:
        page = paginator.page(page_number)  # Obtenir la page demandée
    except Exception:
        return JsonResponse({"message": "Page not found"}, status=404)

    # Formater les produits pour la réponse JSON
    products_data = [
        {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "description": product.description,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        for product in page
    ]

    # Informations sur la pagination
    pagination_info = {
        'current_page': page.number,
        'total_pages': paginator.num_pages,
        'total_products': paginator.count,
    }

    return JsonResponse({
        'products': products_data,
        'pagination': pagination_info
    })


# Vue pour obtenir le produit le plus cher
def get_most_expensive_product(request):
    product = Product.objects.order_by('-price').first()
    if product:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "description": product.description,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        return JsonResponse(product_data)
    else:
        return JsonResponse({"message": "No products found."}, status=404)


# Vue pour ajouter un nouveau produit
@csrf_exempt  # Désactive la vérification CSRF pour cette vue
def add_product(request):
    if request.method == 'POST':
        try:
            # Charger les données JSON envoyées dans la requête
            data = json.loads(request.body)
            
            # Récupérer les données du produit
            name = data.get('name')
            price = data.get('price')
            description = data.get('description', "")  # Description est optionnelle
            
            # Validation des données
            if not name or not price:
                return JsonResponse({'message': 'Name and price are required.'}, status=400)
            
            # Créer le produit
            new_product = Product.objects.create(
                name=name,
                price=price,
                description=description
            )
            
            # Retourner une réponse avec les données du produit ajouté
            return JsonResponse({
                'id': new_product.id,
                'name': new_product.name,
                'price': float(new_product.price),
                'description': new_product.description,
                'created_at': new_product.created_at,
                'updated_at': new_product.updated_at
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'message': 'Only POST method is allowed.'}, status=405)


# Vue pour mettre à jour un produit existant
@csrf_exempt
def update_product(request, product_id):
    if request.method == "PUT":
        # Essayer de charger les données JSON envoyées dans la requête
        try:
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')
            description = data.get('description')
        except ValueError:
            return JsonResponse({"message": "Invalid JSON data."}, status=400)

        try:
            # Trouver le produit à mettre à jour
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product not found."}, status=404)

        # Mettre à jour le produit avec les nouvelles valeurs
        if name:
            product.name = name
        if price:
            product.price = price
        if description:
            product.description = description

        product.save()  # Sauvegarder les modifications dans la base de données

        return JsonResponse({"message": "Product updated successfully", "id": product.id}, status=200)

    return JsonResponse({"message": "Only PUT method is allowed."}, status=405)


#gestion des autorisations
def get_all_products(request):
    token = request.headers.get('Authorization')

    if not token:
        return JsonResponse({'message': 'Authorization token required.'}, status=401)

    try:
        right = APIRight.objects.get(endpoint_name='get_all_products', token=token)
        if not right.can_access:
            return JsonResponse({'message': 'Access denied.'}, status=403)
    except APIRight.DoesNotExist:
        return JsonResponse({'message': 'No rights defined for this token.'}, status=403)

    # Si l'accès est autorisé, continuer normalement
    products = Product.objects.all()
    products_data = [
        {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "description": product.description,
            "created_at": product.created_at,
            "updated_at": product.updated_at
        }
        for product in products
    ]
    return JsonResponse(products_data, safe=False)



#SI VOUS SOUHAITEZ TESTER LES ROLES VOICI COMMENT PROCEDER


# Ouvre le shell Django
# Commande à taper dans ton terminal
# > python manage.py shell

# Puis, dans le shell Python :
from my_app.models import APIRight

# Crée un droit d'accès pour l'endpoint "get_all_products"
APIRight.objects.create(
    endpoint_name='get_all_products',
    token='abc123',
    can_access=True
)



from rest_framework import viewsets, generics
from .models import Product, APIRight
from .serializers import ProductSerializer, APIRightSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import HasEndpointAccess

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, HasEndpointAccess]

class APIRightViewSet(viewsets.ModelViewSet):
    queryset = APIRight.objects.all()
    serializer_class = APIRightSerializer
    permission_classes = [IsAuthenticated]
