def probability_rams(ram, criteria):
    score = 0
    explanation = []

    # Propósito
    if criteria.get("purpose") and ram.purpose == criteria["purpose"]:
        score += 0.2
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    elif criteria.get("purpose"):
        explanation.append(f"❌ Propósito diferente: se esperaba '{criteria['purpose']}', pero esta RAM es para '{ram.purpose}'.")
    else:
        explanation.append("ℹ️ No se especificó propósito.")

    # Nivel de performance
    perf_levels = {"low": 0, "mid": 1, "high": 2, "ultra": 3}
    requested_level = perf_levels.get(criteria.get("performance_tier"), 1)
    ram_level = perf_levels.get(ram.performance_tier, 1)
    diff = abs(ram_level - requested_level)

    if criteria.get("performance_tier"):
        if diff == 0:
            score += 0.15
            explanation.append("✔️ Nivel de rendimiento coincide con lo esperado.")
        elif diff == 1:
            score += 0.1
            explanation.append("⚠️ Nivel de rendimiento aceptable.")
        else:
            explanation.append("❌ Nivel de rendimiento alejado del requerido.")
    else:
        explanation.append("ℹ️ No se especificó nivel de rendimiento.")

    # Precio
    if criteria.get("max_price_usd") is not None:
        if ram.price_usd <= criteria["max_price_usd"]:
            score += 0.15
            explanation.append(f"✔️ Precio dentro del presupuesto (${ram.price_usd} <= ${criteria['max_price_usd']}).")
        else:
            explanation.append(f"❌ Precio fuera del presupuesto (${ram.price_usd} > ${criteria['max_price_usd']}).")
    else:
        explanation.append("ℹ️ No se especificó presupuesto máximo.")

    # Capacidad
    if criteria.get("capacity_gb") is not None:
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
        explanation.append("ℹ️ No se especificó capacidad.")

    # Tipo de memoria
    if criteria.get("type"):
        if ram.type == criteria["type"]:
            score += 0.1
            explanation.append(f"✔️ Tipo de memoria compatible ({criteria['type']}).")
        else:
            explanation.append(f"❌ Tipo de memoria incompatible: se esperaba {criteria['type']}, pero tiene {ram.type}.")
    else:
        explanation.append("ℹ️ No se especificó tipo de memoria.")

    # ECC
    if criteria.get("ecc_required") is True:
        if ram.ecc:
            score += 0.05
            explanation.append("✔️ Incluye ECC, como se requiere.")
        else:
            explanation.append("❌ Se requiere ECC, pero la memoria no lo incluye.")
    else:
        score += 0.02
        explanation.append("✔️ No se requiere ECC, cumple con el criterio.")

    # RGB
    if criteria.get("rgb_required") is True:
        if ram.rgb:
            score += 0.03
            explanation.append("✔️ Tiene RGB, como se requiere.")
        else:
            explanation.append("❌ Se requiere RGB, pero no lo tiene.")
    else:
        score += 0.01
        explanation.append("✔️ No se requiere RGB, cumple con el criterio.")

    # Form Factor
    if criteria.get("form_factor"):
        if ram.form_factor == criteria["form_factor"]:
            score += 0.05
            explanation.append("✔️ Factor de forma compatible.")
        else:
            explanation.append(f"❌ Incompatibilidad en factor de forma (esperado {criteria['form_factor']}, tiene {ram.form_factor}).")
    else:
        explanation.append("ℹ️ No se especificó factor de forma.")

    # Velocidad (MHz)
    if criteria.get("speed_mhz") is not None:
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
