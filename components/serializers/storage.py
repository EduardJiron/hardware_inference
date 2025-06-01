from rest_framework import serializers
from ..models.storage import Storage

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class StorageInferenceInputSerializer(serializers.Serializer):
    purpose = serializers.CharField()
    max_price_usd = serializers.FloatField()
    type = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    interface = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    form_factor = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    capacity_gb = serializers.IntegerField(required=False, allow_null=True)
    read_speed_mb_s = serializers.IntegerField(required=False, allow_null=True)
    write_speed_mb_s = serializers.IntegerField(required=False, allow_null=True)
    requires_m2_slot = serializers.BooleanField(required=False, allow_null=True)
    requires_sata_port = serializers.BooleanField(required=False, allow_null=True)
    performance_tier = serializers.ChoiceField(
        choices=["low", "mid", "high", "ultra"], required=False, allow_null=True
    )
