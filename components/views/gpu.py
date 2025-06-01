from rest_framework import generics
from ..models.gpu import GPU
from ..serializers.gpu import GPUInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.gpu import GPUSerializer
from ..utils.gpu import probability_gpus

class GPUInferenceView(APIView):
    def post(self, request):
        serializer = GPUInferenceInputSerializer(data=request.data)
        if serializer.is_valid():
            criteria = serializer.validated_data
            gpus = GPU.objects.all()

            scored_gpus = []
            for gpu in gpus:
                prob, explanation = probability_gpus(gpu, criteria)
                if prob > 0.05:  # filtro mínimo para recomendaciones relevantes
                    scored_gpus.append((gpu, prob, explanation))

            scored_gpus.sort(key=lambda x: x[1], reverse=True)
            top_gpus = scored_gpus[:3]

            results = []
            for gpu, prob, explanation in top_gpus:
                gpu_data = GPUSerializer(gpu).data
                gpu_data["probability"] = round(prob, 3)
                gpu_data["explanation"] = explanation
                results.append(gpu_data)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)