from django.db import models

# ------------------------------
# CPU
# ------------------------------
class CPU(models.Model):
    model = models.CharField(max_length=100)
    clock_speed_ghz = models.FloatField()
    cores = models.IntegerField()
    cache_mb = models.IntegerField()
    memory_types = models.JSONField()
    integrated_gpu = models.CharField(max_length=100, null=True, blank=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=50)
    performance_level = models.CharField(max_length=20)
    socket_type = models.CharField(max_length=50)

    def __str__(self):
        return self.model
