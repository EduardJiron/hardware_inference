from django.db import models


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
