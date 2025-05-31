def probability_cpus(cpu, criteria):
    score = 0
    explanation = []

    # Propósito (peso fuerte)
    if criteria.get("purpose") and cpu.purpose == criteria["purpose"]:
        score += 0.25
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    else:
        expected = criteria.get("purpose", "no especificado")
        explanation.append(f"❌ Propósito diferente: se esperaba '{expected}', pero este CPU es para '{cpu.purpose}'.")

    # Nivel de performance (peso moderado)
    perf_levels = {"low": 0, "mid": 1, "high": 2, "ultra": 3}
    requested_level = perf_levels.get(criteria.get("performance_level"), 1)
    cpu_level = perf_levels.get(cpu.performance_level, 1)
    diff = abs(cpu_level - requested_level)

    if criteria.get("performance_level") is not None:
        if diff == 0:
            score += 0.2
            explanation.append("✔️ Nivel de rendimiento coincide con lo esperado.")
        elif diff == 1:
            score += 0.1
            explanation.append("⚠️ Nivel de rendimiento aceptable, aunque no ideal.")
        else:
            explanation.append("❌ Nivel de rendimiento alejado del requerido.")
    else:
        explanation.append("ℹ️ No se especificó nivel de rendimiento en el criterio.")

    # Precio (peso moderado)
    if "max_price_usd" in criteria and criteria["max_price_usd"] is not None:
        cpu_price = float(cpu.price_usd)
        if cpu_price <= criteria["max_price_usd"]:
            score += 0.15
            explanation.append(f"✔️ Precio dentro del presupuesto (${cpu_price} <= ${criteria['max_price_usd']}).")
        else:
            explanation.append(f"❌ Precio fuera del presupuesto (${cpu_price} > ${criteria['max_price_usd']}).")
    else:
        explanation.append("ℹ️ No se especificó presupuesto máximo en el criterio.")

    # Socket (peso medio)
    if criteria.get("socket_type"):
        if cpu.socket_type == criteria["socket_type"]:
            score += 0.15
            explanation.append("✔️ Compatible con el socket requerido.")
        else:
            explanation.append(f"❌ Socket incompatible: se necesita '{criteria['socket_type']}', pero tiene '{cpu.socket_type}'.")
    else:
        explanation.append("ℹ️ No se especificó tipo de socket en el criterio.")

    # GPU integrada
    if criteria.get("integrated_gpu_required") is not None:
        if criteria["integrated_gpu_required"]:
            if cpu.integrated_gpu:
                score += 0.1
                explanation.append("✔️ Incluye GPU integrada, como se requiere.")
            else:
                explanation.append("❌ Se requiere GPU integrada, pero este CPU no la incluye.")
        else:
            score += 0.05  # No penaliza si no se requiere
            explanation.append("✔️ No se requiere GPU integrada, cumple con el criterio.")
    else:
        explanation.append("ℹ️ No se especificó requisito para GPU integrada.")

    # Tipo de memoria
    if criteria.get("memory_type"):
        if criteria["memory_type"] in cpu.memory_types:
            score += 0.1
            explanation.append(f"✔️ Soporta el tipo de memoria requerido ({criteria['memory_type']}).")
        else:
            explanation.append(f"❌ No es compatible con la memoria '{criteria['memory_type']}'.")
    else:
        explanation.append("ℹ️ No se especificó tipo de memoria en el criterio.")

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
