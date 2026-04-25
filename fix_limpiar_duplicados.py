#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_limpiar_duplicados.py

Elimina los bloques duplicados que quedaron en index.html
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

fixes = 0

# ══ FIX 1: Eliminar segundo bloque CSS stock-low-badge ══
BLOQUE_STOCK = """

    /* ── Indicador últimas unidades ── */
    .stock-low-badge {
      position: absolute; bottom: 10px; left: 10px;
      background: linear-gradient(135deg, #FF6B6B, #ff4444);
      color: #fff; font-size: .6rem; font-weight: 800;
      padding: 4px 10px; border-radius: 20px;
      letter-spacing: .06em; text-transform: uppercase;
      display: flex; align-items: center; gap: 4px;
      box-shadow: 0 3px 10px rgba(255,107,107,.45);
      animation: stockPulse 2s ease-in-out infinite;
      z-index: 2;
    }
    .stock-low-badge i { font-size: .58rem; }
    @keyframes stockPulse {
      0%,100% { box-shadow: 0 3px 10px rgba(255,107,107,.45); }
      50%      { box-shadow: 0 3px 18px rgba(255,107,107,.75); }
    }
    .prod-card.stock-low {
      border-color: rgba(255,107,107,.35);
    }"""

# El primer bloque debe quedar, el segundo se elimina
count = content.count(BLOQUE_STOCK)
if count == 2:
    # Eliminar solo la segunda ocurrencia
    first = content.find(BLOQUE_STOCK)
    second = content.find(BLOQUE_STOCK, first + len(BLOQUE_STOCK))
    content = content[:second] + content[second + len(BLOQUE_STOCK):]
    print("✅ FIX 1: segundo bloque CSS stock-low eliminado")
    fixes += 1
elif count == 1:
    print("✅ FIX 1: ya estaba limpio (1 sola vez)")
    fixes += 1
else:
    print(f"⚠️  FIX 1: bloque aparece {count} veces")

# ══ FIX 2: Eliminar segundo bloque CSS CONTADORES ══
BLOQUE_CSS_STATS = """

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
    .prod-stat-sep { color: var(--gray-200); }"""

count2 = content.count(BLOQUE_CSS_STATS)
if count2 == 2:
    first = content.find(BLOQUE_CSS_STATS)
    second = content.find(BLOQUE_CSS_STATS, first + len(BLOQUE_CSS_STATS))
    content = content[:second] + content[second + len(BLOQUE_CSS_STATS):]
    print("✅ FIX 2: segundo bloque CSS contadores eliminado")
    fixes += 1
elif count2 == 1:
    print("✅ FIX 2: ya estaba limpio")
    fixes += 1
else:
    print(f"⚠️  FIX 2: {count2} veces")

# ══ FIX 3: Eliminar segundo bloque JS STATS completo ══
BLOQUE_JS_STATS = """

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
}"""

count3 = content.count(BLOQUE_JS_STATS)
if count3 == 2:
    first = content.find(BLOQUE_JS_STATS)
    second = content.find(BLOQUE_JS_STATS, first + len(BLOQUE_JS_STATS))
    content = content[:second] + content[second + len(BLOQUE_JS_STATS):]
    print("✅ FIX 3: segundo bloque JS contadores eliminado")
    fixes += 1
elif count3 == 1:
    print("✅ FIX 3: ya estaba limpio")
    fixes += 1
else:
    print(f"⚠️  FIX 3: {count3} veces")

# ══ FIX 4: Agregar el hook de ventas que faltaba ══
# Solo si no existe ya
HOOK_VENTAS = """
/* ── Hook: registrar ventas al hacer pedido ── */
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.cart-checkout-btn');
  if (!btn) return;
  if (typeof carrito !== 'undefined' && Array.isArray(carrito)) {
    carrito.forEach(function(item) {
      if (item.prodId) statsRegistrarVenta(item.prodId, item.qty);
    });
  }
});"""

if HOOK_VENTAS.strip() in content:
    print("✅ FIX 4: hook ventas ya existe")
    fixes += 1
else:
    # Agregar antes del cierre del script
    OLD = "window.addEventListener('storage', function(e){\n  if(e.key === 'magama_productos'){\n    renderProds(obtenerProductosActuales());\n  }\n});"
    if OLD in content:
        content = content.replace(OLD, OLD + "\n" + HOOK_VENTAS, 1)
        print("✅ FIX 4: hook ventas agregado")
        fixes += 1
    else:
        print("⚠️  FIX 4: punto de inserción no encontrado")

# ══ Verificación final ══
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {fixes}/4 fixes aplicados")

# Contar ocurrencias finales
print("\nVerificación final:")
print(f"  stock-low-badge CSS: {content.count('/* ── Indicador últimas unidades ──')} vez (debe ser 1)")
print(f"  CSS contadores: {content.count('CONTADORES DE VISTAS Y VENDIDOS')} vez (debe ser 1)")
print(f"  JS statsCargar: {content.count('function statsCargar()')} vez (debe ser 1)")
print(f"  Hook ventas: {content.count('cart-checkout-btn')} veces")