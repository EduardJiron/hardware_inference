def probability_motherboard(mb, criteria):
    score = 0
    explanation = []

    def safe_lower(val):
        return val.strip().lower() if isinstance(val, str) else val

    # Propósito
    if safe_lower(criteria.get("purpose")) == safe_lower(mb.purpose):
        score += 0.25
        explanation.append("✔️ Propósito adecuado para el uso esperado.")
    elif criteria.get("purpose"):
        explanation.append(
            f"❌ Propósito diferente: se esperaba '{criteria['purpose']}', pero esta motherboard es para '{mb.purpose}'."
        )
    else:
        explanation.append("ℹ️ No se especificó propósito.")

    # Precio
    max_price = criteria.get("max_price_usd")
    if max_price is not None:
        if float(mb.price_usd) <= max_price:
            score += 0.2
            explanation.append(f"✔️ Precio dentro del presupuesto (${mb.price_usd} <= ${max_price}).")
        else:
            explanation.append(f"❌ Precio fuera del presupuesto (${mb.price_usd} > ${max_price}).")
    else:
        explanation.append("ℹ️ No se especificó presupuesto máximo.")

    # Socket
    if safe_lower(criteria.get("socket_type")) == safe_lower(mb.socket_type):
        score += 0.15
        explanation.append("✔️ Compatible con el socket requerido.")
    elif criteria.get("socket_type"):
        explanation.append(f"❌ Socket incompatible: se necesita '{criteria['socket_type']}', pero tiene '{mb.socket_type}'.")
    else:
        explanation.append("ℹ️ No se especificó socket requerido.")

    # Chipset
    if safe_lower(criteria.get("chipset")) == safe_lower(mb.chipset):
        score += 0.1
        explanation.append("✔️ Chipset compatible.")
    elif criteria.get("chipset"):
        explanation.append(f"❌ Chipset incompatible: se esperaba '{criteria['chipset']}', pero tiene '{mb.chipset}'.")
    else:
        explanation.append("ℹ️ No se especificó chipset requerido.")

    # Form factor
    if safe_lower(criteria.get("form_factor")) == safe_lower(mb.form_factor):
        score += 0.05
        explanation.append("✔️ Factor de forma compatible.")
    elif criteria.get("form_factor"):
        explanation.append(f"❌ Factor de forma incompatible: se esperaba '{criteria['form_factor']}', pero tiene '{mb.form_factor}'.")
    else:
        explanation.append("ℹ️ No se especificó factor de forma requerido.")

    # Tipo de memoria
    mem_type = criteria.get("supported_memory_type")
    if mem_type:
        if mem_type in mb.supported_memory_types:
            score += 0.1
            explanation.append(f"✔️ Soporta el tipo de memoria requerido ({mem_type}).")
        else:
            explanation.append(f"❌ No soporta el tipo de memoria '{mem_type}'.")
    else:
        explanation.append("ℹ️ No se especificó tipo de memoria.")

    # Memoria máxima
    min_mem = criteria.get("min_max_memory_gb")
    if min_mem is not None:
        if mb.max_memory_gb >= min_mem:
            score += 0.05
            explanation.append(f"✔️ Capacidad máxima de memoria suficiente ({mb.max_memory_gb} GB).")
        else:
            explanation.append(f"❌ Capacidad máxima insuficiente ({mb.max_memory_gb} GB < {min_mem} GB).")
    else:
        explanation.append("ℹ️ No se especificó capacidad máxima de memoria requerida.")

    # Slots RAM
    min_slots = criteria.get("min_memory_slots")
    if min_slots is not None:
        if mb.memory_slots >= min_slots:
            score += 0.05
            explanation.append(f"✔️ Tiene al menos {min_slots} slots de RAM.")
        else:
            explanation.append(f"❌ Solo tiene {mb.memory_slots} slots, se esperaban al menos {min_slots}.")
    else:
        explanation.append("ℹ️ No se especificó número mínimo de slots de RAM.")

    # PCI Express
    min_pci = criteria.get("pci_express_slots")
    if min_pci is not None:
        if mb.pci_express_slots >= min_pci:
            score += 0.03
            explanation.append(f"✔️ Tiene al menos {min_pci} ranuras PCI Express.")
        else:
            explanation.append(f"❌ Solo tiene {mb.pci_express_slots} ranuras PCIe, se esperaban al menos {min_pci}.")
    else:
        explanation.append("ℹ️ No se especificó número de ranuras PCI Express.")

    # M.2 slots
    min_m2 = criteria.get("m2_slots")
    if min_m2 is not None:
        if mb.m2_slots >= min_m2:
            score += 0.03
            explanation.append(f"✔️ Tiene al menos {min_m2} ranuras M.2.")
        else:
            explanation.append(f"❌ Solo tiene {mb.m2_slots} ranuras M.2, se esperaban al menos {min_m2}.")
    else:
        explanation.append("ℹ️ No se especificó número mínimo de ranuras M.2.")

    # SATA
    min_sata = criteria.get("sata_ports")
    if min_sata is not None:
        if mb.sata_ports >= min_sata:
            score += 0.03
            explanation.append(f"✔️ Tiene al menos {min_sata} puertos SATA.")
        else:
            explanation.append(f"❌ Solo tiene {mb.sata_ports} puertos SATA, se esperaban al menos {min_sata}.")
    else:
        explanation.append("ℹ️ No se especificó número mínimo de puertos SATA.")

    # WiFi integrada
    if criteria.get("integrated_wifi_required"):
        if mb.integrated_wifi:
            score += 0.05
            explanation.append("✔️ Tiene WiFi integrada.")
        else:
            explanation.append("❌ Se requiere WiFi integrada, pero no la tiene.")
    else:
        explanation.append("ℹ️ No se requiere WiFi integrada.")

    # Audio integrado
    if criteria.get("integrated_audio_required"):
        if mb.integrated_audio:
            score += 0.05
            explanation.append("✔️ Tiene audio integrado.")
        else:
            explanation.append("❌ Se requiere audio integrado, pero no lo tiene.")
    else:
        explanation.append("ℹ️ No se requiere audio integrado.")

    # CPU tier
    cpu_tier = criteria.get("supported_cpu_tier")
    if cpu_tier:
        if safe_lower(cpu_tier) == safe_lower(mb.supported_cpu_tiers):
            score += 0.05
            explanation.append("✔️ Compatible con el nivel de CPU esperado.")
        else:
            explanation.append(f"❌ CPU tier incompatible: esperado '{cpu_tier}', pero tiene '{mb.supported_cpu_tiers}'.")
    else:
        explanation.append("ℹ️ No se especificó CPU tier esperado.")

    return round(score, 2), explanation
