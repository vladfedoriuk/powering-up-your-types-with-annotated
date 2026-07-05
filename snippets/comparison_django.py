from decimal import Decimal
from pathlib import Path
from typing import Annotated

from annotated_types import Ge, Le
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import include as django_include
from nanodjango import Django


_ROOT = Path(__file__).resolve().parent.parent

# --- Semantic types (documentation only — Django defines its own constraints via Field) ---
NightCount = Annotated[int, Ge(1), Le(365)]
Percentage = Annotated[Decimal, Ge(0), Le(100)]
TaxRate = Annotated[Decimal, Ge(0), Le(1)]

app = Django(
    SQLITE_DATABASE=str(_ROOT / "reservations_django.db"),
    INSTALLED_APPS=lambda apps: apps + ["rest_framework"],
    MIGRATIONS_DIR="django_migrations",
)

from rest_framework import serializers, viewsets  # noqa: E402
from rest_framework.routers import DefaultRouter  # noqa: E402


@app.admin(list_display=["room_id", "capacity"])
class Room(models.Model):
    # Django owns field shape, validation, DB mapping, admin metadata, and runtime API.
    # Domain meaning is coupled to framework field declarations.
    room_id = models.CharField(max_length=20, unique=True, db_index=True)
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self) -> str:
        return self.room_id

    def add_reservation(self, reservation: "Reservation") -> None:
        if reservation.room_id != self.room_id:
            raise ValueError("Reservation belongs to another room")
        if reservation.guest_count > self.capacity:
            raise ValueError("Reservation exceeds room capacity")
        if reservation.night_count < 1:
            raise ValueError("Reservation must last at least one night")
        if any(reservation.overlaps(existing) for existing in self.reservations.all()):
            raise ValueError("Reservation overlaps existing reservation")
        reservation.room = self
        reservation.save()


@app.admin(list_display=["room", "guest_count", "rate", "starts_at", "ends_at"])
class Reservation(models.Model):
    room = models.ForeignKey(
        Room, related_name="reservations", on_delete=models.CASCADE
    )
    guest_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    starts_at = models.DateField()
    ends_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def night_count(self) -> NightCount:
        return self.ends_at.toordinal() - self.starts_at.toordinal()

    def overlaps(self, other: "Reservation") -> bool:
        return self.starts_at < other.ends_at and other.starts_at < self.ends_at


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_id", "capacity"]


class ReservationSerializer(serializers.ModelSerializer):
    night_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "room",
            "guest_count",
            "rate",
            "starts_at",
            "ends_at",
            "created_at",
            "night_count",
        ]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"reservations", ReservationViewSet, basename="reservation")

app.route("/api/", include=django_include(router.urls))


def calculate_stay_total(
    reservation: Reservation,
    discount_percent: Percentage = Decimal(0),
    tax_rate: TaxRate = Decimal("0.1"),
) -> Decimal:
    subtotal = reservation.rate * Decimal(reservation.night_count)
    discount_amount = subtotal * (discount_percent / Decimal(100))
    total = (subtotal - discount_amount) * (Decimal(1) + tax_rate)
    return total.quantize(Decimal("0.01"))


if __name__ == "__main__":
    app.run()
