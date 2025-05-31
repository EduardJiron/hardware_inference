from rest_framework import generics
from ..models.cpu import CPU
from ..serializers.cpu import CPUInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.cpu import CPUSerializer
from ..utils.cpu import probability_cpus
class CPUInferenceView(APIView):
    def post(self, request):
        serializer = CPUInferenceInputSerializer(data=request.data)
        if serializer.is_valid():
            criteria = serializer.validated_data
            cpus = CPU.objects.all()

            scored_cpus = []
            for cpu in cpus:
                prob, explanation = probability_cpus(cpu, criteria)
                if prob > 0.05:  # filtro mínimo para no recomendar CPUs muy incompatibles
                    scored_cpus.append((cpu, prob, explanation))

            scored_cpus.sort(key=lambda x: x[1], reverse=True)
            top_cpus = scored_cpus[:3]

            # Serializamos CPUs y agregamos explicaciones
            results = []
            for cpu, prob, explanation in top_cpus:
                cpu_data = CPUSerializer(cpu).data
                cpu_data['probability'] = round(prob, 3)
                cpu_data['explanation'] = explanation
                results.append(cpu_data)

            return Response(results, status=200)

        return Response(serializer.errors, status=400)

