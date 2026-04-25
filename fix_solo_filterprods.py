#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_solo_filterprods.py

Corrige SOLO UN BUG: el bloque de funciones de estadísticas
que quedó atrapado DENTRO de la función filterProds().

No toca NADA más del archivo.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Archivo leído: {content.count(chr(10))} líneas")

# ══ VERIFICAR EL BUG ══
# El bug es: el bloque de stats está DENTRO de filterProds
idx_filter = content.find('function filterProds(btn, cat)')
idx_stats   = content.find('const STATS_KEY')

if idx_stats == -1:
    print("⚠️  No se encontró STATS_KEY en el archivo")
    print("   El bloque de stats no está en este archivo")
    exit()

if idx_stats > idx_filter:
    # Verificar que está DENTRO de filterProds (antes del siguiente })
    fragmento = content[idx_filter:idx_filter + 2000]
    if 'const STATS_KEY' in fragmento:
        print("✅ Bug confirmado: STATS_KEY está dentro de filterProds")
    else:
        print("✅ STATS_KEY ya está en el lugar correcto — no hay nada que corregir")
        exit()
else:
    print("✅ STATS_KEY ya está antes de filterProds — no hay nada que corregir")
    exit()

# ══ EL BLOQUE PROBLEMÁTICO ══
# Es exactamente este texto que está DENTRO de filterProds:
BLOQUE_STATS = """  /* ════════════════════════════════════════════════════
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

# ══ VERIFICAR QUÉ HAY ANTES Y DESPUÉS DEL BLOQUE ══
if BLOQUE_STATS not in content:
    # Intentar encontrar una versión sin la indentación exacta
    print("Buscando el bloque con formato alternativo...")
    # Buscar desde STATS_KEY hasta statsFormatear
    inicio = content.find("/* ════════════════════════════════════════════════════\n   CONTADORES DE VISTAS Y VENDIDOS")
    if inicio == -1:
        inicio = content.find("const STATS_KEY = 'magama_stats';")
    
    if inicio != -1:
        fin = content.find("  return String(n);\n}\n", inicio)
        if fin != -1:
            fin = fin + len("  return String(n);\n}\n")
            bloque_encontrado = content[inicio:fin]
            print(f"Bloque encontrado ({len(bloque_encontrado)} chars):")
            print(repr(bloque_encontrado[:100]))
            
            # Determinar qué hay ANTES del bloque dentro de filterProds
            antes = content[:inicio]
            despues = content[fin:]
            
            # El bloque debe ir ANTES de filterProds, no dentro
            # Buscar el inicio de filterProds para saber dónde insertar
            idx_fp = antes.rfind('function filterProds(btn, cat)')
            
            if idx_fp != -1:
                print("✅ Bloque está dentro de filterProds — corrigiendo...")
                
                # Eliminar el bloque de donde está (dentro de filterProds)
                content_sin_bloque = antes + despues
                
                # Insertar el bloque ANTES de filterProds
                idx_fp2 = content_sin_bloque.rfind('function filterProds(btn, cat)')
                
                BLOQUE_LIMPIO = """/* ════════════════════════════════════════════════════
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
                content_final = (
                    content_sin_bloque[:idx_fp2] +
                    BLOQUE_LIMPIO +
                    content_sin_bloque[idx_fp2:]
                )
                
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(content_final)
                
                print(f"✅ Bug corregido exitosamente")
                print(f"   Líneas antes: {content.count(chr(10))}")
                print(f"   Líneas después: {content_final.count(chr(10))}")
                
                # Verificar
                idx_fp_check = content_final.find('function filterProds(btn, cat)')
                idx_stats_check = content_final.find('const STATS_KEY')
                print(f"\nVerificación:")
                print(f"  STATS_KEY en posición: {idx_stats_check}")
                print(f"  filterProds en posición: {idx_fp_check}")
                print(f"  ✅ STATS_KEY está ANTES de filterProds: {idx_stats_check < idx_fp_check}")
            else:
                print("⚠️  No se pudo determinar la posición correcta")
        else:
            print("⚠️  No se encontró el fin del bloque stats")
    else:
        print("⚠️  No se encontró el inicio del bloque stats")
else:
    # El bloque se encontró con formato exacto
    # Eliminarlo de donde está e insertarlo antes de filterProds
    content_sin_bloque = content.replace(BLOQUE_STATS, '', 1)
    
    idx_fp = content_sin_bloque.find('function filterProds(btn, cat)')
    
    BLOQUE_LIMPIO = """/* ════════════════════════════════════════════════════
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
    content_final = (
        content_sin_bloque[:idx_fp] +
        BLOQUE_LIMPIO +
        content_sin_bloque[idx_fp:]
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content_final)
    
    print(f"✅ Bug corregido exitosamente")
    print(f"   Líneas: {content_final.count(chr(10))}")
    
    idx_stats_final = content_final.find('const STATS_KEY')
    idx_fp_final    = content_final.find('function filterProds(btn, cat)')
    print(f"\nVerificación:")
    print(f"  ✅ STATS_KEY antes de filterProds: {idx_stats_final < idx_fp_final}")