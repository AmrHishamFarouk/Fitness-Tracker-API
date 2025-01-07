from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('RUN', 'Running'),
        ('CYC', 'Cycling'),
        ('WL', 'Weightlifting'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=3, choices=ACTIVITY_TYPES)
    duration = models.IntegerField()
    distance = models.FloatField(blank=True, null=True)
    calories_burned = models.FloatField(blank=True, null=True)
    date = models.DateField()

    def clean(self):
        if not self.activity_type:
            raise ValidationError('Activity Type is required.')
        if self.duration is None or self.duration <= 0:
            raise ValidationError('Duration is required or invalid.')
        if not self.date:
            raise ValidationError('Date is required.')

    def save(self, *args, **kwargs):
        # Call clean() before saving to ensure validation
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.activity_type} by {self.user.username} on {self.date}"
