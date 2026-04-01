from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import POSProduct, Sale, POSCustomer
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusPOS with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuspos.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if POSProduct.objects.count() == 0:
            for i in range(10):
                POSProduct.objects.create(
                    name=f"Sample POSProduct {i+1}",
                    sku=f"Sample {i+1}",
                    category=f"Sample {i+1}",
                    price=round(random.uniform(1000, 50000), 2),
                    cost=round(random.uniform(1000, 50000), 2),
                    quantity=random.randint(1, 100),
                    barcode=f"Sample {i+1}",
                    status=random.choice(["active", "inactive"]),
                    tax_rate=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 POSProduct records created'))

        if Sale.objects.count() == 0:
            for i in range(10):
                Sale.objects.create(
                    receipt_number=f"Sample {i+1}",
                    customer_name=f"Sample Sale {i+1}",
                    total=round(random.uniform(1000, 50000), 2),
                    discount=round(random.uniform(1000, 50000), 2),
                    tax=round(random.uniform(1000, 50000), 2),
                    payment_method=random.choice(["cash", "card", "upi", "wallet"]),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                    cashier=f"Sample {i+1}",
                    items_count=random.randint(1, 100),
                )
            self.stdout.write(self.style.SUCCESS('10 Sale records created'))

        if POSCustomer.objects.count() == 0:
            for i in range(10):
                POSCustomer.objects.create(
                    name=f"Sample POSCustomer {i+1}",
                    phone=f"+91-98765{43210+i}",
                    email=f"demo{i+1}@example.com",
                    loyalty_points=random.randint(1, 100),
                    total_purchases=round(random.uniform(1000, 50000), 2),
                    visit_count=random.randint(1, 100),
                    last_visit=date.today() - timedelta(days=random.randint(0, 90)),
                    tier=random.choice(["bronze", "silver", "gold", "platinum"]),
                )
            self.stdout.write(self.style.SUCCESS('10 POSCustomer records created'))
