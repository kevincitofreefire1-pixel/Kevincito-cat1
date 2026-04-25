#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_resenas.py
"""

# ══════════════════════════════════════════════
# PATCH index.html — agregar sección reseñas
# ══════════════════════════════════════════════
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes = 0

# CSS de reseñas — insertar antes del cierre de </style>
CSS_RESENAS = """
    /* ============================================================
       RESEÑAS / TESTIMONIOS
       ============================================================ */
    .resenas-sec { background: var(--white); }
    .resenas-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
    }
    .resena-card {
      background: var(--cream);
      border-radius: 18px;
      padding: 28px 26px;
      border: 1px solid var(--gray-200);
      box-shadow: var(--shadow-sm);
      display: flex; flex-direction: column; gap: 16px;
      transition: transform var(--transition), box-shadow var(--transition);
      position: relative;
    }
    .resena-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
    .resena-card::before {
      content: '"';
      position: absolute; top: 16px; right: 22px;
      font-family: var(--font-display); font-size: 5rem;
      color: var(--navy-mid); opacity: .08; line-height: 1;
      pointer-events: none;
    }
    .resena-estrellas { display: flex; gap: 3px; }
    .resena-estrellas i { color: #FFB703; font-size: .85rem; }
    .resena-texto {
      font-size: .88rem; line-height: 1.75;
      color: var(--gray-700); flex: 1;
      font-style: italic;
    }
    .resena-autor {
      display: flex; align-items: center; gap: 12px;
      border-top: 1px solid var(--gray-200);
      padding-top: 14px;
    }
    .resena-avatar {
      width: 44px; height: 44px; border-radius: 50%;
      background: linear-gradient(135deg, var(--navy), var(--navy-mid));
      display: flex; align-items: center; justify-content: center;
      color: var(--sky-light); font-weight: 700; font-size: 1rem;
      flex-shrink: 0;
    }
    .resena-nombre { font-weight: 700; font-size: .88rem; color: var(--navy); }
    .resena-detalle { font-size: .72rem; color: var(--gray-500); margin-top: 1px; }
    .resena-badge {
      display: inline-flex; align-items: center; gap: 5px;
      background: rgba(6,214,160,.1); color: #039d76;
      font-size: .65rem; font-weight: 700; padding: 2px 8px;
      border-radius: 20px; margin-top: 3px; width: fit-content;
    }
    .resena-badge i { font-size: .6rem; }

    @media (max-width: 900px) {
      .resenas-grid { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 520px) {
      .resenas-grid { grid-template-columns: 1fr; }
    }
"""

OLD_CSS = "  </style>"
if OLD_CSS in idx:
    idx = idx.replace(OLD_CSS, CSS_RESENAS + "\n  </style>", 1)
    print("✅ CSS reseñas agregado")
    fixes += 1
else:
    print("⚠️  CSS: </style> no encontrado")

# HTML de reseñas — insertar entre Features y Newsletter
HTML_RESENAS = """
<!-- RESEÑAS -->
<section class="sec resenas-sec" id="resenas">
  <div class="sec-inner">
    <div class="sec-hdr">
      <div class="sec-eyebrow">Lo que dicen nuestros clientes</div>
      <h2 class="sec-title">Reseñas <em>verificadas</em></h2>
      <div class="sec-bar"></div>
    </div>
    <div class="resenas-grid" id="resenasGrid">
      <!-- Las reseñas se cargan dinámicamente desde localStorage -->
    </div>
  </div>
</section>

"""

OLD_SECTION = "</section>\n\n<!-- NEWSLETTER -->"
if OLD_SECTION in idx:
    idx = idx.replace(OLD_SECTION, "</section>\n" + HTML_RESENAS + "\n<!-- NEWSLETTER -->", 1)
    print("✅ HTML sección reseñas insertada")
    fixes += 1
else:
    print("⚠️  HTML: separador features/newsletter no encontrado")

# JS para cargar reseñas — agregar antes de los scripts al final
RESENAS_DEFAULT = [
    {"nombre":"María G.","detalle":"Compró Polo Top","texto":"Excelente calidad, llegó rápido y el trato fue muy amable. Definitivamente volvería a comprar acá. ¡El polo quedó perfecto!","estrellas":5,"producto":"Polo Top"},
    {"nombre":"Carlos R.","detalle":"Compró Casaca Jean","texto":"Muy buena atención por WhatsApp, me ayudaron a elegir la talla correcta. La casaca es tal como en las fotos, muy bonita.","estrellas":5,"producto":"Casaca Jean"},
    {"nombre":"Lucía M.","detalle":"Compró Vestido Oferta","texto":"Me sorprendió la calidad por el precio. El vestido es precioso y el despacho fue muy rápido. 100% recomendado.","estrellas":5,"producto":"Vestido Oferta"},
]

JS_RESENAS = """
/* ── Reseñas dinámicas ── */
function renderResenas() {
  const grid = document.getElementById('resenasGrid');
  if (!grid) return;
  var resenas;
  try {
    var raw = localStorage.getItem('magama_resenas');
    resenas = raw ? JSON.parse(raw) : null;
  } catch(e) { resenas = null; }

  if (!resenas || !resenas.length) {
    resenas = """ + str(RESENAS_DEFAULT).replace("True","true").replace("False","false") + """;
  }

  grid.innerHTML = resenas.map(function(r) {
    var estrellas = '';
    for (var i = 0; i < 5; i++) {
      estrellas += '<i class="' + (i < r.estrellas ? 'fas' : 'far') + ' fa-star"></i>';
    }
    var inicial = (r.nombre || 'C').charAt(0).toUpperCase();
    return '<div class="resena-card">' +
      '<div class="resena-estrellas">' + estrellas + '</div>' +
      '<p class="resena-texto">' + r.texto + '</p>' +
      '<div class="resena-autor">' +
        '<div class="resena-avatar">' + inicial + '</div>' +
        '<div>' +
          '<div class="resena-nombre">' + r.nombre + '</div>' +
          '<div class="resena-detalle">' + r.detalle + '</div>' +
          '<div class="resena-badge"><i class="fas fa-check-circle"></i> Compra verificada</div>' +
        '</div>' +
      '</div>' +
    '</div>';
  }).join('');
}

/* Escuchar cambios de reseñas desde el admin */
window.addEventListener('storage', function(e) {
  if (e.key === 'magama_resenas') renderResenas();
});
"""

OLD_JS = "/* Init */\nconst productosFinales"
if OLD_JS in idx:
    idx = idx.replace(OLD_JS, JS_RESENAS + "\n/* Init */\nconst productosFinales", 1)
    print("✅ JS renderResenas agregado")
    fixes += 1
else:
    print("⚠️  JS: punto de inserción no encontrado")

# Llamar renderResenas en el Init
OLD_INIT = "renderProds(productosFinales);\n\n// Actualizar en tiempo real"
if OLD_INIT in idx:
    idx = idx.replace(OLD_INIT, "renderProds(productosFinales);\nrenderResenas();\n\n// Actualizar en tiempo real", 1)
    print("✅ renderResenas() en Init")
    fixes += 1
else:
    # Intentar sin el storage listener
    OLD_INIT2 = "renderProds(productosFinales);"
    if OLD_INIT2 in idx:
        idx = idx.replace(OLD_INIT2, "renderProds(productosFinales);\nrenderResenas();", 1)
        print("✅ renderResenas() en Init (alternativo)")
        fixes += 1
    else:
        print("⚠️  Init: renderProds no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ index.html: {fixes}/4 fixes")

# ══════════════════════════════════════════════
# PATCH admin/index.html — gestión de reseñas
# ══════════════════════════════════════════════
import os
admin_path = 'admin/index.html'
if not os.path.exists(admin_path):
    print("\n⚠️  admin/index.html no encontrado")
    exit()

with open(admin_path, 'r', encoding='utf-8') as f:
    adm = f.read()

fixes_adm = 0

# Agregar nav item Reseñas en el sidebar
OLD_NAV = '<div class="sb-section">Configuración</div>'
NEW_NAV = '<div class="sb-item" onclick="showView(\'resenas\',this)"><i class="fas fa-star"></i><span class="sb-item-label">Reseñas</span></div>\n    <div class="sb-section">Configuración</div>'
if OLD_NAV in adm:
    adm = adm.replace(OLD_NAV, NEW_NAV, 1)
    print("\n✅ ADM: nav item Reseñas agregado")
    fixes_adm += 1
else:
    print("\n⚠️  ADM: nav sidebar no encontrado")

# Agregar vista reseñas antes del cierre de .content
OLD_CONTENT = "    <!-- CONFIG -->"
NEW_CONTENT = """    <!-- RESEÑAS -->
    <div class="view" id="view-resenas">
      <div class="view-section-badge"><i class="fas fa-star"></i> Reseñas de Clientes</div>
      <div class="panel">
        <div class="panel-hdr">
          <div class="panel-title"><i class="fas fa-plus"></i> Agregar Reseña</div>
        </div>
        <div class="panel-body">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Nombre del cliente <span class="req">*</span></label>
              <input class="form-input" id="r-nombre" placeholder="Ej: María G."/>
            </div>
            <div class="form-group">
              <label class="form-label">Detalle (qué compró)</label>
              <input class="form-input" id="r-detalle" placeholder="Ej: Compró Polo Top"/>
            </div>
            <div class="form-group form-full">
              <label class="form-label">Comentario <span class="req">*</span></label>
              <textarea class="form-textarea" id="r-texto" placeholder="Escribe el comentario del cliente..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Estrellas</label>
              <select class="form-select" id="r-estrellas">
                <option value="5">⭐⭐⭐⭐⭐ 5 estrellas</option>
                <option value="4">⭐⭐⭐⭐ 4 estrellas</option>
                <option value="3">⭐⭐⭐ 3 estrellas</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Producto mencionado</label>
              <input class="form-input" id="r-producto" placeholder="Ej: Polo Top"/>
            </div>
          </div>
          <div style="margin-top:20px;display:flex;justify-content:flex-end">
            <button class="btn-save" onclick="agregarResena()"><i class="fas fa-plus"></i> Agregar Reseña</button>
          </div>
        </div>
      </div>
      <div class="panel">
        <div class="panel-hdr"><div class="panel-title"><i class="fas fa-list"></i> Reseñas actuales</div></div>
        <div id="resenas-lista" style="padding:16px"></div>
      </div>
    </div>

    <!-- CONFIG -->"""

if OLD_CONTENT in adm:
    adm = adm.replace(OLD_CONTENT, NEW_CONTENT, 1)
    print("✅ ADM: vista reseñas agregada")
    fixes_adm += 1
else:
    print("⚠️  ADM: bloque config no encontrado")

# Agregar JS de reseñas
OLD_JS_ADM = "document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});"
NEW_JS_ADM = """document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});

/* ─── RESEÑAS ─── */
function cargarResenas(){
  try {
    var raw = localStorage.getItem('magama_resenas');
    return raw ? JSON.parse(raw) : [];
  } catch(e) { return []; }
}

function guardarResenas(arr){
  try {
    localStorage.setItem('magama_resenas', JSON.stringify(arr));
  } catch(e) { showToast('Error al guardar ⚠️','err'); }
}

function agregarResena(){
  var nombre = document.getElementById('r-nombre').value.trim();
  var texto  = document.getElementById('r-texto').value.trim();
  if(!nombre||!texto){ showToast('Completa nombre y comentario ⚠️','err'); return; }

  var resenas = cargarResenas();
  resenas.push({
    nombre:    nombre,
    detalle:   document.getElementById('r-detalle').value.trim() || 'Cliente verificado',
    texto:     texto,
    estrellas: parseInt(document.getElementById('r-estrellas').value) || 5,
    producto:  document.getElementById('r-producto').value.trim() || '',
  });
  guardarResenas(resenas);

  /* Limpiar formulario */
  ['r-nombre','r-detalle','r-texto','r-producto'].forEach(function(id){
    document.getElementById(id).value = '';
  });
  document.getElementById('r-estrellas').value = '5';

  renderResenasAdmin();
  showToast('Reseña agregada correctamente ✅');
}

function eliminarResena(idx){
  if(!confirm('¿Eliminar esta reseña?')) return;
  var resenas = cargarResenas();
  resenas.splice(idx, 1);
  guardarResenas(resenas);
  renderResenasAdmin();
  showToast('Reseña eliminada');
}

function renderResenasAdmin(){
  var el = document.getElementById('resenas-lista');
  if(!el) return;
  var resenas = cargarResenas();
  if(!resenas.length){
    el.innerHTML = '<div class="empty-state"><i class="fas fa-star"></i><p>No hay reseñas aún. Agrega la primera.</p></div>';
    return;
  }
  el.innerHTML = resenas.map(function(r, i){
    var estrellas = '';
    for(var s=0;s<r.estrellas;s++) estrellas += '⭐';
    return '<div style="display:flex;align-items:flex-start;gap:14px;padding:14px 0;border-bottom:1px solid var(--g100)">' +
      '<div style="flex:1">' +
        '<div style="font-weight:700;color:var(--navy)">' + r.nombre + ' ' + estrellas + '</div>' +
        '<div style="font-size:.74rem;color:var(--g500);margin:2px 0">' + r.detalle + '</div>' +
        '<div style="font-size:.84rem;color:var(--g700);margin-top:6px;font-style:italic">"' + r.texto + '"</div>' +
      '</div>' +
      '<button class="act-btn act-del" onclick="eliminarResena(' + i + ')"><i class="fas fa-trash"></i></button>' +
    '</div>';
  }).join('');
}"""

if OLD_JS_ADM in adm:
    adm = adm.replace(OLD_JS_ADM, NEW_JS_ADM, 1)
    print("✅ ADM: JS reseñas agregado")
    fixes_adm += 1
else:
    print("⚠️  ADM: punto JS no encontrado")

# Cargar reseñas al abrir la vista
OLD_VIEW = "  if(id==='config')     cargarHeroAdmin();"
NEW_VIEW = "  if(id==='config')     cargarHeroAdmin();\n  if(id==='resenas')    renderResenasAdmin();"
if OLD_VIEW in adm:
    adm = adm.replace(OLD_VIEW, NEW_VIEW, 1)
    print("✅ ADM: renderResenasAdmin en showView")
    fixes_adm += 1
else:
    print("⚠️  ADM: showView config no encontrado")

# Agregar título en pageTitles
OLD_PT = "  config:     ['Configuración','Datos y ajustes de la tienda'],"
NEW_PT = "  config:     ['Configuración','Datos y ajustes de la tienda'],\n  resenas:    ['Reseñas','Comentarios de clientes verificados'],"
if OLD_PT in adm:
    adm = adm.replace(OLD_PT, NEW_PT, 1)
    print("✅ ADM: título reseñas en pageTitles")
    fixes_adm += 1
else:
    print("⚠️  ADM: pageTitles no encontrado")

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(adm)

print(f"\n✅ admin/index.html: {fixes_adm}/5 fixes")
print("\n🎉 Listo. Ejecuta: python3 fix_resenas.py desde magama-web/")  