from django.db import migrations

def add_initial_products(apps, schema_editor):
    Product = apps.get_model('Menu', 'Product')
    
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

def remove_products(apps, schema_editor):
    Product = apps.get_model('Menu', 'Product')
    Product.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('Menu', '0003_cart_created_at_cart_updated_at_product_category_and_more'),
    ]

    operations = [
        migrations.RunPython(add_initial_products, remove_products),
    ] 