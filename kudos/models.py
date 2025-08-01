from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

KUDOS_LIMIT = 3


class Organization(models.Model):
    id = models.UUIDField(
        editable=False,
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique identifier for the organization record.",
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the data was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the data was last updated."
    )
    is_deleted = models.BooleanField(
        default=False, help_text="Indicates if the data is deleted."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"


class User(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        help_text="The organization to which the user belongs.",
        null=True,
        blank=True,
    )

    def __str__(self):
        org_name = self.organization.name if self.organization else "No Organization"
        return f"{self.username} ({org_name})"

    def kudos_given_this_week(self):
        """
        Returns the number of kudos the user has sent from the start of the current week to now.
        """
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
        return self.kudos_sent.filter(timestamp__date__gte=start_of_week).count()

    def kudos_remaining(self):
        """
        Returns the number of kudos the user can still send this week.
        """
        return max(0, KUDOS_LIMIT - self.kudos_given_this_week())

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Kudo(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="kudos_sent",
        on_delete=models.CASCADE,
        help_text="The user who is sending the kudo.",
    )
    recipient = models.ForeignKey(
        User,
        related_name="kudos_received",
        on_delete=models.CASCADE,
        help_text="The user who is receiving the kudo.",
    )
    message = models.TextField(help_text="The appreciation or feedback message.")
    timestamp = models.DateTimeField(
         default=timezone.now, help_text="The date and time when the kudo was sent."
    )

    def __str__(self):
        return f"{self.sender} - {self.recipient} | {self.message[:30]}"

    class Meta:
        verbose_name = "Kudo"
        verbose_name_plural = "Kudos"
        ordering = ["-timestamp"]
