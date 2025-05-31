
from rest_framework import serializers
from ..models.ram import RAM

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = '__all__'
class RAMInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField(allow_blank=True, required=False)
    performance_tier = serializers.ChoiceField(
        choices=["low", "mid", "high", "ultra"], required=False
    )
    max_price_usd = serializers.FloatField(required=False)
    capacity_gb = serializers.IntegerField(required=False)
    type = serializers.CharField(allow_blank=True, required=False)
    ecc_required = serializers.BooleanField(required=False, default=False)
    rgb_required = serializers.BooleanField(required=False, default=False)
    form_factor = serializers.CharField(allow_blank=True, required=False)
    speed_mhz = serializers.IntegerField(required=False)
