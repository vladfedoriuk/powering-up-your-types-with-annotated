from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from nanodjango import Django
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

app = Django(
    SQLITE_DATABASE="nanodjango_reservations.sqlite3",
    MIGRATIONS_DIR="nanodjango_reservation_migrations",
    INSTALLED_APPS=["rest_framework"],
)


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


@app.admin(list_display=["room", "guest_count", "rate"])
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


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_id", "capacity"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "room", "guest_count", "rate"]


@app.route("/api/rooms/", name="room-list")
@api_view(["GET", "POST"])
def room_list(request):
    if request.method == "GET":
        serializer = RoomSerializer(Room.objects.all(), many=True)
        return Response(serializer.data)

    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@app.route("/api/reservations/", name="reservation-list")
@api_view(["GET", "POST"])
def reservation_list(request):
    if request.method == "GET":
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(serializer.data)

    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
