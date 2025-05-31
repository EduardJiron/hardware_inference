from rest_framework import serializers
from ..models.monitor import Monitor

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = '__all__'

class MonitorInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    max_price_usd = serializers.FloatField()
    size_inches = serializers.FloatField(required=False, allow_null=True)
    resolution = serializers.CharField(required=False, allow_null=True)
    refresh_rate_hz = serializers.IntegerField(required=False, allow_null=True)
    panel_type = serializers.CharField(required=False, allow_null=True)
    video_output_interface = serializers.ListField(
        child=serializers.CharField(), required=False, allow_null=True
    )
