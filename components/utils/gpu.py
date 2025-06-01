def probability_gpus(gpu, criteria):
    score = 0
    explanation = []

    # Propósito
    if gpu.purpose == criteria["purpose"]:
        score += 0.25
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    else:
        explanation.append(f"❌ Propósito diferente: se esperaba '{criteria['purpose']}', pero esta GPU es para '{gpu.purpose}'.")

    # Precio
    price = float(gpu.price_usd)
    if price <= criteria["max_price_usd"]:
        score += 0.2
        explanation.append(f"✔️ Precio dentro del presupuesto (${price} <= ${criteria['max_price_usd']}).")
    else:
        explanation.append(f"❌ Precio fuera del presupuesto (${price} > ${criteria['max_price_usd']}).")

    # VRAM (opcional)
    if "vram_gb" in criteria and criteria["vram_gb"] is not None:
        vram_diff = abs(gpu.vram_gb - criteria["vram_gb"])
        if vram_diff == 0:
            score += 0.15
            explanation.append("✔️ Coincide exactamente con la VRAM requerida.")
        elif vram_diff <= 2:
            score += 0.1
            explanation.append("⚠️ VRAM similar, aunque no exacta.")
        else:
            explanation.append(f"❌ Diferencia considerable en VRAM (esperado {criteria['vram_gb']}GB, tiene {gpu.vram_gb}GB).")
    else:
        explanation.append("ℹ️ No se especificó la cantidad de VRAM en los criterios del usuario.")

    # Reloj base (opcional)
    if "core_clock_mhz" in criteria and criteria["core_clock_mhz"] is not None:
        core_diff = abs(gpu.core_clock_mhz - criteria["core_clock_mhz"])
        if core_diff < 100:
            score += 0.05
            explanation.append("✔️ Frecuencia base muy cercana a la esperada.")
        elif core_diff < 200:
            score += 0.03
            explanation.append("⚠️ Frecuencia base algo diferente.")
        else:
            explanation.append(f"❌ Diferencia considerable en frecuencia base (esperado {criteria['core_clock_mhz']} MHz, tiene {gpu.core_clock_mhz} MHz).")
    else:
        explanation.append("ℹ️ No se especificó la frecuencia base en los criterios del usuario.")

    # Boost clock (opcional)
    if "boost_clock_mhz" in criteria and criteria["boost_clock_mhz"] is not None:
        boost_diff = abs(gpu.boost_clock_mhz - criteria["boost_clock_mhz"])
        if boost_diff < 100:
            score += 0.05
            explanation.append("✔️ Boost clock muy cercano al esperado.")
        elif boost_diff < 200:
            score += 0.03
            explanation.append("⚠️ Boost clock aceptable.")
        else:
            explanation.append(f"❌ Diferencia considerable en boost clock (esperado {criteria['boost_clock_mhz']} MHz, tiene {gpu.boost_clock_mhz} MHz).")
    else:
        explanation.append("ℹ️ No se especificó el boost clock en los criterios del usuario.")

    # Consumo de energía (opcional)
    if "power_draw_w" in criteria and criteria["power_draw_w"] is not None:
        if gpu.power_draw_w <= criteria["power_draw_w"]:
            score += 0.05
            explanation.append("✔️ Consumo energético dentro del límite esperado.")
        else:
            explanation.append(f"❌ Requiere más energía de la esperada ({gpu.power_draw_w}W > {criteria['power_draw_w']}W).")
    else:
        explanation.append("ℹ️ No se especificó el consumo energético en los criterios del usuario.")

    # Tipo de salida de video (opcional)
    if "video_output_interface" in criteria and criteria["video_output_interface"]:
        matched_outputs = set(gpu.video_output_interface).intersection(set(criteria["video_output_interface"]))
        if matched_outputs:
            score += 0.1
            explanation.append(f"✔️ Compatible con las interfaces requeridas: {list(matched_outputs)}.")
        else:
            explanation.append(f"❌ No tiene ninguna de las interfaces requeridas: {criteria['video_output_interface']}.")
    else:
        explanation.append("ℹ️ No se especificaron interfaces de salida de video en los criterios del usuario.")

    # Nivel de rendimiento (opcional)
    if "performance_tier" in criteria and criteria["performance_tier"] is not None:
        tiers = {"low": 1, "mid": 2, "high": 3, "ultra": 4}
        expected = tiers.get(criteria["performance_tier"], 2)
        actual = tiers.get(gpu.performance_tier, 2)
        diff = abs(expected - actual)

        if diff == 0:
            score += 0.1
            explanation.append("✔️ Nivel de rendimiento coincide con lo esperado.")
        elif diff == 1:
            score += 0.05
            explanation.append("⚠️ Nivel de rendimiento aceptable, aunque diferente.")
        else:
            explanation.append(f"❌ Nivel de rendimiento alejado del requerido: esperado '{criteria['performance_tier']}', tiene '{gpu.performance_tier}'.")
    else:
        explanation.append("ℹ️ No se especificó el nivel de rendimiento en los criterios del usuario.")

    return round(score, 2), explanation
