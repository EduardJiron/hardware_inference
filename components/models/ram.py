from django.db import models

# ------------------------------
# RAM
# ------------------------------
class RAM(models.Model):
    model = models.CharField(max_length=100)
    capacity_gb = models.IntegerField()
    modules = models.IntegerField()
    speed_mhz = models.IntegerField()
    type = models.CharField(max_length=20)
    ecc = models.BooleanField()
    rgb = models.BooleanField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    voltage = models.FloatField()
    form_factor = models.CharField(max_length=50)
    purpose = models.CharField(max_length=50)
    performance_tier = models.CharField(max_length=20)

    def __str__(self):
        return self.model
