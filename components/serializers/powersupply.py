from rest_framework import serializers
from ..models.powersupply import PowerSupply
class PowerSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerSupply  
        fields = '__all__'

class PowerSupplyInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField(required=False, allow_blank=True)
    max_price_usd = serializers.FloatField(required=False)
    wattage = serializers.IntegerField(required=False)
    modular = serializers.CharField(required=False, allow_blank=True)
    efficiency_rating = serializers.CharField(required=False, allow_blank=True)
    form_factor = serializers.CharField(required=False, allow_blank=True)
    performance_tier = serializers.CharField(required=False, allow_blank=True)

