def probability_monitors(monitor, criteria):
    score = 0
    explanation = []

    # Propósito (obligatorio)
    if monitor.purpose == criteria.get("purpose"):
        score += 0.25
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    else:
        explanation.append(f"❌ Propósito diferente: se esperaba '{criteria.get('purpose')}', pero este monitor es para '{monitor.purpose}'.")

    # Precio (obligatorio)
    price = float(monitor.price_usd)
    max_price = criteria.get("max_price_usd")
    if max_price is not None:
        if price <= max_price:
            score += 0.2
            explanation.append(f"✔️ Precio dentro del presupuesto (${price} <= ${max_price}).")
        else:
            explanation.append(f"❌ Precio fuera del presupuesto (${price} > ${max_price}).")
    else:
        explanation.append("ℹ️ No se especificó presupuesto máximo.")

    # Tamaño de pantalla (opcional)
    size_inches = criteria.get("size_inches")
    if size_inches is not None:
        size_diff = abs(monitor.size_inches - size_inches)
        if size_diff <= 1.0:
            score += 0.15
            explanation.append("✔️ Tamaño de pantalla muy cercano al deseado.")
        elif size_diff <= 2.5:
            score += 0.08
            explanation.append("⚠️ Tamaño aceptable, aunque no ideal.")
        else:
            explanation.append(f"❌ Diferencia considerable en tamaño de pantalla (esperado {size_inches}”, tiene {monitor.size_inches}”).")
    else:
        explanation.append("ℹ️ No se especificó tamaño de pantalla deseado.")

    # Resolución (opcional)
    resolution = criteria.get("resolution")
    if resolution:
        if monitor.resolution == resolution:
            score += 0.1
            explanation.append("✔️ Resolución coincide con la esperada.")
        else:
            explanation.append(f"❌ Resolución diferente: se esperaba '{resolution}', pero es '{monitor.resolution}'.")
    else:
        explanation.append("ℹ️ No se especificó resolución deseada.")

    # Frecuencia de actualización (opcional)
    refresh_rate = criteria.get("refresh_rate_hz")
    if refresh_rate is not None:
        if monitor.refresh_rate_hz >= refresh_rate:
            score += 0.1
            explanation.append("✔️ Frecuencia de actualización adecuada o superior.")
        else:
            explanation.append(f"❌ Frecuencia insuficiente ({monitor.refresh_rate_hz}Hz < {refresh_rate}Hz).")
    else:
        explanation.append("ℹ️ No se especificó frecuencia de actualización deseada.")

    # Tipo de panel (opcional)
    panel_type = criteria.get("panel_type")
    if panel_type:
        if monitor.panel_type.lower() == panel_type.lower():
            score += 0.1
            explanation.append("✔️ Tipo de panel coincide con lo esperado.")
        else:
            explanation.append(f"❌ Tipo de panel diferente: se esperaba '{panel_type}', pero tiene '{monitor.panel_type}'.")
    else:
        explanation.append("ℹ️ No se especificó tipo de panel.")

    # Interfaces de salida de video (opcional)
    video_outputs_req = criteria.get("video_output_interface")
    if video_outputs_req:
        matched_outputs = set(monitor.video_output_interface).intersection(set(video_outputs_req))
        if matched_outputs:
            score += 0.1
            explanation.append(f"✔️ Compatible con las interfaces requeridas: {list(matched_outputs)}.")
        else:
            explanation.append(f"❌ No tiene ninguna de las interfaces requeridas: {video_outputs_req}.")
    else:
        explanation.append("ℹ️ No se especificaron interfaces de video requeridas.")

    return round(score, 2), explanation
