# Playbook — Módulo 2: Monetización de la landing (repetible por producto)

> Continuación de `playbook-clonar-landing.md`. Estado 2026-07-24: máquina montada, pendiente activar cuando Esteban decida publicar.

## Decisión tomada (2026-07-24)
- **Fase corta (validar):** Hotmart — cobra en todo Latam con métodos locales por país (CO: PSE/Nequi/Efecty · MX: OXXO/SPEI · AR: Mercado Pago · PE: Yape · CL: MACH · BR: PIX · resto: tarjetas/PayPal) y ENTREGA el material automáticamente. Sin mensualidad, comisión ~10%.
- **Fase larga (escalar):** dLocal Go — la de mayor cobertura (13 países Latam con métodos locales + tarjetas internacionales, sin mensualidad, ~3-4%). Requiere KYB de comercio. El sistema propio (checkout+webhook+entrega) lo construye el Lab cuando aprueben el KYB.

## Receta Hotmart por producto (probada hoy con "Multi Consola", ID 8189092, quedó en Draft)
1. Panel → Productos → Registrar producto. Tipo: eBook (o Curso). Nombre EXACTO como en la landing (consistencia = confianza). Precio en USD (Hotmart convierte a moneda local del comprador). Garantía: 7 días (calza con la de la página).
2. **Product Content (dice Optional pero es LA ENTREGA):** subir el PDF de entrega → contiene: bienvenida + link de descarga (Mega) + instrucciones de instalación + requisitos + contacto de soporte. Sin esto, se cobra y no se entrega nada.
   - El PDF de entrega se genera con la plantilla de marca (negro/verde) — pedirlo a Cowork o al Lab con: link de Mega, contacto de soporte, pasos especiales.
3. Submit Product → revisión de Hotmart (horas). Producto aprobado → Promotional links → link de checkout `pay.hotmart.com/XXXX`.
4. Pegar el link en `LINKS_DE_PAGO` (bloque config en scripts/construir.py, clave `principal`; bonos = b0..b5, gold-pc, gold-mob) → push → el robot reconstruye y publica.
5. Validar: compra de prueba (o sandbox) → el botón de la landing abre el checkout Hotmart → al pagar llega el PDF.

## Estado por activar (checklist del día del lanzamiento)
- [ ] Producto Hotmart: completar Product Content (PDF de entrega) + Submit
- [ ] Pegar link de checkout en LINKS_DE_PAGO y republicar
- [ ] Compra de prueba end-to-end
- [ ] (Paralelo) Aplicar KYB en dlocalgo.com para la fase larga
- [ ] (Futuro) Encargo a la Fábrica: sistema propio de pagos (endpoint checkout dLocal + webhook + email de entrega automático) — spec pendiente
- [ ] (Futuro) Migrar dominio consolaultimate.shop a Pages al cancelar Shopify
- [ ] (Futuro) Subir los 6 videos a canal de YouTube propio y cambiar IDs

## Nota
La landing publicada funciona ya con los botones en modo seguro: si LINKS_DE_PAGO está vacío, el botón avisa "Configura tu link de pago" en vez de romperse. La página puede vivir publicada sin vender hasta que se active el checkout.
