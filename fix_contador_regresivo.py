#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_contador_regresivo.py
"""

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes = 0

# ══ FIX 1: CSS del contador regresivo ══
CSS_COUNTDOWN = """
    /* ============================================================
       CONTADOR REGRESIVO EN OFERTAS
       ============================================================ */
    .prod-countdown {
      display: flex; align-items: center; gap: 6px;
      padding: 6px 16px 8px;
      font-size: .68rem;
    }
    .prod-countdown-label {
      color: var(--accent); font-weight: 700; font-size: .65rem;
      letter-spacing: .06em; text-transform: uppercase;
      display: flex; align-items: center; gap: 4px;
    }
    .prod-countdown-label i { font-size: .62rem; animation: tickPulse 1s ease-in-out infinite; }
    @keyframes tickPulse { 0%,100%{opacity:1} 50%{opacity:.5} }
    .countdown-blocks { display: flex; align-items: center; gap: 4px; }
    .cd-block {
      background: var(--navy); color: var(--sky-light);
      border-radius: 6px; padding: 3px 6px; text-align: center;
      min-width: 32px;
      font-family: var(--font-display); font-weight: 700; font-size: .82rem;
      line-height: 1.2;
    }
    .cd-block span { display: block; font-size: .48rem; font-family: var(--font-body); color: var(--sky); letter-spacing: .06em; text-transform: uppercase; font-weight: 600; }
    .cd-sep { color: var(--accent); font-weight: 700; font-size: .85rem; margin-bottom: 6px; }
"""

OLD_CSS = "  </style>"
if OLD_CSS in idx:
    idx = idx.replace(OLD_CSS, CSS_COUNTDOWN + "\n  </style>", 1)
    print("✅ FIX 1: CSS contador regresivo agregado")
    fixes += 1
else:
    print("⚠️  FIX 1: </style> no encontrado")

# ══ FIX 2: JS del contador regresivo ══
JS_COUNTDOWN = """
/* ════════════════════════════════════════════════════
   CONTADOR REGRESIVO EN OFERTAS
   Calcula tiempo restante hasta medianoche del domingo
   (fin de semana = fin de oferta)
   ════════════════════════════════════════════════════ */
function obtenerFechaFinOferta() {
  /* Buscar en localStorage si hay fecha configurada desde admin */
  try {
    const raw = localStorage.getItem('magama_oferta_fin');
    if (raw) return new Date(raw);
  } catch(e) {}
  /* Por defecto: próximo domingo a medianoche */
  const ahora = new Date();
  const diasHastaDomingo = (7 - ahora.getDay()) % 7 || 7;
  const domingo = new Date(ahora);
  domingo.setDate(ahora.getDate() + diasHastaDomingo);
  domingo.setHours(23, 59, 59, 0);
  return domingo;
}

function calcularCountdown() {
  const fin = obtenerFechaFinOferta();
  const ahora = new Date();
  const diff = Math.max(0, fin - ahora);
  return {
    dias:    Math.floor(diff / (1000 * 60 * 60 * 24)),
    horas:   Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
    minutos: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
    segundos:Math.floor((diff % (1000 * 60)) / 1000),
    activo:  diff > 0,
  };
}

function pad(n) { return n < 10 ? '0' + n : String(n); }

function renderCountdownHTML(cdId) {
  var t = calcularCountdown();
  if (!t.activo) return '';
  var bloques = '';
  if (t.dias > 0) {
    bloques += '<div class="cd-block">' + pad(t.dias) + '<span>días</span></div><span class="cd-sep">:</span>';
  }
  bloques +=
    '<div class="cd-block">' + pad(t.horas)   + '<span>hrs</span></div><span class="cd-sep">:</span>' +
    '<div class="cd-block">' + pad(t.minutos) + '<span>min</span></div><span class="cd-sep">:</span>' +
    '<div class="cd-block" id="cd-sec-' + cdId + '">' + pad(t.segundos) + '<span>seg</span></div>';
  return '<div class="prod-countdown">' +
    '<span class="prod-countdown-label"><i class="fas fa-clock"></i> Oferta termina en:</span>' +
    '<div class="countdown-blocks">' + bloques + '</div>' +
  '</div>';
}

/* Actualizar segundos cada segundo sin re-renderizar toda la tarjeta */
(function iniciarCountdown() {
  setInterval(function() {
    var t = calcularCountdown();
    /* Actualizar solo los bloques de segundos visibles */
    document.querySelectorAll('[id^="cd-sec-"]').forEach(function(el) {
      el.childNodes[0].nodeValue = pad(t.segundos);
    });
    /* Actualizar minutos/horas cuando sea necesario */
    if (t.segundos === 0) {
      /* Re-renderizar todos los contadores completos */
      document.querySelectorAll('.prod-countdown').forEach(function(el, i) {
        var cdId = el.querySelector('[id^="cd-sec-"]');
        if (cdId) {
          var id = cdId.id.replace('cd-sec-', '');
          el.outerHTML = renderCountdownHTML(id);
        }
      });
    }
  }, 1000);
})();

"""

# Insertar antes del Init
OLD_INIT = "/* ── Init ── */\nrenderSkeleton(8);"
if OLD_INIT in idx:
    idx = idx.replace(OLD_INIT, JS_COUNTDOWN + "/* ── Init ── */\nrenderSkeleton(8);", 1)
    print("✅ FIX 2: JS contador regresivo agregado")
    fixes += 1
else:
    # Alternativa
    OLD_INIT2 = "renderSkeleton(8);\nsetTimeout(function() {"
    if OLD_INIT2 in idx:
        idx = idx.replace(OLD_INIT2, JS_COUNTDOWN + "renderSkeleton(8);\nsetTimeout(function() {", 1)
        print("✅ FIX 2b: JS contador regresivo agregado")
        fixes += 1
    else:
        print("⚠️  FIX 2: punto de inserción no encontrado")

# ══ FIX 3: Agregar el contador en las tarjetas de oferta ══
# Buscar el bloque donde se construye mayorHtml en renderProds
# y agregar el countdown después para productos de oferta

OLD_MAYOR = """    const mayorHtml = p.precioMayor
      ? `<div style="font-size:.7rem;color:#06D6A0;font-weight:700;padding:4px 16px 0">Mayor x${p.cantidadMayor||6}+: S/ ${Number(p.precioMayor).toFixed(2)}</div>` : '';"""

NEW_MAYOR = """    const mayorHtml = p.precioMayor
      ? `<div style="font-size:.7rem;color:#06D6A0;font-weight:700;padding:4px 16px 0">Mayor x${p.cantidadMayor||6}+: S/ ${Number(p.precioMayor).toFixed(2)}</div>` : '';
    /* Contador regresivo solo para ofertas */
    const esOferta = badge === 'sale' || cat === 'ofertas';
    const countdownHtml = esOferta ? renderCountdownHTML(p.id) : '';"""

if OLD_MAYOR in idx:
    idx = idx.replace(OLD_MAYOR, NEW_MAYOR, 1)
    print("✅ FIX 3: countdownHtml calculado en renderProds")
    fixes += 1
else:
    print("⚠️  FIX 3: bloque mayorHtml no encontrado")

# ══ FIX 4: Insertar el countdown en el HTML de la tarjeta ══
OLD_CARD_STATS = """      ${mayorHtml}
      ${(function() {
        const st = statsObtener(p.id);"""

NEW_CARD_STATS = """      ${mayorHtml}
      ${countdownHtml}
      ${(function() {
        const st = statsObtener(p.id);"""

if OLD_CARD_STATS in idx:
    idx = idx.replace(OLD_CARD_STATS, NEW_CARD_STATS, 1)
    print("✅ FIX 4: countdown insertado en tarjeta de oferta")
    fixes += 1
else:
    print("⚠️  FIX 4: punto de inserción en tarjeta no encontrado")

# ══ FIX 5: Agregar campo de fecha en admin (Configuración) ══
OLD_CFG_LIMITE = """            <div class="form-group">
              <label class="form-label"><i class="fas fa-fire" style="color:var(--accent);margin-right:4px"></i>Límite "Últimas unidades"</label>
              <input class="form-input" type="number" min="1" max="20" id="cfg-stock-limite" value="5" placeholder="5"/>
              <div style="font-size:.7rem;color:var(--g500);margin-top:4px">Si un producto tiene ≤ este número de unidades, aparece la alerta roja.</div>
            </div>"""

NEW_CFG_LIMITE = """            <div class="form-group">
              <label class="form-label"><i class="fas fa-fire" style="color:var(--accent);margin-right:4px"></i>Límite "Últimas unidades"</label>
              <input class="form-input" type="number" min="1" max="20" id="cfg-stock-limite" value="5" placeholder="5"/>
              <div style="font-size:.7rem;color:var(--g500);margin-top:4px">Si un producto tiene ≤ este número de unidades, aparece la alerta roja.</div>
            </div>
            <div class="form-group">
              <label class="form-label"><i class="fas fa-clock" style="color:var(--sky);margin-right:4px"></i>Fecha fin de ofertas</label>
              <input class="form-input" type="datetime-local" id="cfg-oferta-fin"/>
              <div style="font-size:.7rem;color:var(--g500);margin-top:4px">Fecha y hora en que terminan las ofertas. Si está vacío, usa el próximo domingo.</div>
            </div>"""

with open('admin/index.html', 'r', encoding='utf-8') as f:
    adm = f.read()

if OLD_CFG_LIMITE in adm:
    adm = adm.replace(OLD_CFG_LIMITE, NEW_CFG_LIMITE, 1)
    print("✅ FIX 5: campo fecha fin de ofertas en admin Config")
    fixes += 1

    # Guardar fecha en guardarConfig
    OLD_GC = """function guardarConfig(){
  const limite = document.getElementById('cfg-stock-limite');
  if(limite && limite.value) localStorage.setItem('magama_stock_limite', limite.value);
  showToast('Configuración guardada correctamente');
}"""
    NEW_GC = """function guardarConfig(){
  const limite = document.getElementById('cfg-stock-limite');
  if(limite && limite.value) localStorage.setItem('magama_stock_limite', limite.value);
  const ofertaFin = document.getElementById('cfg-oferta-fin');
  if(ofertaFin && ofertaFin.value) localStorage.setItem('magama_oferta_fin', ofertaFin.value);
  else localStorage.removeItem('magama_oferta_fin');
  showToast('Configuración guardada correctamente');
}"""
    if OLD_GC in adm:
        adm = adm.replace(OLD_GC, NEW_GC, 1)
        print("✅ FIX 5b: guardarConfig guarda fecha oferta")
        fixes += 1

    # Cargar fecha en cargarHeroAdmin
    OLD_CHA = "  const limite = localStorage.getItem('magama_stock_limite');\n  const elLimite = document.getElementById('cfg-stock-limite');\n  if(limite && elLimite) elLimite.value = limite;"
    NEW_CHA = "  const limite = localStorage.getItem('magama_stock_limite');\n  const elLimite = document.getElementById('cfg-stock-limite');\n  if(limite && elLimite) elLimite.value = limite;\n  const ofertaFin = localStorage.getItem('magama_oferta_fin');\n  const elOferta = document.getElementById('cfg-oferta-fin');\n  if(ofertaFin && elOferta) elOferta.value = ofertaFin;"
    if OLD_CHA in adm:
        adm = adm.replace(OLD_CHA, NEW_CHA, 1)
        print("✅ FIX 5c: cargarHeroAdmin carga fecha oferta")
        fixes += 1

    with open('admin/index.html', 'w', encoding='utf-8') as f:
        f.write(adm)
else:
    print("⚠️  FIX 5: campo límite stock en admin no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ {fixes}/7 fixes aplicados")
print("\n🎉 Listo. Los productos con tag 'Oferta' o categoría 'Ofertas'")
print("   mostrarán un contador regresivo animado.")
print("   La fecha fin se configura en Admin → Configuración.")