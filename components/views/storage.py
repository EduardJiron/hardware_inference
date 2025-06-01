from rest_framework import generics
from ..models.storage import Storage
from ..serializers.storage import StorageInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.storage import StorageSerializer
from ..utils.storage import probability_storages

class StorageInferenceView(APIView):
    def post(self, request):
        serializer = StorageInferenceInputSerializer(data=request.data)
        if serializer.is_valid():
            criteria = serializer.validated_data
            storages = Storage.objects.all()

            scored_storages = []
            for storage in storages:
                prob, explanation = probability_storages(storage, criteria)
                if prob > 0.05:  # filtro mínimo para recomendaciones relevantes
                    scored_storages.append((storage, prob, explanation))

            scored_storages.sort(key=lambda x: x[1], reverse=True)
            top_storages = scored_storages[:3]

            results = []
            for storage, prob, explanation in top_storages:
                storage_data = StorageSerializer(storage).data
                storage_data["probability"] = round(prob, 3)
                storage_data["explanation"] = explanation
                results.append(storage_data)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)