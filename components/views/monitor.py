from rest_framework import generics
from ..models.monitor import Monitor
from ..serializers.monitor import MonitorInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.monitor import MonitorSerializer
from ..utils.monitor import probability_monitors

class MonitorInferenceView(APIView):
    def post(self, request):
        serializer = MonitorInferenceInputSerializer(data=request.data)
        if serializer.is_valid():
            criteria = serializer.validated_data
            monitors = Monitor.objects.all()

            scored_monitors = []
            for monitor in monitors:
                prob, explanation = probability_monitors(monitor, criteria)
                if prob > 0.05:  # filtro mínimo para recomendaciones relevantes
                    scored_monitors.append((monitor, prob, explanation))

            scored_monitors.sort(key=lambda x: x[1], reverse=True)
            top_monitors = scored_monitors[:3]

            results = []
            for monitor, prob, explanation in top_monitors:
                monitor_data = MonitorSerializer(monitor).data
                monitor_data["probability"] = round(prob, 3)
                monitor_data["explanation"] = explanation
                results.append(monitor_data)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)