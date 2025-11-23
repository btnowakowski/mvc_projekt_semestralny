from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="slots")
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.end <= self.start:
            raise ValidationError("Koniec musi być po starcie.")
        if self.start < timezone.now():
            raise ValidationError("Nie możesz dodać terminu w przeszłości.")

    class Meta:
        unique_together = ("service", "start")
        ordering = ["start"]

    def __str__(self):
        return f"{self.service.name} | {self.start:%Y-%m-%d %H:%M}"


class Reservation(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Oczekująca"
        APPROVED = "approved", "Zatwierdzona"
        CANCELLED = "cancelled", "Anulowana"
        REJECTED = "rejected", "Odrzucona"

    archived_start = models.DateTimeField(null=True, blank=True)
    archived_end = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    slot = models.OneToOneField(
        TimeSlot, on_delete=models.PROTECT, null=True, blank=True
    )

    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.slot:
            dt = self.slot.start
        else:
            dt = self.archived_start

        dt_str = dt.strftime("%Y-%m-%d %H:%M") if dt else "brak daty"

        return f"{self.user} -> {self.service} @ {dt_str} ({self.status})"
