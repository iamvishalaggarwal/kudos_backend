from django.core.management.base import BaseCommand
from kudos.models import User, Organization, Kudo
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Generate fixture data with users and kudos'

    def handle(self, *args, **kwargs):
        org = Organization.objects.create(name="TestOrg")

        users = []
        for i in range(5):
            user = User.objects.create_user(
                username=f"user{i}",
                password="pass@123",
                organization=org
            )
            users.append(user)

        messages = [
            "Great work!", "Well done!", "Thanks for your help!",
            "You nailed it!", "Really appreciate your efforts!"
        ]

        for _ in range(10):
            sender = random.choice(users)
            recipient = random.choice([u for u in users if u != sender])
            message = random.choice(messages)

            Kudo.objects.create(
                sender=sender,
                recipient=recipient,
                message=message,
                timestamp=timezone.now() - timezone.timedelta(days=random.randint(0, 6))
            )

        self.stdout.write(self.style.SUCCESS("Fixtures created."))
