#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_contador.py
"""

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes = 0

# ══ FIX 1: CSS contadores ══
CSS_CONTADOR = """
    /* ============================================================
       CONTADORES DE VISTAS Y VENDIDOS
       ============================================================ */
    .prod-stats {
      display: flex; align-items: center; gap: 10px;
      padding: 0 16px 10px;
      font-size: .68rem; color: var(--gray-500);
    }
    .prod-stat {
      display: flex; align-items: center; gap: 4px;
      font-weight: 600;
    }
    .prod-stat i { font-size: .62rem; }
    .prod-stat.vistas i  { color: var(--navy-mid); }
    .prod-stat.vendidos i { color: #06D6A0; }
    .prod-stat-sep { color: var(--gray-200); }
"""

OLD_CSS = "  </style>"
if OLD_CSS in idx:
    idx = idx.replace(OLD_CSS, CSS_CONTADOR + "\n  </style>", 1)
    print("✅ FIX 1: CSS contadores agregado")
    fixes += 1
else:
    print("⚠️  FIX 1: </style> no encontrado")

# ══ FIX 2: JS — sistema de vistas y vendidos ══
# Agregar antes del Init

JS_CONTADOR = """
/* ════════════════════════════════════════════════════
   CONTADORES DE VISTAS Y VENDIDOS
   ════════════════════════════════════════════════════ */
const STATS_KEY = 'magama_stats';

function statsCargar() {
  try {
    const raw = localStorage.getItem(STATS_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch(e) { return {}; }
}

function statsGuardar(data) {
  try { localStorage.setItem(STATS_KEY, JSON.stringify(data)); } catch(e) {}
}

function statsRegistrarVista(prodId) {
  const data = statsCargar();
  if (!data[prodId]) data[prodId] = { vistas: 0, vendidos: 0 };
  data[prodId].vistas = (data[prodId].vistas || 0) + 1;
  statsGuardar(data);
}

function statsRegistrarVenta(prodId, qty) {
  const data = statsCargar();
  if (!data[prodId]) data[prodId] = { vistas: 0, vendidos: 0 };
  data[prodId].vendidos = (data[prodId].vendidos || 0) + (qty || 1);
  statsGuardar(data);
}

function statsObtener(prodId) {
  const data = statsCargar();
  return data[prodId] || { vistas: 0, vendidos: 0 };
}

function statsFormatear(n) {
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
  return String(n);
}

"""

OLD_INIT = "/* Init */\nrenderSkeleton(8);"
if OLD_INIT in idx:
    idx = idx.replace(OLD_INIT, JS_CONTADOR + "/* Init */\nrenderSkeleton(8);", 1)
    print("✅ FIX 2: JS contadores agregado")
    fixes += 1
else:
    # Intentar sin skeleton
    OLD_INIT2 = "/* Init */\nconst productosFinales"
    if OLD_INIT2 in idx:
        idx = idx.replace(OLD_INIT2, JS_CONTADOR + "/* Init */\nconst productosFinales", 1)
        print("✅ FIX 2b: JS contadores agregado (alternativo)")
        fixes += 1
    else:
        print("⚠️  FIX 2: punto de inserción no encontrado")

# ══ FIX 3: Agregar contadores en las tarjetas de producto ══
# Buscar el bloque del prod-foot en renderProds y agregar stats antes

OLD_CARD = """      ${mayorHtml}
      <div class="prod-foot">"""
NEW_CARD = """      ${mayorHtml}
      ${(function() {
        const st = statsObtener(p.id);
        const v  = st.vistas   || 0;
        const ve = st.vendidos || 0;
        if (!v && !ve) return '';
        return '<div class="prod-stats">' +
          (v  ? '<span class="prod-stat vistas"><i class="fas fa-eye"></i> ' + statsFormatear(v) + ' vistas</span>' : '') +
          (v && ve ? '<span class="prod-stat-sep">·</span>' : '') +
          (ve ? '<span class="prod-stat vendidos"><i class="fas fa-shopping-bag"></i> ' + statsFormatear(ve) + ' vendidos</span>' : '') +
        '</div>';
      })()}
      <div class="prod-foot">"""

if OLD_CARD in idx:
    idx = idx.replace(OLD_CARD, NEW_CARD, 1)
    print("✅ FIX 3: contadores en tarjetas")
    fixes += 1
else:
    print("⚠️  FIX 3: bloque prod-foot no encontrado")

# ══ FIX 4: Registrar vista al abrir el detalle ══
# En abrirDetalle de producto-detalle.js, registrar la vista
# Como no podemos modificar producto-detalle.js aquí, lo hacemos
# interceptando el onclick de las tarjetas con un wrapper

OLD_CLICK = 'onclick="abrirDetalle(${p.id})">${nombre}</div>'
NEW_CLICK = 'onclick="statsRegistrarVista(${p.id});abrirDetalle(${p.id})">${nombre}</div>'
if OLD_CLICK in idx:
    idx = idx.replace(OLD_CLICK, NEW_CLICK, 1)
    print("✅ FIX 4a: registrar vista al click en nombre")
    fixes += 1
else:
    print("⚠️  FIX 4a: onclick nombre no encontrado")

# También en el thumb
OLD_THUMB = 'onclick="abrirDetalle(${p.id})">\n        ${thumbContent}'
NEW_THUMB = 'onclick="statsRegistrarVista(${p.id});abrirDetalle(${p.id})">\n        ${thumbContent}'
if OLD_THUMB in idx:
    idx = idx.replace(OLD_THUMB, NEW_THUMB, 1)
    print("✅ FIX 4b: registrar vista al click en imagen")
    fixes += 1
else:
    print("⚠️  FIX 4b: onclick thumb no encontrado")

# ══ FIX 5: Registrar venta al hacer pedido por WhatsApp ══
# En carrito.js registramos la venta — pero como está en archivo separado
# lo hacemos en el hacerPedido si existe en index.html, sino en un hook

# Agregar hook que intercepta el botón de pedir por WhatsApp
JS_HOOK_PEDIDO = """
/* ── Hook: registrar ventas al hacer pedido ── */
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.cart-checkout-btn');
  if (!btn) return;
  /* Registrar ventas de cada item del carrito */
  if (typeof carrito !== 'undefined' && Array.isArray(carrito)) {
    carrito.forEach(function(item) {
      if (item.prodId) statsRegistrarVenta(item.prodId, item.qty);
    });
  }
});
"""

OLD_STORAGE = "// Actualizar en tiempo real si el admin cambia productos\nwindow.addEventListener('storage', function(e){"
if OLD_STORAGE in idx:
    idx = idx.replace(OLD_STORAGE, JS_HOOK_PEDIDO + "\n// Actualizar en tiempo real si el admin cambia productos\nwindow.addEventListener('storage', function(e){", 1)
    print("✅ FIX 5: hook registro de ventas al hacer pedido")
    fixes += 1
else:
    print("⚠️  FIX 5: punto de inserción storage no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ index.html: {fixes}/6 fixes aplicados")
print("\n🎉 Listo.")
print("  - Las vistas se cuentan cada vez que alguien hace clic en un producto")
print("  - Las ventas se cuentan cuando alguien hace clic en 'Pedir por WhatsApp'")
print("  - Los contadores aparecen en la tarjeta si hay al menos 1 vista o venta")