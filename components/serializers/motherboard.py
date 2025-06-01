from rest_framework import serializers
from ..models.motherboard import Motherboard

class MotherboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motherboard
        fields = '__all__'

from rest_framework import serializers

class MotherboardInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    max_price_usd = serializers.FloatField()

    socket_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    chipset = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    form_factor = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    supported_memory_type = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    min_memory_slots = serializers.IntegerField(required=False, allow_null=True)
    min_max_memory_gb = serializers.IntegerField(required=False, allow_null=True)
    pci_express_slots = serializers.IntegerField(required=False, allow_null=True)
    m2_slots = serializers.IntegerField(required=False, allow_null=True)
    sata_ports = serializers.IntegerField(required=False, allow_null=True)

    integrated_wifi_required = serializers.BooleanField(required=False, default=False)
    integrated_audio_required = serializers.BooleanField(required=False, default=False)

    supported_cpu_tier = serializers.ChoiceField(
        choices=["budget", "midrange", "highend"],
        required=False,
        allow_null=True
    )
