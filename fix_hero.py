#!/usr/bin/env python3
"""
Ejecutar en la carpeta magama-web/:
    python3 fix_hero.py

Hace cambios en index.html:
  1. Agrega IDs a los elementos del hero
  2. Agrega script para leer hero desde localStorage

Hace cambios en admin/index.html:
  3. Agrega formulario de hero en la sección Configuración
  4. Agrega JS para guardar/cargar hero
"""

import os

# ══════════════════════════════════════════════
# PATCH index.html
# ══════════════════════════════════════════════
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes_idx = 0

# FIX 1: Agregar IDs a los elementos del hero
OLD1 = '      <div class="hero-eyebrow"><i class="fas fa-star"></i> Colección 2025 disponible</div>'
NEW1 = '      <div class="hero-eyebrow" id="hero-eyebrow"><i class="fas fa-star"></i> <span id="hero-eyebrow-txt">Colección 2025 disponible</span></div>'
if OLD1 in idx:
    idx = idx.replace(OLD1, NEW1, 1)
    print("✅ IDX FIX 1: ID en eyebrow")
    fixes_idx += 1
else:
    print("⚠️  IDX FIX 1: eyebrow no encontrado")

OLD2 = '      <h1 class="hero-title">\n        Tu moda,<br>\n        <span class="hl">tu estilo</span><br>\n        <span class="accent-line">único.</span>\n      </h1>'
NEW2 = '      <h1 class="hero-title" id="hero-title">\n        <span id="hero-l1">Tu moda,</span><br>\n        <span class="hl" id="hero-hl">tu estilo</span><br>\n        <span class="accent-line" id="hero-l3">único.</span>\n      </h1>'
if OLD2 in idx:
    idx = idx.replace(OLD2, NEW2, 1)
    print("✅ IDX FIX 2: IDs en título hero")
    fixes_idx += 1
else:
    print("⚠️  IDX FIX 2: título hero no encontrado")

OLD3 = '      <p class="hero-desc">Descubre las últimas tendencias para mujer, hombre y niños. Prendas de calidad al mejor precio, directo a tus manos.</p>'
NEW3 = '      <p class="hero-desc" id="hero-desc">Descubre las últimas tendencias para mujer, hombre y niños. Prendas de calidad al mejor precio, directo a tus manos.</p>'
if OLD3 in idx:
    idx = idx.replace(OLD3, NEW3, 1)
    print("✅ IDX FIX 3: ID en descripción hero")
    fixes_idx += 1
else:
    print("⚠️  IDX FIX 3: descripción hero no encontrado")

OLD4 = '        <div class="bd-num">50%</div>\n        <div class="bd-txt">de descuento</div>'
NEW4 = '        <div class="bd-num" id="hero-badge-num">50%</div>\n        <div class="bd-txt" id="hero-badge-txt">de descuento</div>'
if OLD4 in idx:
    idx = idx.replace(OLD4, NEW4, 1)
    print("✅ IDX FIX 4: IDs en badge del hero")
    fixes_idx += 1
else:
    print("⚠️  IDX FIX 4: badge no encontrado")

OLD5 = '        <div class="card-label">Nueva Colección</div>'
NEW5 = '        <div class="card-label" id="hero-card-label">Nueva Colección</div>'
if OLD5 in idx:
    idx = idx.replace(OLD5, NEW5, 1)
    print("✅ IDX FIX 5: ID en card label")
    fixes_idx += 1
else:
    print("⚠️  IDX FIX 5: card label no encontrado")

# FIX 6: Agregar script de hero dinámico antes de favoritos.js
OLD6 = '<script src="js/favoritos.js"></script>'
NEW6 = '''<script>
/* ── Hero dinámico desde admin ── */
(function aplicarHero() {
  try {
    const raw = localStorage.getItem('magama_hero');
    if (!raw) return;
    const h = JSON.parse(raw);
    if (!h) return;
    const set = function(id, val) {
      const el = document.getElementById(id);
      if (el && val) el.textContent = val;
    };
    set('hero-eyebrow-txt', h.eyebrow);
    set('hero-l1',          h.l1);
    set('hero-hl',          h.hl);
    set('hero-l3',          h.l3);
    set('hero-desc',        h.desc);
    set('hero-badge-num',   h.badgeNum);
    set('hero-badge-txt',   h.badgeTxt);
    set('hero-card-label',  h.cardLabel);
  } catch(e) { /* silent */ }
})();
</script>
<script src="js/favoritos.js"></script>'''

if OLD6 in idx:
    idx = idx.replace(OLD6, NEW6, 1)
    print("✅ IDX FIX 6: script hero dinámico agregado")
    fixes_idx += 1
else:
    print("⚠️  IDX FIX 6: script favoritos.js no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ index.html: {fixes_idx}/6 fixes aplicados")

# ══════════════════════════════════════════════
# PATCH admin/index.html
# ══════════════════════════════════════════════
admin_path = 'admin/index.html'
if not os.path.exists(admin_path):
    print(f"\n⚠️  {admin_path} no encontrado — asegúrate de ejecutar desde magama-web/")
    exit()

with open(admin_path, 'r', encoding='utf-8') as f:
    adm = f.read()

fixes_adm = 0

# FIX A: Agregar sección Hero al final de la vista CONFIG (antes del cierre del panel)
OLD_A = '''          <div style="margin-top:20px;display:flex;justify-content:flex-end">
            <button class="btn-save" onclick="showToast('Configuración guardada correctamente')"><i class="fas fa-save"></i> Guardar Cambios</button>
          </div>
        </div>
      </div>
    </div>'''

NEW_A = '''          <div style="margin-top:20px;display:flex;justify-content:flex-end">
            <button class="btn-save" onclick="guardarConfig()"><i class="fas fa-save"></i> Guardar Cambios</button>
          </div>
        </div>
      </div>

      <!-- HERO DINÁMICO -->
      <div class="panel">
        <div class="panel-hdr">
          <div class="panel-title"><i class="fas fa-image"></i> Banner Principal (Hero)</div>
          <span style="font-size:.72rem;color:var(--g500)">Cambia el texto de la portada de tu tienda</span>
        </div>
        <div class="panel-body">
          <div class="form-grid">
            <div class="form-group form-full">
              <label class="form-label">Texto pequeño (eyebrow)</label>
              <input class="form-input" id="hero-cfg-eyebrow" placeholder="Ej: Colección 2025 disponible"/>
            </div>
            <div class="form-group">
              <label class="form-label">Título línea 1</label>
              <input class="form-input" id="hero-cfg-l1" placeholder="Ej: Tu moda,"/>
            </div>
            <div class="form-group">
              <label class="form-label">Título línea 2 (resaltada)</label>
              <input class="form-input" id="hero-cfg-hl" placeholder="Ej: tu estilo"/>
            </div>
            <div class="form-group">
              <label class="form-label">Título línea 3 (acento)</label>
              <input class="form-input" id="hero-cfg-l3" placeholder="Ej: único."/>
            </div>
            <div class="form-group form-full">
              <label class="form-label">Descripción</label>
              <textarea class="form-textarea" id="hero-cfg-desc" placeholder="Ej: Descubre las últimas tendencias..."></textarea>
            </div>
            <div class="form-group">
              <label class="form-label">Badge — número (ej: 50%)</label>
              <input class="form-input" id="hero-cfg-badge-num" placeholder="50%"/>
            </div>
            <div class="form-group">
              <label class="form-label">Badge — texto (ej: de descuento)</label>
              <input class="form-input" id="hero-cfg-badge-txt" placeholder="de descuento"/>
            </div>
            <div class="form-group">
              <label class="form-label">Etiqueta de la tarjeta</label>
              <input class="form-input" id="hero-cfg-card-label" placeholder="Nueva Colección"/>
            </div>
            <div class="form-group">
              <div style="background:var(--cream);border:1px solid var(--g200);border-radius:10px;padding:12px 14px;font-size:.78rem;color:var(--g500);">
                <i class="fas fa-info-circle" style="color:var(--sky)"></i>
                Deja en blanco los campos que no quieras cambiar.
              </div>
            </div>
          </div>
          <div style="margin-top:20px;display:flex;justify-content:flex-end">
            <button class="btn-save" onclick="guardarHero()"><i class="fas fa-save"></i> Guardar Hero</button>
          </div>
        </div>
      </div>
    </div>'''

if OLD_A in adm:
    adm = adm.replace(OLD_A, NEW_A, 1)
    print("\n✅ ADM FIX A: Sección Hero agregada en Configuración")
    fixes_adm += 1
else:
    print("\n⚠️  ADM FIX A: No encontrado el bloque de config")

# FIX B: Agregar funciones JS guardarConfig y guardarHero
OLD_B = "document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});"
NEW_B = """document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});

/* ─── CONFIGURACIÓN DE TIENDA ─── */
function guardarConfig(){
  showToast('Configuración guardada correctamente');
}

/* ─── HERO DINÁMICO ─── */
function guardarHero(){
  const get = function(id){ return document.getElementById(id).value.trim(); };
  const h = {
    eyebrow:   get('hero-cfg-eyebrow'),
    l1:        get('hero-cfg-l1'),
    hl:        get('hero-cfg-hl'),
    l3:        get('hero-cfg-l3'),
    desc:      get('hero-cfg-desc'),
    badgeNum:  get('hero-cfg-badge-num'),
    badgeTxt:  get('hero-cfg-badge-txt'),
    cardLabel: get('hero-cfg-card-label'),
  };
  /* Solo guardar campos que tienen valor */
  const hFiltrado = {};
  Object.keys(h).forEach(function(k){ if(h[k]) hFiltrado[k] = h[k]; });

  try {
    localStorage.setItem('magama_hero', JSON.stringify(hFiltrado));
    showToast('Banner hero guardado ✅ — recarga la tienda para ver los cambios');
  } catch(e) {
    showToast('Error al guardar el hero ⚠️', 'err');
  }
}

function cargarHeroAdmin(){
  try {
    const raw = localStorage.getItem('magama_hero');
    if (!raw) return;
    const h = JSON.parse(raw);
    const set = function(id, val){
      const el = document.getElementById(id);
      if(el && val) el.value = val;
    };
    set('hero-cfg-eyebrow',    h.eyebrow);
    set('hero-cfg-l1',         h.l1);
    set('hero-cfg-hl',         h.hl);
    set('hero-cfg-l3',         h.l3);
    set('hero-cfg-desc',       h.desc);
    set('hero-cfg-badge-num',  h.badgeNum);
    set('hero-cfg-badge-txt',  h.badgeTxt);
    set('hero-cfg-card-label', h.cardLabel);
  } catch(e) { /* silent */ }
}"""

if OLD_B in adm:
    adm = adm.replace(OLD_B, NEW_B, 1)
    print("✅ ADM FIX B: Funciones guardarHero y cargarHeroAdmin agregadas")
    fixes_adm += 1
else:
    print("⚠️  ADM FIX B: punto de inserción JS no encontrado")

# FIX C: Cargar hero al mostrar config
OLD_C = "  if(id==='inventario') renderInventario();\n  if(id==='dashboard')  renderDashboardRecents();"
NEW_C = "  if(id==='inventario') renderInventario();\n  if(id==='dashboard')  renderDashboardRecents();\n  if(id==='config')     cargarHeroAdmin();"
if OLD_C in adm:
    adm = adm.replace(OLD_C, NEW_C, 1)
    print("✅ ADM FIX C: cargarHeroAdmin() al abrir config")
    fixes_adm += 1
else:
    print("⚠️  ADM FIX C: showView no encontrado")

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(adm)

print(f"\n✅ admin/index.html: {fixes_adm}/3 fixes aplicados")
print("\n🎉 Listo. Abre el admin → Configuración → Banner Principal")