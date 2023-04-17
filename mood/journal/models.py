from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    number_of_meditations = models.IntegerField(default=0)
    def __str__(self):
        return self.username
    def serialize(self):
        return {
            "username": self.username,
            "number_of_meditations": self.number_of_meditations
        }

class Entry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_entries")
    entry_title = models.TextField(default="")
    entry_body = models.TextField(default="")
    date = models.DateTimeField(default=now)
    emotion = models.TextField(default="happy")
    image = models.TextField(default='')  

    def serialize(self):
        return {
            "entry_title": self.entry_title,
            "entry_body": self.entry_body,
            "date": self.date,
            "emotion": self.emotion,
            "image": self.image
        }  
