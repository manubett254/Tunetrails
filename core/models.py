from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.postgres.fields import ArrayField  # only for PostgreSQL

INSTRUMENT_CHOICES = [
    ('piano', 'Piano'),
    ('guitar', 'Guitar'),
    ('bass', 'Bass'),
    ('drums', 'Drums'),
    ('sax', 'Saxophone'),
    ('violin', 'Violin'),

]

# Change from ArrayField or simple CharField to:


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    instruments_taught = models.CharField(max_length=255)

    bio = models.TextField()

    def __str__(self):
        return self.name
