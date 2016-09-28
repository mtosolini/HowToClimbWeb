from django.db import models

# Create your models here.
class RateLimiter(models.Model):
    apiKey = models.CharField(max_length=100)
    region = models.CharField(max_length=10)
    calls = models.IntegerField()
    firstCall = models.DecimalField(decimal_places=3, max_digits=25)
    lastCall = models.DecimalField(decimal_places=3, max_digits=25)
    rate = models.DecimalField(decimal_places=3, max_digits=25)
    apiUrl = models.CharField(max_length=100)

    def __str__(self):
        return self.region


