from rest_framework import serializers
from ..models.gpu import GPU
class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = '__all__'


class GPUInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    max_price_usd = serializers.FloatField()
    vram_gb = serializers.FloatField(required=False, allow_null=True)
    core_clock_mhz = serializers.IntegerField(required=False, allow_null=True)
    boost_clock_mhz = serializers.IntegerField(required=False, allow_null=True)
    power_draw_w = serializers.IntegerField(required=False, allow_null=True)
    video_output_interface = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
    performance_tier = serializers.ChoiceField(
        choices=["low", "mid", "high", "ultra"], required=False, allow_null=True
    )
