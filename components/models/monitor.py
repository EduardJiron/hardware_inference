from django.db import models

class Monitor(models.Model):
    model = models.CharField(max_length=100)
    size_inches = models.FloatField()
    resolution = models.CharField(max_length=20)  # Ej: "3840x2160"
    refresh_rate_hz = models.IntegerField()
    panel_type = models.CharField(max_length=20)  # Ej: OLED, IPS, VA
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    video_output_interface = models.JSONField()  # Ej: ["USB-C", "VGA"]
    purpose = models.CharField(max_length=50)  # Ej: gaming, diseño, oficina

    def __str__(self):
        return self.model