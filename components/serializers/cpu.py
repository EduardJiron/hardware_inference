from rest_framework import serializers
from ..models.cpu import CPU

class CPUInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField(required=False, allow_blank=True)
    performance_level = serializers.ChoiceField(choices=["low", "mid", "high", "ultra"], required=False)
    max_price_usd = serializers.FloatField(required=False)
    socket_type = serializers.CharField(required=False, allow_blank=True)
    integrated_gpu_required = serializers.BooleanField(required=False, allow_null=True)
    memory_type = serializers.CharField(required=False, allow_blank=True)
    cores = serializers.IntegerField(required=False, allow_null=True)
    clock_speed_ghz = serializers.FloatField(required=False, allow_null=True)


class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = '__all__'
