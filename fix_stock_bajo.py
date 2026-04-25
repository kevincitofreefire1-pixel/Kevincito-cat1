#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_stock_bajo.py
"""

# ══════════════════════════════════════════════
# PATCH index.html
# ══════════════════════════════════════════════
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes_idx = 0

# ── CSS indicador stock bajo ──
CSS_STOCK = """
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
    }
"""

OLD_CSS = "  </style>"
if OLD_CSS in idx:
    idx = idx.replace(OLD_CSS, CSS_STOCK + "\n  </style>", 1)
    print("✅ IDX: CSS stock bajo agregado")
    fixes_idx += 1
else:
    print("⚠️  IDX: </style> no encontrado")

# ── JS: agregar badge de stock bajo en renderProds ──
# Buscar la línea donde se construye el badge del producto
OLD_RENDER = """    const mayorHtml = p.precioMayor
      ? `<div style="font-size:.7rem;color:#06D6A0;font-weight:700;padding:4px 16px 0">Mayor x${p.cantidadMayor||6}+: S/ ${Number(p.precioMayor).toFixed(2)}</div>` : '';
    const thumbContent = imagen
      ? `<img src="${imagen}" alt="${nombre}" style="width:100%;height:100%;object-fit:cover;position:absolute;inset:0" onerror="this.style.display='none'">`
      : `<span class="pemoji">${p.emoji||'👕'}</span>`;
    return `
    <div class="prod-card">
      <div class="prod-thumb" style="background:${p.bg||'#dbeafe'};position:relative;cursor:pointer" onclick="abrirDetalle(${p.id})">
        ${thumbContent}
        ${badge ? `<span class="ptag ptag-${badge}">${tagTxt}</span>` : ''}
        <button class="pwish" onclick="event.stopPropagation();toggleWishlist(this)"><i class="far fa-heart"></i></button>
      </div>"""

NEW_RENDER = """    const mayorHtml = p.precioMayor
      ? `<div style="font-size:.7rem;color:#06D6A0;font-weight:700;padding:4px 16px 0">Mayor x${p.cantidadMayor||6}+: S/ ${Number(p.precioMayor).toFixed(2)}</div>` : '';
    const thumbContent = imagen
      ? `<img src="${imagen}" alt="${nombre}" style="width:100%;height:100%;object-fit:cover;position:absolute;inset:0" onerror="this.style.display='none'">`
      : `<span class="pemoji">${p.emoji||'👕'}</span>`;
    /* Stock bajo */
    const limiteStock = Number(localStorage.getItem('magama_stock_limite') || 5);
    const stockNum    = (p.stockUnidades !== undefined && p.stockUnidades !== null) ? Number(p.stockUnidades) : null;
    const esStockBajo = stockNum !== null && stockNum > 0 && stockNum <= limiteStock;
    const stockBadge  = esStockBajo
      ? `<span class="stock-low-badge"><i class="fas fa-fire"></i> ¡Solo ${stockNum} unidades!</span>` : '';
    return `
    <div class="prod-card${esStockBajo ? ' stock-low' : ''}">
      <div class="prod-thumb" style="background:${p.bg||'#dbeafe'};position:relative;cursor:pointer" onclick="abrirDetalle(${p.id})">
        ${thumbContent}
        ${badge ? `<span class="ptag ptag-${badge}">${tagTxt}</span>` : ''}
        ${stockBadge}
        <button class="pwish" onclick="event.stopPropagation();toggleWishlist(this)"><i class="far fa-heart"></i></button>
      </div>"""

if OLD_RENDER in idx:
    idx = idx.replace(OLD_RENDER, NEW_RENDER, 1)
    print("✅ IDX: badge stock bajo en tarjetas")
    fixes_idx += 1
else:
    print("⚠️  IDX: bloque renderProds no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ index.html: {fixes_idx}/2 fixes")

# ══════════════════════════════════════════════
# PATCH admin/index.html
# ══════════════════════════════════════════════
import os
admin_path = 'admin/index.html'
if not os.path.exists(admin_path):
    print("\n⚠️  admin/index.html no encontrado")
    exit()

with open(admin_path, 'r', encoding='utf-8') as f:
    adm = f.read()

fixes_adm = 0

# ── Agregar campo stockUnidades en el formulario del modal ──
OLD_FORM = """        <!-- Notas adicionales -->
        <div class="form-group form-full">
          <label class="form-label">Notas adicionales</label>
          <textarea class="form-textarea" id="f-notes" placeholder="Ej: Viene en talla estándar peruana, lavado a mano recomendado..."></textarea>
        </div>"""

NEW_FORM = """        <!-- Stock unidades -->
        <div class="form-group">
          <label class="form-label">
            <i class="fas fa-boxes" style="color:var(--accent);margin-right:4px"></i>
            Unidades en stock
          </label>
          <input class="form-input" id="f-stock-unidades" type="number" min="0" step="1" placeholder="Ej: 3 (deja vacío si no aplica)"/>
          <div style="font-size:.7rem;color:var(--g500);margin-top:4px">
            <i class="fas fa-info-circle" style="color:var(--sky)"></i>
            Si hay pocas unidades, aparecerá una alerta roja en la tarjeta del producto.
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Estado de stock</label>
          <div class="toggle-row" style="margin-top:12px">
            <label class="toggle-switch">
              <input type="checkbox" id="f-stock" checked/>
              <span class="toggle-track"></span>
            </label>
            <span class="toggle-lbl">Disponible en stock</span>
          </div>
        </div>

        <!-- Notas adicionales -->
        <div class="form-group form-full">
          <label class="form-label">Notas adicionales</label>
          <textarea class="form-textarea" id="f-notes" placeholder="Ej: Viene en talla estándar peruana, lavado a mano recomendado..."></textarea>
        </div>"""

# Necesitamos quitar el toggle stock duplicado
OLD_TOGGLE = """        <div class="form-group">
          <label class="form-label">Estado de stock</label>
          <div class="toggle-row" style="margin-top:12px">
            <label class="toggle-switch">
              <input type="checkbox" id="f-stock" checked/>
              <span class="toggle-track"></span>
            </label>
            <span class="toggle-lbl">Disponible en stock</span>
          </div>
        </div>

        <!-- Notas adicionales -->"""

if OLD_TOGGLE in adm:
    adm = adm.replace(OLD_TOGGLE, """        <!-- Notas adicionales -->""", 1)
    print("\n✅ ADM: toggle stock movido")

if OLD_FORM in adm:
    adm = adm.replace(OLD_FORM, NEW_FORM, 1)
    print("✅ ADM: campo stockUnidades agregado al modal")
    fixes_adm += 1
else:
    print("⚠️  ADM: bloque notas no encontrado")

# ── Guardar stockUnidades en guardarProducto ──
OLD_GUARDAR = """    const prod={
    id: editId||Date.now(),
    name,cat,subcat:sub,emoji,bg:selBg,
    tag:selTagVal||null,price:pr,old,
    precioMayor,cantidadMayor,
    desc:document.getElementById('f-desc').value.trim(),
    tallas,colores,
    stock:document.getElementById('f-stock').checked,
    notes:document.getElementById('f-notes').value.trim(),"""

NEW_GUARDAR = """  const stockUnidades = document.getElementById('f-stock-unidades').value !== ''
    ? parseInt(document.getElementById('f-stock-unidades').value)
    : null;

  const prod={
    id: editId||Date.now(),
    name,cat,subcat:sub,emoji,bg:selBg,
    tag:selTagVal||null,price:pr,old,
    precioMayor,cantidadMayor,
    desc:document.getElementById('f-desc').value.trim(),
    tallas,colores,
    stock:document.getElementById('f-stock').checked,
    stockUnidades,
    notes:document.getElementById('f-notes').value.trim(),"""

if OLD_GUARDAR in adm:
    adm = adm.replace(OLD_GUARDAR, NEW_GUARDAR, 1)
    print("✅ ADM: stockUnidades guardado en producto")
    fixes_adm += 1
else:
    print("⚠️  ADM: guardarProducto no encontrado")

# ── Restaurar stockUnidades al editar ──
OLD_EDIT = "  document.getElementById('f-mayor-qty').value  =p.cantidadMayor||'';\n  document.getElementById('f-mayor-price').value=p.precioMayor||'';"
NEW_EDIT = "  document.getElementById('f-mayor-qty').value  =p.cantidadMayor||'';\n  document.getElementById('f-mayor-price').value=p.precioMayor||'';\n  document.getElementById('f-stock-unidades').value = p.stockUnidades !== null && p.stockUnidades !== undefined ? p.stockUnidades : '';"
if OLD_EDIT in adm:
    adm = adm.replace(OLD_EDIT, NEW_EDIT, 1)
    print("✅ ADM: stockUnidades restaurado al editar")
    fixes_adm += 1
else:
    print("⚠️  ADM: editarProducto no encontrado")

# ── Agregar límite configurable en sección Config ──
OLD_CFG = """            <div class="form-group form-full"><label class="form-label">Mensaje de anuncio (barra superior)</label><input class="form-input" value="🌊 Nueva colección disponible | 📦 Envíos a toda la ciudad | 🔥 Ofertas especiales" id="cfg-ann"/></div>"""
NEW_CFG = """            <div class="form-group form-full"><label class="form-label">Mensaje de anuncio (barra superior)</label><input class="form-input" value="🌊 Nueva colección disponible | 📦 Envíos a toda la ciudad | 🔥 Ofertas especiales" id="cfg-ann"/></div>
            <div class="form-group">
              <label class="form-label">
                <i class="fas fa-fire" style="color:var(--accent);margin-right:4px"></i>
                Límite "Últimas unidades" <span style="font-size:.7rem;color:var(--g500);font-weight:400">(unidades para mostrar alerta)</span>
              </label>
              <input class="form-input" type="number" min="1" max="20" id="cfg-stock-limite" value="5" placeholder="5"/>
              <div style="font-size:.7rem;color:var(--g500);margin-top:4px">Si un producto tiene ≤ este número de unidades, aparece la alerta roja.</div>
            </div>"""
if OLD_CFG in adm:
    adm = adm.replace(OLD_CFG, NEW_CFG, 1)
    print("✅ ADM: límite stock en Configuración")
    fixes_adm += 1
else:
    print("⚠️  ADM: campo cfg-ann no encontrado")

# ── Guardar límite en guardarConfig ──
OLD_GC = "function guardarConfig(){\n  showToast('Configuración guardada correctamente');\n}"
NEW_GC = """function guardarConfig(){
  const limite = document.getElementById('cfg-stock-limite');
  if(limite && limite.value){
    localStorage.setItem('magama_stock_limite', limite.value);
  }
  showToast('Configuración guardada correctamente');
}"""
if OLD_GC in adm:
    adm = adm.replace(OLD_GC, NEW_GC, 1)
    print("✅ ADM: guardarConfig guarda límite stock")
    fixes_adm += 1
else:
    print("⚠️  ADM: guardarConfig no encontrado")

# ── Cargar límite al abrir config ──
OLD_CHA = """function cargarHeroAdmin(){"""
NEW_CHA = """function cargarHeroAdmin(){
  /* Cargar límite stock */
  const limite = localStorage.getItem('magama_stock_limite');
  const elLimite = document.getElementById('cfg-stock-limite');
  if(limite && elLimite) elLimite.value = limite;
"""
if OLD_CHA in adm:
    adm = adm.replace(OLD_CHA, NEW_CHA, 1)
    print("✅ ADM: límite stock cargado en cargarHeroAdmin")
    fixes_adm += 1
else:
    print("⚠️  ADM: cargarHeroAdmin no encontrado")

# ── Resetear campo al resetear formulario ──
OLD_RESET = "  document.getElementById('f-mayor-qty').value  ='';\n  document.getElementById('f-mayor-price').value='';"
NEW_RESET = "  document.getElementById('f-mayor-qty').value  ='';\n  document.getElementById('f-mayor-price').value='';\n  document.getElementById('f-stock-unidades').value='';"
if OLD_RESET in adm:
    adm = adm.replace(OLD_RESET, NEW_RESET, 1)
    print("✅ ADM: resetForm limpia stockUnidades")
    fixes_adm += 1
else:
    print("⚠️  ADM: resetForm mayor no encontrado")

with open(admin_path, 'w', encoding='utf-8') as f:
    f.write(adm)

print(f"\n✅ admin/index.html: {fixes_adm}/7 fixes")
print("\n🎉 Listo.")