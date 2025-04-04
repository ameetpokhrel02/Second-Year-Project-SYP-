from django.core.management.base import BaseCommand
from Menu.models import Product

class Command(BaseCommand):
    help = 'Adds initial products to the database'

    def handle(self, *args, **kwargs):
        # Clear existing products
        Product.objects.all().delete()
        
        # Non-Vegetarian Products
        Product.objects.create(
            name='Chicken Wings',
            description='Crispy and spicy chicken wings',
            price=200.00,
            category='non_veg',
            image='products/chickenwings1.jpg'
        )
        
        Product.objects.create(
            name='Momo',
            description='Steamed dumplings with chicken filling',
            price=150.00,
            category='non_veg',
            image='products/momo2.webp'
        )
        
        Product.objects.create(
            name='Chicken 65',
            description='Spicy and crispy chicken pieces',
            price=180.00,
            category='non_veg',
            image='products/chicken 65.jpg'
        )
        
        # Vegetarian Products
        Product.objects.create(
            name='Pakoda',
            description='Crispy vegetable fritters',
            price=80.00,
            category='veg',
            image='products/pppakaoda.jpg'
        )
        
        Product.objects.create(
            name='Chowmein',
            description='Stir-fried noodles with vegetables',
            price=120.00,
            category='veg',
            image='products/chowmein.webp'
        )
        
        Product.objects.create(
            name='Vegetable Sandwich',
            description='Fresh vegetables between bread slices',
            price=100.00,
            category='veg',
            image='products/sandwhich.webp'
        )
        
        # Cold Drinks
        Product.objects.create(
            name='Fanta',
            description='Orange flavored carbonated drink',
            price=50.00,
            category='drinks',
            image='products/fanta.webp'
        )
        
        Product.objects.create(
            name='Coca Cola',
            description='Classic cola drink',
            price=60.00,
            category='drinks',
            image='products/cokesss.jpg'
        )
        
        Product.objects.create(
            name='Red Bull',
            description='Energy drink',
            price=55.00,
            category='drinks',
            image='products/redbull.jpg'
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully added products')) 