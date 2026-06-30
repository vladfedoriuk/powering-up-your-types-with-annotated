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
Django uses the Active Record pattern. The database table shape is the single model that dictates everything.

When a DB field evolves, that change ripples through your serializer, validation checks, and views. There is no independent domain layer. The database exerts continuous design pressure on your entire code structure.
-->
