# ORDEN — Fábrica de landings (proyecto Consola Ultimate → cuenta tiendas)

Claw, orden de Esteban con GO explícito. Lee completo antes de mover un dedo.

## Contexto (30 segundos)
Hoy (2026-07-24) cloné con Cowork la landing de consolaultimate.shop (Shopify) y quedó
standalone y publicada gratis en GitHub Pages: https://wheducation.github.io/consola-ultimate/
El pipeline completo (3 scripts + workflow) quedó como plantilla reutilizable en el repo
PÚBLICO `wheducation/consola-ultimate` — lo puedes clonar sin credenciales.
Playbook con arquitectura + 9 errores reales documentados:
https://github.com/wheducation/consola-ultimate/blob/main/docs/playbook-clonar-landing.md

## Objetivo
Que TÚ (dirigiendo al Lab) puedas repetir esto para cualquier landing, usando una
CUENTA NUEVA de GitHub ("cuenta tiendas") separada del laboratorio, por seguridad.

## Frenos que SÍ aplican (Carta de Autonomía)
- La CUENTA NUEVA la creo YO (Esteban): registro, verificación de email (crítico: sin
  verificar, Actions queda en Queued eterno), 2FA, y el fine-grained PAT (solo repos de
  tiendas, permisos Contents+Pages+Workflows RW). Yo te aviso cuando el token esté en
  el .env del lab como GH_TIENDAS_TOKEN. NO me pidas el token por chat, NUNCA va a memoria.
- Publicar en la cuenta nueva = salida al mundo → este documento ES el GO para este
  proyecto específico (landings de mis tiendas). Cualquier otra publicación fuera de
  este alcance = freno normal, me preguntas.
- Cero gasto de plata: todo el stack es gratis (GitHub free + Pages). Si algo pide
  tarjeta, freno y me avisas.

## Fases (pre-partidas, anti-monolito — cada pieza <10 min de motor)
FASE 0 (tú solo, sin Lab): clonar `wheducation/consola-ultimate` a
  /opt/dispatch/data/tiendas/plantilla/ (es DATO/combustible, NO va al vault).
  Leer docs/playbook-clonar-landing.md y guardar con REMEMBER un resumen de 5 líneas
  (proyecto claw, tipo=aprendizaje).
FASE 1 (cuando yo avise que el PAT existe): probar credencial — crear repo de prueba
  en la cuenta tiendas vía API, push de un README, borrar el repo. Reportar OK/fallo
  con el mensaje real (fail-loud).
FASE 2: migrar consola-ultimate → pedirme la transferencia del repo (Settings→Transfer,
  la hago yo en 1 min) O re-push completo a un repo nuevo de la cuenta tiendas.
  Después: yo activo Pages (Settings→Pages→Source: GitHub Actions, una vez) y tú
  disparas workflow_dispatch y validas con el snippet del playbook
  (esperado: rotas 0, externas 0).
FASE 3 (por cada landing nueva que yo te encargue): pieza A = manifiesto de assets
  (crawl de la página, lista nombre+URL, verificar contra el playbook los 2 CDNs y las
  URLs //). pieza B = correr descargar+procesar+construir LOCAL en el lab y revisar
  el index.html contra la reja (checkout fuera, scripts de terceros fuera,
  LINKS_DE_PAGO presente). pieza C = repo nuevo + push + avisarme para el clic de
  Pages + validación final. Cada pieza es una orden separada al Lab si la delegas.

## Reja de calidad (por landing, antes de darla por terminada)
1. 0 imágenes rotas y 0 imágenes cargando de dominios del sitio original (snippet del playbook).
2. Botones de compra → LINKS_DE_PAGO (nada de cart/add del original).
3. 0 scripts de analytics/pixels de terceros en el index.html final.
4. La página abre y se ve idéntica a la original (comparación visual).
5. Digest a Esteban con: URL publicada, conteos de la validación, y qué falta (links de pago, dominio).

## Memoria
Al terminar cada fase: REMEMBER (proyecto claw, tipo=hecho) con qué quedó y dónde.
Al vault SOLO el digest operativo — el crudo (HTML, imágenes, manifiestos) vive en
/opt/dispatch/data/tiendas/.

— Esteban (vía Cowork, 2026-07-24)
