from random import randint, choice, sample
from datetime import datetime
from faker import Faker
from sqlalchemy.orm import Session
from src.alchemy_db.session import SessionLocal
from src.alchemy_db.models import (
    Users,
    Client,
    Recipe,
    MenuItem,
    Supplier,
    ClientOrder,
    ClientOrderItem,
    KitchenOrder,
    KitchenOrderItem,
    Ingredient
)
def import_demo_data():
    fake = Faker()
    Faker.seed(42)

    db: Session = SessionLocal()

    # Fetch existing Recipes and Ingredients
    recipes = db.query(Recipe).all()
    ingredients = db.query(Ingredient).all()

    if not recipes or not ingredients:
        raise Exception("Recipes and Ingredients must be initialized before running this seed.")

    # --- Users ---
    users = []
    for _ in range(10):
        user = Users(username=fake.user_name(), email=fake.email())
        db.add(user)
        users.append(user)
    db.commit()

    # --- Clients ---
    clients = []
    for _ in range(10):
        client = Client(
            name=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        db.add(client)
        clients.append(client)
    db.commit()

    # --- Menu Items (linked to existing recipes) ---
    menu_items = []
    categories = ["Appetizer", "Main Course", "Dessert", "Beverage"]
    for recipe in sample(recipes, min(15, len(recipes))):
        item = MenuItem(
            recipe_id=recipe.recipe_id,
            name=fake.catch_phrase(),
            price=randint(5, 50),
            description=fake.sentences(),
            category=choice(categories),
            is_visible=choice([True, True, False]),  # mostly visible
            added_on=fake.date_time_this_year()
        )
        db.add(item)
        menu_items.append(item)
    db.commit()

    # --- Suppliers ---
    suppliers = []
    supplier_types = ["Local", "International", "Organic"]
    for _ in range(5):
        supplier = Supplier(
            name=fake.company(),
            contact_name=fake.name(),
            phone_number=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
            supplier_type=choice(supplier_types),
            tax_id=fake.bothify(text="??######"),
            payment_terms=choice(["Net 30", "Net 60", "Prepaid"]),
            lead_time_days=randint(1, 14),
            rating=randint(1, 5),
            active=True
        )
        db.add(supplier)
        suppliers.append(supplier)
    db.commit()

    # --- Client Orders and Items (linked to existing MenuItems) ---
    client_orders = []
    for client in clients:
        for _ in range(randint(1, 3)):  # 1-3 orders per client
            order = ClientOrder(
                client_id=client.client_id,
                order_date=fake.date_time_this_month(),
                served=choice([True, False]),
                notes=fake.sentence()
            )
            db.add(order)
            client_orders.append(order)
    db.commit()

    for order in client_orders:
        items_count = randint(1, min(5, len(menu_items)))
        for menu_item in sample(menu_items, items_count):
            item = ClientOrderItem(
                order_id=order.order_id,
                menu_item_id=menu_item.menu_item_id,
                quantity=randint(1, 3),
                price=randint(5, 50)
            )
            db.add(item)
    db.commit()

    # --- Kitchen Orders and Items (linked to existing Ingredients) ---
    kitchen_orders = []
    for supplier in suppliers:
        for _ in range(randint(1, 3)):
            order = KitchenOrder(
                supplier_id=supplier.supplier_id,
                order_date=fake.date_time_this_month(),
                delivered=choice([True, False]),
                notes=fake.sentence()
            )
            db.add(order)
            kitchen_orders.append(order)
    db.commit()

    for order in kitchen_orders:
        items_count = randint(1, min(5, len(ingredients)))
        for ingredient in sample(ingredients, items_count):
            item = KitchenOrderItem(
                order_id=order.order_id,
                ingredient_id=ingredient.ingredient_id,
                quantity=randint(1, 20),
                unit= fake.word()
            )
            db.add(item)
    db.commit()

    print("✅ Database seeded successfully with existing Recipes and Ingredients!")