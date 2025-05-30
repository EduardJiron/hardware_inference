from rest_framework import generics
from ..models.cpu import CPU
from ..serializers.cpu import CPUInferenceInputSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.cpu import CPUSerializer


def probability_cpus(cpu, criteria):
    score = 0
    explanation = []

    # Propósito (peso fuerte)
    if cpu.purpose == criteria["purpose"]:
        score += 0.25
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    else:
        explanation.append(f"❌ Propósito diferente: se esperaba '{criteria['purpose']}', pero este CPU es para '{cpu.purpose}'.")

    # Nivel de performance (peso moderado)
    perf_levels = {"low": 0, "mid": 1, "high": 2, "ultra": 3}
    requested_level = perf_levels.get(criteria["performance_level"], 1)
    cpu_level = perf_levels.get(cpu.performance_level, 1)
    diff = abs(cpu_level - requested_level)

    if diff == 0:
        score += 0.2
        explanation.append("✔️ Nivel de rendimiento coincide con lo esperado.")
    elif diff == 1:
        score += 0.1
        explanation.append("⚠️ Nivel de rendimiento aceptable, aunque no ideal.")
    else:
        explanation.append("❌ Nivel de rendimiento alejado del requerido.")

    # Precio (peso moderado)
    cpu_price = float(cpu.price_usd)
    if cpu_price <= criteria["max_price_usd"]:
        score += 0.15
        explanation.append(f"✔️ Precio dentro del presupuesto (${cpu_price} <= ${criteria['max_price_usd']}).")
    else:
        explanation.append(f"❌ Precio fuera del presupuesto (${cpu_price} > ${criteria['max_price_usd']}).")

    # Socket (peso medio)
    if cpu.socket_type == criteria["socket_type"]:
        score += 0.15
        explanation.append("✔️ Compatible con el socket requerido.")
    else:
        explanation.append(f"❌ Socket incompatible: se necesita '{criteria['socket_type']}', pero tiene '{cpu.socket_type}'.")

    # GPU integrada
    if criteria["integrated_gpu_required"]:
        if cpu.integrated_gpu:
            score += 0.1
            explanation.append("✔️ Incluye GPU integrada, como se requiere.")
        else:
            explanation.append("❌ Se requiere GPU integrada, pero este CPU no la incluye.")
    else:
        score += 0.05  # No penaliza si no se requiere
        explanation.append("✔️ No se requiere GPU integrada, cumple con el criterio.")

    # Tipo de memoria
    if criteria["memory_type"] in cpu.memory_types:
        score += 0.1
        explanation.append(f"✔️ Soporta el tipo de memoria requerido ({criteria['memory_type']}).")
    else:
        explanation.append(f"❌ No es compatible con la memoria '{criteria['memory_type']}'.")

    # Núcleos (peso leve)
    if "cores" in criteria and criteria["cores"] is not None:
        core_diff = abs(cpu.cores - criteria["cores"])
        if core_diff == 0:
            score += 0.05
            explanation.append("✔️ Coincide exactamente con el número de núcleos requerido.")
        elif core_diff <= 2:
            score += 0.03
            explanation.append(f"⚠️ Núcleos similares (diferencia de {core_diff}).")
        else:
            explanation.append(f"❌ Gran diferencia en núcleos requeridos (esperado {criteria['cores']}, tiene {cpu.cores}).")
    else:
        explanation.append("ℹ️ No se especificó número de núcleos en el criterio.")

    # Velocidad de reloj (peso leve)
    if "clock_speed_ghz" in criteria and criteria["clock_speed_ghz"] is not None:
        speed_diff = abs(cpu.clock_speed_ghz - criteria["clock_speed_ghz"])
        if speed_diff < 0.2:
            score += 0.05
            explanation.append("✔️ Velocidad de reloj muy cercana a la deseada.")
        elif speed_diff < 0.5:
            score += 0.03
            explanation.append("⚠️ Velocidad de reloj algo menor a la deseada.")
        else:
            explanation.append(f"❌ Velocidad de reloj baja (esperado {criteria['clock_speed_ghz']} GHz, tiene {cpu.clock_speed_ghz} GHz).")
    else:
        explanation.append("ℹ️ No se especificó velocidad de reloj en el criterio.")

    return round(score, 2), explanation
