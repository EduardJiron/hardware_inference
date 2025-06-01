def probability_power_supply(psu, criteria):
    score = 0
    explanation = []

    # Propósito (peso fuerte)
    if criteria.get("purpose"):
        if psu.purpose == criteria["purpose"]:
            score += 0.25
            explanation.append("✔️ Propósito adecuado para el uso esperado.")
        else:
            explanation.append(f"❌ Propósito diferente: se esperaba '{criteria['purpose']}', pero esta PSU es para '{psu.purpose}'.")
    else:
        explanation.append("ℹ️ No se especificó el propósito.")

    # Precio (peso fuerte)
    if criteria.get("max_price_usd") is not None:
        price = float(psu.price_usd)
        if price <= criteria["max_price_usd"]:
            score += 0.2
            explanation.append(f"✔️ Precio dentro del presupuesto (${price} <= ${criteria['max_price_usd']}).")
        else:
            explanation.append(f"❌ Precio fuera del presupuesto (${price} > ${criteria['max_price_usd']}).")
    else:
        explanation.append("ℹ️ No se especificó el presupuesto máximo.")

    # Potencia (peso medio)
    if criteria.get("wattage") is not None:
        if psu.wattage >= criteria["wattage"]:
            score += 0.15
            explanation.append(f"✔️ Potencia suficiente ({psu.wattage}W >= {criteria['wattage']}W).")
        else:
            explanation.append(f"❌ Potencia insuficiente ({psu.wattage}W < {criteria['wattage']}W).")
    else:
        explanation.append("ℹ️ No se especificó un mínimo de potencia.")

    # Modularidad (peso leve)
    if criteria.get("modular"):
        if psu.modular == criteria["modular"]:
            score += 0.1
            explanation.append("✔️ Tipo de modularidad coincide con el requerido.")
        else:
            explanation.append(f"⚠️ Tipo de modularidad diferente: se esperaba '{criteria['modular']}', pero es '{psu.modular}'.")
    else:
        explanation.append("ℹ️ No se especificó el tipo de modularidad.")

    # Eficiencia (peso leve)
    if criteria.get("efficiency_rating"):
        if psu.efficiency_rating == criteria["efficiency_rating"]:
            score += 0.1
            explanation.append("✔️ Eficiencia energética coincide con lo esperado.")
        else:
            explanation.append(f"⚠️ Eficiencia energética diferente: se esperaba '{criteria['efficiency_rating']}', pero es '{psu.efficiency_rating}'.")
    else:
        explanation.append("ℹ️ No se especificó nivel de eficiencia.")

    # Form Factor (peso leve)
    if criteria.get("form_factor"):
        if psu.form_factor == criteria["form_factor"]:
            score += 0.1
            explanation.append("✔️ Form factor compatible.")
        else:
            explanation.append(f"⚠️ Form factor diferente: se esperaba '{criteria['form_factor']}', pero es '{psu.form_factor}'.")
    else:
        explanation.append("ℹ️ No se especificó el form factor.")

    # Performance tier (peso leve)
    tier_map = {"low": 0, "mid": 1, "high": 2, "ultra": 3}
    if criteria.get("performance_tier"):
        expected = tier_map.get(criteria["performance_tier"], 1)
        actual = tier_map.get(psu.performance_tier, 1)
        diff = abs(expected - actual)

        if diff == 0:
            score += 0.1
            explanation.append("✔️ Nivel de rendimiento coincide con lo esperado.")
        elif diff == 1:
            score += 0.05
            explanation.append("⚠️ Nivel de rendimiento aceptable.")
        else:
            explanation.append(f"❌ Nivel de rendimiento inadecuado: se esperaba '{criteria['performance_tier']}', pero es '{psu.performance_tier}'.")
    else:
        explanation.append("ℹ️ No se especificó el nivel de rendimiento.")

    return round(score, 2), explanation
