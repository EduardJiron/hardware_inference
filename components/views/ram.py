from rest_framework import generics
from ..models.ram import RAM
from ..serializers.ram import RAMInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.ram import RAMSerializer
from ..utils.ram import probability_rams

class RAMInferenceView(APIView):
    def post(self, request):
        serializer = RAMInferenceInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        criteria = serializer.validated_data

        results = []
        for ram in RAM.objects.all():
            score, explanation = probability_rams(ram, criteria)
            results.append({
                "id": ram.id,
                "model": ram.model,
                "capacity_gb": ram.capacity_gb,
                "modules": ram.modules,
                "speed_mhz": ram.speed_mhz,
                "type": ram.type,
                "ecc": ram.ecc,
                "rgb": ram.rgb,
                "price_usd": float(ram.price_usd),
                "voltage": ram.voltage,
                "form_factor": ram.form_factor,
                "purpose": ram.purpose,
                "performance_tier": ram.performance_tier,
                "probability": score,
                "explanation": explanation
            })

        # Ordenar por probabilidad descendente y limitar a 3 resultados
        top_3 = sorted(results, key=lambda x: x["probability"], reverse=True)[:3]

        return Response(top_3, status=status.HTTP_200_OK)