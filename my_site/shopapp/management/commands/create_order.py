from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order

class Command(BaseCommand):
    """
    Create orders
    """
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username="admin")
        order, created = Order.objects.get_or_create(
            delivery_adress="ul Pushkina d 10",
            promocode="Sale1234",
            user=user
        )

        self.stdout.write(f"Order {order}, created={created}")