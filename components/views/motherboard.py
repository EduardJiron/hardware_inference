from rest_framework import generics
from ..models.motherboard import Motherboard
from ..serializers.motherboard import MotherboardInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.motherboard import MotherboardSerializer
from ..utils.motherboard import probability_motherboard

class MotherboardInferenceView(APIView):
    def post(self, request):
        serializer = MotherboardInferenceInputSerializer(data=request.data)
        if serializer.is_valid():
            criteria = serializer.validated_data
            motherboards = Motherboard.objects.all()

            scored_motherboards = []
            for motherboard in motherboards:
                prob, explanation = probability_motherboard(motherboard, criteria)
                if prob > 0.05:  # filtro mínimo para recomendaciones relevantes
                    scored_motherboards.append((motherboard, prob, explanation))

            scored_motherboards.sort(key=lambda x: x[1], reverse=True)
            top_motherboards = scored_motherboards[:3]

            results = []
            for motherboard, prob, explanation in top_motherboards:
                motherboard_data = MotherboardSerializer(motherboard).data
                motherboard_data["probability"] = round(prob, 3)
                motherboard_data["explanation"] = explanation
                results.append(motherboard_data)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
