from django.db import models

class Storage(models.Model):
    model = models.CharField(max_length=100)
    type = models.CharField(max_length=20)  # SSD, HDD, etc.
    interface = models.CharField(max_length=50)
    form_factor = models.CharField(max_length=50)
    capacity_gb = models.IntegerField()
    read_speed_mb_s = models.IntegerField()
    write_speed_mb_s = models.IntegerField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    requires_m2_slot = models.BooleanField()
    requires_sata_port = models.BooleanField()
    purpose = models.CharField(max_length=50)
    performance_tier = models.CharField(max_length=20)

    def __str__(self):
        return self.model