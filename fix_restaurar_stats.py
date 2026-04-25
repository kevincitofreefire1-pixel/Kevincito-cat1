#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_restaurar_stats.py
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Verificar estado actual
tiene_stats = 'function statsCargar()' in content
tiene_hook  = 'cart-checkout-btn' in content

print(f"statsCargar existe: {tiene_stats}")
print(f"hook ventas existe: {tiene_hook}")

JS_STATS = """
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

if not tiene_stats:
    # Insertar antes del Init
    OLD = "/* Init */\nrenderSkeleton(8);"
    if OLD in content:
        content = content.replace(OLD, JS_STATS + "/* Init */\nrenderSkeleton(8);", 1)
        print("✅ JS contadores restaurado")
    else:
        # Alternativa: insertar antes del window.addEventListener storage
        OLD2 = "window.addEventListener('storage', function(e){\n  if(e.key === 'magama_productos'){"
        if OLD2 in content:
            content = content.replace(OLD2, JS_STATS + OLD2, 1)
            print("✅ JS contadores restaurado (alternativo)")
        else:
            print("⚠️  No se encontró punto de inserción")
else:
    print("✅ statsCargar ya existe — no necesita restaurarse")

# Verificación
print(f"\nVerificación final:")
print(f"  statsCargar: {content.count('function statsCargar()')} vez (debe ser 1)")
print(f"  statsRegistrarVista: {content.count('function statsRegistrarVista(')} vez (debe ser 1)")
print(f"  statsObtener: {content.count('function statsObtener(')} vez (debe ser 1)")
print(f"  hook ventas: {'✅' if 'cart-checkout-btn' in content else '❌'}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Listo")