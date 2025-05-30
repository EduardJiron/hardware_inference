
from rest_framework import serializers
from ..models.ram import RAM

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = '__all__'
class RAMInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    performance_tier = serializers.ChoiceField(choices=["low", "mid", "high", "ultra"])
    max_price_usd = serializers.FloatField()
    capacity_gb = serializers.IntegerField(required=False)
    type = serializers.CharField()
    ecc_required = serializers.BooleanField(required=False, default=False)
    rgb_required = serializers.BooleanField(required=False, default=False)
    form_factor = serializers.CharField(required=False)
    speed_mhz = serializers.IntegerField(required=False)
