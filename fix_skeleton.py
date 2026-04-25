#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_skeleton.py
"""

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes = 0

# ══ FIX 1: CSS del skeleton ══
CSS_SKELETON = """
    /* ============================================================
       SKELETON DE CARGA
       ============================================================ */
    .skel-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px,1fr));
      gap: 26px;
    }
    .skel-card {
      background: var(--white);
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid var(--gray-200);
      display: flex; flex-direction: column;
      animation: skelFade .4s ease both;
    }
    @keyframes skelFade {
      from { opacity:0; transform:translateY(12px); }
      to   { opacity:1; transform:translateY(0); }
    }
    .skel-thumb {
      height: 260px;
      background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 50%, var(--gray-100) 75%);
      background-size: 200% 100%;
      animation: skelShimmer 1.4s infinite;
    }
    .skel-body { padding: 16px; display: flex; flex-direction: column; gap: 10px; }
    .skel-line {
      border-radius: 6px;
      background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 50%, var(--gray-100) 75%);
      background-size: 200% 100%;
      animation: skelShimmer 1.4s infinite;
    }
    .skel-line.s { height: 10px; width: 45%; animation-delay: .1s; }
    .skel-line.m { height: 13px; width: 75%; animation-delay: .15s; }
    .skel-line.l { height: 11px; width: 55%; animation-delay: .2s; }
    .skel-foot {
      padding: 12px 16px;
      border-top: 1px solid var(--gray-100);
      display: flex; align-items: center; justify-content: space-between;
    }
    .skel-price {
      height: 22px; width: 70px; border-radius: 6px;
      background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 50%, var(--gray-100) 75%);
      background-size: 200% 100%;
      animation: skelShimmer 1.4s infinite;
      animation-delay: .25s;
    }
    .skel-btn {
      width: 38px; height: 38px; border-radius: 50%;
      background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 50%, var(--gray-100) 75%);
      background-size: 200% 100%;
      animation: skelShimmer 1.4s infinite;
      animation-delay: .3s;
    }
    @keyframes skelShimmer {
      0%   { background-position:  200% 0; }
      100% { background-position: -200% 0; }
    }

    /* Fade in suave al aparecer los productos reales */
    #prodGrid.loaded .prod-card {
      animation: prodAppear .35s ease both;
    }
    @keyframes prodAppear {
      from { opacity:0; transform:translateY(10px); }
      to   { opacity:1; transform:translateY(0); }
    }
    #prodGrid.loaded .prod-card:nth-child(1)  { animation-delay: .00s; }
    #prodGrid.loaded .prod-card:nth-child(2)  { animation-delay: .04s; }
    #prodGrid.loaded .prod-card:nth-child(3)  { animation-delay: .08s; }
    #prodGrid.loaded .prod-card:nth-child(4)  { animation-delay: .12s; }
    #prodGrid.loaded .prod-card:nth-child(5)  { animation-delay: .16s; }
    #prodGrid.loaded .prod-card:nth-child(6)  { animation-delay: .20s; }
    #prodGrid.loaded .prod-card:nth-child(7)  { animation-delay: .24s; }
    #prodGrid.loaded .prod-card:nth-child(8)  { animation-delay: .28s; }
    #prodGrid.loaded .prod-card:nth-child(n+9){ animation-delay: .32s; }
"""

OLD_CSS = "  </style>"
if OLD_CSS in idx:
    idx = idx.replace(OLD_CSS, CSS_SKELETON + "\n  </style>", 1)
    print("✅ FIX 1: CSS skeleton agregado")
    fixes += 1
else:
    print("⚠️  FIX 1: </style> no encontrado")

# ══ FIX 2: función renderSkeleton + modificar renderProds ══
# Agregar función renderSkeleton y modificar renderProds para mostrar
# los productos con la clase loaded (animación entrada)

OLD_RENDER = "function renderProds(list) {\n  const g = document.getElementById('prodGrid');"
NEW_RENDER = """/* ── Skeleton de carga ── */
function renderSkeleton(n) {
  n = n || 8;
  const g = document.getElementById('prodGrid');
  if (!g) return;
  g.classList.remove('loaded');
  g.innerHTML = '<div class="skel-grid" style="grid-column:1/-1">' +
    Array.from({length: n}, function(_, i) {
      return '<div class="skel-card" style="animation-delay:' + (i * 0.06) + 's">' +
        '<div class="skel-thumb"></div>' +
        '<div class="skel-body">' +
          '<div class="skel-line s"></div>' +
          '<div class="skel-line m"></div>' +
          '<div class="skel-line l"></div>' +
        '</div>' +
        '<div class="skel-foot">' +
          '<div class="skel-price"></div>' +
          '<div class="skel-btn"></div>' +
        '</div>' +
      '</div>';
    }).join('') +
  '</div>';
}

function renderProds(list) {
  const g = document.getElementById('prodGrid');"""

if OLD_RENDER in idx:
    idx = idx.replace(OLD_RENDER, NEW_RENDER, 1)
    print("✅ FIX 2: función renderSkeleton agregada")
    fixes += 1
else:
    print("⚠️  FIX 2: renderProds no encontrado")

# ══ FIX 3: añadir clase 'loaded' al grid cuando se renderizan productos reales ══
OLD_GRID_END = "  g.innerHTML = list.map(p => {"
NEW_GRID_END = "  g.classList.remove('loaded');\n  g.innerHTML = list.map(p => {"
if OLD_GRID_END in idx:
    idx = idx.replace(OLD_GRID_END, NEW_GRID_END, 1)
    print("✅ FIX 3: limpiar clase loaded antes de renderizar")
    fixes += 1
else:
    print("⚠️  FIX 3: g.innerHTML no encontrado")

# ══ FIX 4: agregar clase loaded después de renderizar ══
# Buscar el cierre de renderProds para agregar la clase
OLD_CLOSE = "  g.innerHTML = list.map(p => {\n    /* Soporte dual:"
NEW_CLOSE = "  g.classList.remove('loaded');\n  g.innerHTML = list.map(p => {\n    /* Soporte dual:"

# El FIX 3 ya hizo esto, ahora agregar loaded al final
# Buscar el final de la función renderProds
OLD_END = "  g.innerHTML = list.map(p => {"
# Ya modificado, buscar donde termina el map
OLD_REND_CLOSE = "  }).join('');\n}"
# Hay varios join, buscar el de renderProds específicamente
# Agregar loaded via requestAnimationFrame al final del innerHTML
OLD_JOIN = "  }).join('');\n}\n\n/* Filters */"
NEW_JOIN = "  }).join('');\n  requestAnimationFrame(function() { g.classList.add('loaded'); });\n}\n\n/* Filters */"
if OLD_JOIN in idx:
    idx = idx.replace(OLD_JOIN, NEW_JOIN, 1)
    print("✅ FIX 4: clase 'loaded' agregada al renderizar productos")
    fixes += 1
else:
    print("⚠️  FIX 4: cierre renderProds no encontrado")

# ══ FIX 5: mostrar skeleton en el Init antes de renderProds ══
OLD_INIT = "/* Init */\nconst productosFinales = obtenerProductosActuales();\nrenderProds(productosFinales);\nrenderResenas();"
NEW_INIT = """/* Init */
renderSkeleton(8); /* Mostrar skeleton inmediatamente */
setTimeout(function() {
  const productosFinales = obtenerProductosActuales();
  renderProds(productosFinales);
  renderResenas();
}, 300); /* Pequeño delay para que se vea el skeleton */"""

if OLD_INIT in idx:
    idx = idx.replace(OLD_INIT, NEW_INIT, 1)
    print("✅ FIX 5: skeleton en Init")
    fixes += 1
else:
    # Intentar sin renderResenas
    OLD_INIT2 = "/* Init */\nconst productosFinales = obtenerProductosActuales();\nrenderProds(productosFinales);"
    NEW_INIT2 = """/* Init */
renderSkeleton(8);
setTimeout(function() {
  const productosFinales = obtenerProductosActuales();
  renderProds(productosFinales);
  if (typeof renderResenas === 'function') renderResenas();
}, 300);"""
    if OLD_INIT2 in idx:
        idx = idx.replace(OLD_INIT2, NEW_INIT2, 1)
        print("✅ FIX 5b: skeleton en Init (alternativo)")
        fixes += 1
    else:
        print("⚠️  FIX 5: Init no encontrado")

# ══ FIX 6: también mostrar skeleton al filtrar productos ══
OLD_FILTER = "function filterProds(btn, cat) {\n  document.querySelectorAll('.fb').forEach(b => b.classList.remove('active'));\n  btn.classList.add('active');\n  const lista = obtenerProductosActuales();\n  renderProds(cat === 'all' ? lista : lista.filter(p => (p.cat||p.categoria) === cat));"

NEW_FILTER = """function filterProds(btn, cat) {
  document.querySelectorAll('.fb').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderSkeleton(8);
  setTimeout(function() {
    const lista = obtenerProductosActuales();
    renderProds(cat === 'all' ? lista : lista.filter(p => (p.cat||p.categoria) === cat));
  }, 180);"""

if OLD_FILTER in idx:
    idx = idx.replace(OLD_FILTER, NEW_FILTER, 1)
    print("✅ FIX 6: skeleton al filtrar categorías")
    fixes += 1
else:
    print("⚠️  FIX 6: filterProds no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ index.html: {fixes}/6 fixes aplicados")
print("\n🎉 Listo. El skeleton aparece al cargar y al cambiar filtros.")