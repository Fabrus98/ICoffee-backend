from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Crea utenti predefiniti"

    def handle(self, *args, **kwargs):
        users = [
            ("admin", "1234", True),
            ("Fabrizio", "1234", True),

        ]

        for username, pwd, is_admin in users:
            if not User.objects.filter(username=username).exists():
                if is_admin:
                    User.objects.create_superuser(username=username, password=pwd)
                    self.stdout.write(self.style.SUCCESS(f"Creato admin {username}"))
                else:
                    User.objects.create_user(username=username, password=pwd)
                    self.stdout.write(self.style.SUCCESS(f"Creato utente {username}"))


'''            ("Stefano", "1234", True),
            ("Alessandro", "1234", True),
            ("Gianluca", "1234", True),
            ("Luca", "1234", True),
            ("Alberto", "1234", True),
            ("Giuseppe", "1234", True),
            ("Marianna", "1234", False),
            ("Mirko", "1234", False),
            ("Arianna", "1234", False),
            ("Michela", "1234", False),'''