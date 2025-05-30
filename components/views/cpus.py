from rest_framework import generics
from ..models.cpu import CPU
from ..serializers.cpu import CPUInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.cpu import CPUSerializer
from ..utils.cpu import probability_cpus
from .models import  GPU,  Storage, Motherboard, PowerSupply, Cooler, Case
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

def probability_ram(ram, criteria):
    score = 0
    explanation = []

    # Propósito
    if ram.purpose == criteria["purpose"]:
        score += 0.2
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    else:
        explanation.append(f"❌ Propósito diferente: se esperaba '{criteria['purpose']}', pero esta RAM es para '{ram.purpose}'.")

    # Nivel de performance
    perf_levels = {"low": 0, "mid": 1, "high": 2, "ultra": 3}
    requested_level = perf_levels.get(criteria["performance_tier"], 1)
    ram_level = perf_levels.get(ram.performance_tier, 1)
    diff = abs(ram_level - requested_level)

    if diff == 0:
        score += 0.15
        explanation.append("✔️ Nivel de rendimiento coincide con lo esperado.")
    elif diff == 1:
        score += 0.1
        explanation.append("⚠️ Nivel de rendimiento aceptable.")
    else:
        explanation.append("❌ Nivel de rendimiento alejado del requerido.")

    # Precio
    if ram.price_usd <= criteria["max_price_usd"]:
        score += 0.15
        explanation.append(f"✔️ Precio dentro del presupuesto (${ram.price_usd} <= ${criteria['max_price_usd']}).")
    else:
        explanation.append(f"❌ Precio fuera del presupuesto (${ram.price_usd} > ${criteria['max_price_usd']}).")

    # Capacidad
    if "capacity_gb" in criteria and criteria["capacity_gb"] is not None:
        cap_diff = abs(ram.capacity_gb - criteria["capacity_gb"])
        if cap_diff == 0:
            score += 0.1
            explanation.append("✔️ Capacidad exacta requerida.")
        elif cap_diff <= 4:
            score += 0.07
            explanation.append(f"⚠️ Capacidad cercana (diferencia de {cap_diff} GB).")
        else:
            explanation.append(f"❌ Diferencia considerable en capacidad (esperado {criteria['capacity_gb']} GB, tiene {ram.capacity_gb} GB).")
    else:
        explanation.append("ℹ️ No se especificó capacidad en el criterio.")

    # Tipo de memoria (DDR4/DDR5)
    if ram.type == criteria["type"]:
        score += 0.1
        explanation.append(f"✔️ Tipo de memoria compatible ({criteria['type']}).")
    else:
        explanation.append(f"❌ Tipo de memoria incompatible: se esperaba {criteria['type']}, pero tiene {ram.type}.")

    # ECC
    if criteria.get("ecc_required", False):
        if ram.ecc:
            score += 0.05
            explanation.append("✔️ Incluye ECC, como se requiere.")
        else:
            explanation.append("❌ Se requiere ECC, pero la memoria no lo incluye.")
    else:
        score += 0.02  # No penaliza
        explanation.append("✔️ No se requiere ECC, cumple con el criterio.")

    # RGB
    if criteria.get("rgb_required", False):
        if ram.rgb:
            score += 0.03
            explanation.append("✔️ Tiene RGB, como se requiere.")
        else:
            explanation.append("❌ Se requiere RGB, pero no lo tiene.")
    else:
        score += 0.01
        explanation.append("✔️ No se requiere RGB, cumple con el criterio.")

    # Form Factor
    if "form_factor" in criteria and criteria["form_factor"] is not None:
        if ram.form_factor == criteria["form_factor"]:
            score += 0.05
            explanation.append("✔️ Factor de forma compatible.")
        else:
            explanation.append(f"❌ Incompatibilidad en factor de forma (esperado {criteria['form_factor']}, tiene {ram.form_factor}).")
    else:
        explanation.append("ℹ️ No se especificó factor de forma.")

    # Velocidad (MHz)
    if "speed_mhz" in criteria and criteria["speed_mhz"] is not None:
        speed_diff = abs(ram.speed_mhz - criteria["speed_mhz"])
        if speed_diff <= 200:
            score += 0.05
            explanation.append("✔️ Velocidad muy cercana a la requerida.")
        elif speed_diff <= 500:
            score += 0.03
            explanation.append("⚠️ Velocidad razonablemente cercana.")
        else:
            explanation.append(f"❌ Gran diferencia en velocidad (esperado {criteria['speed_mhz']} MHz, tiene {ram.speed_mhz} MHz).")
    else:
        explanation.append("ℹ️ No se especificó velocidad.")

    return round(score, 2), explanation

class RAMInferenceView(APIView):
    def post(self, request):
        serializer = RAMInferenceInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        criteria = serializer.validated_data

        results = []
        for ram in RAM.objects.all():
            score, explanation = probability_ram(ram, criteria)
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