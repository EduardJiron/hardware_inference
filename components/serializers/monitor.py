from rest_framework import serializers
from ..models.monitor import Monitor

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = '__all__'

class MonitorInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    max_price_usd = serializers.FloatField()
    size_inches = serializers.FloatField(required=False)
    resolution = serializers.CharField(required=False)
    refresh_rate_hz = serializers.IntegerField(required=False)
    panel_type = serializers.CharField(required=False)
    video_output_interface = serializers.ListField(
        child=serializers.CharField(), required=False
    )
