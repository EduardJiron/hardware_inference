from django.db import models

# ------------------------------
# CPU
# ------------------------------

# ------------------------------
# GPU
# ------------------------------
class GPU(models.Model):
    model = models.CharField(max_length=100)
    vram_gb = models.IntegerField()
    core_clock_mhz = models.IntegerField()
    boost_clock_mhz = models.IntegerField()
    power_draw_w = models.IntegerField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    video_output_interface = models.JSONField()
    purpose = models.CharField(max_length=50)
    performance_tier = models.CharField(max_length=20)

    def __str__(self):
        return self.model

# ------------------------------
# RAM
# ------------------------------


# ------------------------------
# Almacenamiento
# ------------------------------
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

# ------------------------------
# Motherboard
# ------------------------------
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

# ------------------------------
# Fuente de Poder
# ------------------------------
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

# ------------------------------
# Cooler
# ------------------------------
class Cooler(models.Model):
    model = models.CharField(max_length=100)
    type = models.CharField(max_length=20)  # Ej: air, liquid
    compatible_sockets = models.JSONField()
    noise_level_db = models.FloatField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    performance_tier = models.CharField(max_length=20)

    def __str__(self):
        return self.model

# ------------------------------
# Case
# ------------------------------
class Case(models.Model):
    model = models.CharField(max_length=100)
    form_factor = models.CharField(max_length=50)
    rgb = models.BooleanField()
    included_fans = models.IntegerField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=50)

    def __str__(self):
        return self.model
