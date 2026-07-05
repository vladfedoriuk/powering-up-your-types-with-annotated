---
layout: default
class: code-center
---


# The Django way

<div class="divider-red"></div>

```python
class Room(models.Model):
    room_id = models.CharField(max_length=20, unique=True, db_index=True)
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_id", "capacity"]
```

<!--
Django uses the Active Record pattern — the database table is the one model that dictates everything.

Change a field, and that ripples through the serializer, the validation, the views. There's no separate layer holding your business rules — just the database, pushing pressure onto everything above it.
-->
