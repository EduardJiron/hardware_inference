from rest_framework import serializers
from ..models.cpu import CPU

class CPUInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    performance_level = serializers.ChoiceField(choices=["low", "mid", "high", "ultra"])
    max_price_usd = serializers.FloatField()
    socket_type = serializers.CharField()
    integrated_gpu_required = serializers.BooleanField()
    memory_type = serializers.CharField()
    cores = serializers.IntegerField(required=False)
    clock_speed_ghz = serializers.FloatField(required=False)

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = '__all__'
