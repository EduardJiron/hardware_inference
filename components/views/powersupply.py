from rest_framework import generics
from ..models.powersupply import PowerSupply
from ..serializers.powersupply import PowerSupplyInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.powersupply import PowerSupplySerializer
from ..utils.powersupply import probability_power_supply

class PowerSupplyInferenceView(APIView):
    def post(self, request):
        serializer = PowerSupplyInferenceInputSerializer(data=request.data)
        if serializer.is_valid():
            criteria = serializer.validated_data
            powersupplys = PowerSupply.objects.all()

            scored_powersupplys = []
            for powersupply in powersupplys:
                prob, explanation = probability_power_supply(powersupply, criteria)
                if prob > 0.05:  # filtro mínimo para recomendaciones relevantes
                    scored_powersupplys.append((powersupply, prob, explanation))

            scored_powersupplys.sort(key=lambda x: x[1], reverse=True)
            top_powersupplys = scored_powersupplys[:3]

            results = []
            for powersupply, prob, explanation in top_powersupplys:
                powersupply_data = PowerSupplySerializer(powersupply).data
                powersupply_data["probability"] = round(prob, 3)
                powersupply_data["explanation"] = explanation
                results.append(powersupply_data)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
