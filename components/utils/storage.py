def probability_storages(storage, criteria):
    score = 0
    explanation = []

    # Propósito
    if storage.purpose == criteria["purpose"]:
        score += 0.25
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    else:
        explanation.append(f"❌ Propósito diferente: se esperaba '{criteria['purpose']}', pero este dispositivo es para '{storage.purpose}'.")

    # Precio
    if storage.price_usd <= criteria["max_price_usd"]:
        score += 0.2
        explanation.append(f"✔️ Precio dentro del presupuesto (${storage.price_usd} <= ${criteria['max_price_usd']}).")
    else:
        explanation.append(f"❌ Precio fuera del presupuesto (${storage.price_usd} > ${criteria['max_price_usd']}).")

    # Tipo (SSD, HDD, etc.)
    if "type" in criteria and criteria["type"]:
        if storage.type.lower() == criteria["type"].lower():
            score += 0.1
            explanation.append("✔️ Tipo de almacenamiento coincide con lo esperado.")
        else:
            explanation.append(f"❌ Tipo diferente: se esperaba '{criteria['type']}', pero tiene '{storage.type}'.")
    else:
        explanation.append("ℹ️ No se especificó el tipo de almacenamiento.")

    # Interfaz
    if "interface" in criteria and criteria["interface"]:
        if storage.interface.lower() == criteria["interface"].lower():
            score += 0.1
            explanation.append("✔️ Interfaz de conexión compatible.")
        else:
            explanation.append(f"❌ Interfaz diferente: se esperaba '{criteria['interface']}', pero tiene '{storage.interface}'.")
    else:
        explanation.append("ℹ️ No se especificó interfaz de conexión.")

    # Form Factor
    if "form_factor" in criteria and criteria["form_factor"]:
        if storage.form_factor.lower() == criteria["form_factor"].lower():
            score += 0.05
            explanation.append("✔️ Factor de forma compatible.")
        else:
            explanation.append(f"❌ Factor de forma diferente: se esperaba '{criteria['form_factor']}', pero es '{storage.form_factor}'.")
    else:
        explanation.append("ℹ️ No se especificó factor de forma.")

    # Capacidad
    if "capacity_gb" in criteria and criteria["capacity_gb"] is not None:
        cap_diff = abs(storage.capacity_gb - criteria["capacity_gb"])
        if cap_diff <= 50:
            score += 0.05
            explanation.append("✔️ Capacidad muy cercana a lo requerido.")
        elif cap_diff <= 200:
            score += 0.03
            explanation.append("⚠️ Capacidad aceptable, aunque no ideal.")
        else:
            explanation.append(f"❌ Gran diferencia en capacidad (esperado {criteria['capacity_gb']} GB, tiene {storage.capacity_gb} GB).")
    else:
        explanation.append("ℹ️ No se especificó capacidad de almacenamiento.")

    # Velocidad de lectura
    if "read_speed_mb_s" in criteria and criteria["read_speed_mb_s"] is not None:
        if storage.read_speed_mb_s >= criteria["read_speed_mb_s"]:
            score += 0.05
            explanation.append("✔️ Velocidad de lectura adecuada o superior.")
        else:
            explanation.append(f"❌ Velocidad de lectura insuficiente ({storage.read_speed_mb_s} < {criteria['read_speed_mb_s']} MB/s).")
    else:
        explanation.append("ℹ️ No se especificó velocidad de lectura.")

    # Velocidad de escritura
    if "write_speed_mb_s" in criteria and criteria["write_speed_mb_s"] is not None:
        if storage.write_speed_mb_s >= criteria["write_speed_mb_s"]:
            score += 0.05
            explanation.append("✔️ Velocidad de escritura adecuada o superior.")
        else:
            explanation.append(f"❌ Velocidad de escritura insuficiente ({storage.write_speed_mb_s} < {criteria['write_speed_mb_s']} MB/s).")
    else:
        explanation.append("ℹ️ No se especificó velocidad de escritura.")

    # Requiere M.2
    if "requires_m2_slot" in criteria and criteria["requires_m2_slot"] is not None:
        if criteria["requires_m2_slot"]:
            if storage.requires_m2_slot:
                score += 0.05
                explanation.append("✔️ Usa slot M.2, como se requiere.")
            else:
                explanation.append("❌ Se requiere slot M.2, pero este dispositivo no lo utiliza.")
        else:
            score += 0.02
            explanation.append("✔️ No se requiere M.2, cumple con el criterio.")
    else:
        explanation.append("ℹ️ No se indicó si se requiere M.2.")

    # Requiere SATA
    if "requires_sata_port" in criteria and criteria["requires_sata_port"] is not None:
        if criteria["requires_sata_port"]:
            if storage.requires_sata_port:
                score += 0.05
                explanation.append("✔️ Usa puerto SATA, como se requiere.")
            else:
                explanation.append("❌ Se requiere puerto SATA, pero este dispositivo no lo utiliza.")
        else:
            score += 0.02
            explanation.append("✔️ No se requiere puerto SATA, cumple con el criterio.")
    else:
        explanation.append("ℹ️ No se indicó si se requiere puerto SATA.")

    # Performance Tier
    if "performance_tier" in criteria and criteria["performance_tier"]:
        perf_levels = {"low": 0, "mid": 1, "high": 2, "ultra": 3}
        requested = perf_levels.get(criteria["performance_tier"], 1)
        actual = perf_levels.get(storage.performance_tier, 1)
        diff = abs(requested - actual)

        if diff == 0:
            score += 0.05
            explanation.append("✔️ Nivel de rendimiento coincide con lo esperado.")
        elif diff == 1:
            score += 0.03
            explanation.append("⚠️ Nivel de rendimiento aceptable.")
        else:
            explanation.append("❌ Nivel de rendimiento alejado del esperado.")
    else:
        explanation.append("ℹ️ No se especificó el nivel de rendimiento.")

    return round(score, 2), explanation
