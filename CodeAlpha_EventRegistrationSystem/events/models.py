from django.db import models


class Event(models.Model):

    CATEGORY_CHOICES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('tech', 'Tech'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="events/", blank=True, null=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='tech'
    )

    def __str__(self):
        return self.title


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=150)

    def __str__(self):
        return self.name