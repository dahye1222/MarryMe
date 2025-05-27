from django.db import models

class MetalPrice(models.Model):
    METAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
    ]

    metal_type = models.CharField(max_length=10, choices=METAL_CHOICES)
    date = models.DateField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()

    class Meta:
        unique_together = ['metal_type', 'date']
        ordering = ['date']

    def __str__(self):
        return f"{self.metal_type} - {self.date}"
