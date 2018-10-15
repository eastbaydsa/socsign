from django.db import models
from django.urls import reverse

import os
import binascii

def random_hex(count=8):
    return binascii.b2a_hex(os.urandom(count))[:count].decode('utf8')

class InterestChoice(models.Model):
    caption = models.CharField(max_length=128)
    tag = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.caption

class EventForm(models.Model):
    class Meta:
        ordering = ('-created', )

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    public_hex = models.CharField(
        max_length=10,
        default=random_hex,
        unique=True,
    )
    secret_hex = models.CharField(max_length=10, default=random_hex)

    event_id = models.CharField(max_length=64)
    event_title = models.CharField(max_length=255)

    VARIANT = (
        ('standard', 'Standard'),
        ('labor', 'Labor'),
    )
    variant = models.CharField(
        'Variant',
        choices=VARIANT,
        default='standard',
        max_length=20,
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    interest_choices = models.ManyToManyField(
        'InterestChoice',
        default=InterestChoice.objects.all,
    )

    def __str__(self):
        return '%s [%s]' % (self.event_title, self.event_id)

    def get_absolute_url(self):
        public_hex = self.public_hex
        secret_hex = self.secret_hex
        url = reverse('event_form', args=(public_hex,))
        return '%s?hx=%s' % (url, str(secret_hex))


class Record(models.Model):
    event = models.ForeignKey(EventForm, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

