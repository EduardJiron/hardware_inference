from django.db import models

class PowerSupply(models.Model):
    model = models.CharField(max_length=100)
    wattage = models.IntegerField()
    modular = models.CharField(max_length=50)  # Ej: "fully-modular"
    efficiency_rating = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=50)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=50)
    performance_tier = models.CharField(max_length=20)

    def __str__(self):
        return self.model
