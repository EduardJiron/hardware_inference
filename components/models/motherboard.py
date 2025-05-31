
from django.db import models

class Motherboard(models.Model):
    model = models.CharField(max_length=100)
    socket_type = models.CharField(max_length=50)
    chipset = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=50)
    supported_memory_types = models.JSONField()
    max_memory_gb = models.IntegerField()
    memory_slots = models.IntegerField()
    pci_express_slots = models.IntegerField()
    m2_slots = models.IntegerField()
    sata_ports = models.IntegerField()
    integrated_wifi = models.BooleanField()
    integrated_audio = models.BooleanField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    supported_cpu_tiers = models.CharField(max_length=50)
    purpose = models.CharField(max_length=50)

    def __str__(self):
        return self.model
