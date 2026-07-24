# Playbook — Clonar una landing (Shopify u otra) y publicarla gratis en GitHub Pages

> Origen: sesión Cowork 2026-07-24. Caso real: consolaultimate.shop → https://wheducation.github.io/consola-ultimate/
> Repo de referencia con todo el código funcionando: `consola-ultimate` (scripts/ + .github/workflows/desplegar.yml + assets-manifest.txt)

## Resultado del caso real
Landing de Shopify clonada 100% standalone: 211 imágenes propias en el repo, checkout de Shopify reemplazado por links de pago configurables (`LINKS_DE_PAGO` en el `<head>`), sin analytics ni pixels de terceros, hosting gratis en Pages, robot (Actions) que reconstruye la página al tocar `scripts/` o el manifiesto.

## Arquitectura (3 scripts + 1 workflow)
1. **`scripts/descargar.py`** — lee `assets-manifest.txt` (líneas `nombre<TAB>url`) y descarga cada asset a `assets/`. Lista `FORZAR` para los que deben re-descargarse siempre. Parcha `url(./...)` en los CSS del tema.
2. **`scripts/procesar.py`** — retoques de imagen (caso real: logos del carrusel con fondo blanco → fondo negro sólido vía flood-fill desde un anillo de 3px del borde, umbral de luminancia 205, máscara con blur 0.8, compuesto sobre negro, guardar WEBP RGB sin alpha).
3. **`scripts/construir.py`** — descarga el HTML vivo de la página original y lo transforma:
   - elimina TODOS los `<script src>` (Shopify/analytics/apps) y los inline salvo los de la página (lista `KEEP` por marcadores) y JSON-LD
   - elimina cart-notification, predictive-search, modulepreloads, preloads de fuentes del CDN
   - reescribe URLs del CDN → `assets/NOMBRE` (solo si el nombre está en el manifiesto)
   - neutraliza forms de `cart/add`, reemplaza `cuGoCheckout` por apertura de `LINKS_DE_PAGO`/`LINKS_COMBO`
   - inyecta el bloque de configuración de pagos en el `<head>`
   - `sessionStorage` en try/catch; fallback de videos de YouTube cuando `location.protocol === 'file:'`
4. **Workflow** — descargar → procesar → construir → commit de `assets/` + `index.html` → `configure-pages` → `upload-pages-artifact` (path `.`) → `deploy-pages`. Triggers: push a `scripts/**`, `assets-manifest.txt`, workflows; y `workflow_dispatch`.

## Ventaja de Claw sobre la sesión Cowork
Claw tiene shell real con red: puede correr los 3 scripts LOCALMENTE en el server y pushear el resultado (assets binarios incluidos) con `git push` normal. No necesita el paso de Actions para CONSTRUIR (solo para publicar, o ni eso: puede commitear el sitio ya construido y dejar Pages en modo "deploy from branch"). El robot de Actions es opcional: sirve como reconstructor automático y documentación viva.

## Errores reales encontrados (no repetir)
- **Manifiesto incompleto**: se omitieron 2 líneas (ps2/ps3) al transcribir → esas imágenes quedaron apuntando al CDN. Verificar SIEMPRE: `imgs con cdn externo == 0` tras publicar (snippet abajo).
- **URLs protocolo-relativas** `//dominio/...`: el regex debe aceptar `(?:https:)?//`.
- **Query strings variadas** `?v=...&width=...`: consumir `\?[^"'\s\\),]*` completo o quedan pegotes.
- **Múltiples CDNs**: la tienda usaba DOS stores de Shopify (`/1/0806/0207/1291/` y `/1/0715/1137/5955/`) — incluir ambos en el regex.
- **YouTube no reproduce en `file://`** (Error 153). Es restricción de YouTube, no un bug. En hosting funciona. Dejar fallback que abre el video en pestaña nueva si `protocol === 'file:'`.
- **WEBP con alpha dio problemas de decodificación** en algún guardado → para fondos, componer sobre color sólido y guardar RGB.
- **Caché del navegador mezcla versiones** de imágenes al iterar → validar con query de DOM (`naturalWidth`, conteo de srcs externos), no a ojo.
- **GitHub Actions en cuenta nueva**: queda "Queued" para siempre hasta VERIFICAR EL EMAIL de la cuenta. Primer síntoma: "job was not acquired by runner".
- **`configure-pages` con `enablement: true` falla** en cuentas personales ("Resource not accessible by integration") → habilitar Pages UNA vez a mano: Settings → Pages → Source: GitHub Actions.
- **Re-run de un workflow corre sobre el commit viejo** → si el bot ya commiteó encima, hacer run nuevo (`workflow_dispatch`), no re-run. El paso de commit lleva `git pull --rebase || true` por esto.

## Procedimiento con cuenta nueva de GitHub (seguridad)
Objetivo: aislar los sitios públicos de venta de la cuenta del laboratorio (repos privados).
1. **Esteban (humano, ~10 min)**: crear cuenta nueva (email nuevo o alias `+tiendas`), **verificar el email** (crítico para Actions), activar 2FA.
2. **Esteban**: en la cuenta nueva → Settings → Developer settings → Fine-grained personal access token: acceso SOLO a los repos de sitios, permisos Contents (RW) + Pages (RW) + Workflows (RW). Guardarlo en el server como secreto (p. ej. `/opt/dispatch/.env` → `GH_TIENDAS_TOKEN`), NUNCA en un repo.
3. **Claw**: crear repo público del sitio en la cuenta nueva (`gh repo create` con el token o API), clonar la plantilla (los 4 archivos del repo `consola-ultimate`), ajustar `URL` y manifiesto del producto nuevo, correr los 3 scripts localmente, commit + push (con el token de la cuenta nueva como credencial del remoto — no mezclar con las credenciales del lab).
4. **Esteban (1 min)**: Settings → Pages → Source: GitHub Actions (una sola vez por repo).
5. **Claw**: disparar workflow (o pushear ya construido), verificar la URL `usuario.github.io/repo` con el snippet de validación.
6. Migrar `consola-ultimate` del lab a la cuenta nueva: transferencia de repo (Settings → Transfer) o re-push. Después, el dominio propio: Settings → Pages → Custom domain + CNAME en el DNS.

## Snippet de validación post-publicación (consola del navegador)
```js
(() => { const im=[...document.images];
  return { total: im.length,
    rotas: im.filter(i=>i.complete&&i.naturalWidth===0).length,
    externas: im.filter(i=>/cdn\.shopify|consolaultimate\.shop/.test(i.src)).length }; })()
// esperado: rotas: 0, externas: 0
```

## Pendientes del caso real
- `LINKS_DE_PAGO` vacíos: al definir plataforma de pago, editar el bloque en `scripts/construir.py` (sección config) y re-desplegar.
- Los 6 videos son embeds de canales de YouTube AJENOS ("MultiConsola" y "Dynamo Box"). Blindaje: subir copias a un canal propio (no listados) y cambiar los 6 IDs.
- Dominio consolaultimate.shop → apuntar a Pages al cancelar Shopify.

## Nota de seguridad adicional (hallazgo de esta sesión)
En `claw-workspace/TOOLS.md` hay un token Bearer commiteado (API de memoria en 127.0.0.1:8090). Es de loopback (riesgo bajo), pero viola la regla propia "secretos NUNCA aquí" — considerar rotarlo y cargarlo desde el .env.
