/* ============================================================
   MAGAMA — producto-detalle.js
   Modal de detalle · Galería múltiple · También te puede gustar
   URL con hash · Compartir por WhatsApp
   ============================================================ */
'use strict';

/* ── Inyectar estilos ── */
(function inyectarEstilos() {
  const style = document.createElement('style');
  style.id = 'magama-detalle-css';
  style.textContent = `
    #detalleOverlay {
      position: fixed; inset: 0; z-index: 1400;
      background: rgba(3,4,94,.55);
      backdrop-filter: blur(8px);
      display: none; align-items: center; justify-content: center;
      padding: 16px;
      animation: detalleFadeIn .22s ease;
    }
    #detalleOverlay.open { display: flex; }
    @keyframes detalleFadeIn { from{opacity:0} to{opacity:1} }

    #detalleCard {
      background: #F8FBFF;
      border-radius: 20px;
      width: 100%; max-width: 900px;
      max-height: 92vh;
      overflow-y: auto;
      box-shadow: 0 32px 80px rgba(3,4,94,.3);
      animation: detalleSlideUp .28s cubic-bezier(.34,1.56,.64,1);
      position: relative;
      display: grid;
      grid-template-columns: 1fr 1fr;
      scrollbar-width: thin;
      scrollbar-color: #D5DDEF transparent;
    }
    @keyframes detalleSlideUp {
      from { opacity:0; transform: translateY(40px) scale(.97); }
      to   { opacity:1; transform: translateY(0)   scale(1);   }
    }
    #detalleCard::-webkit-scrollbar { width: 4px; }
    #detalleCard::-webkit-scrollbar-thumb { background:#D5DDEF; border-radius:2px; }

    #detalleCls {
      position: absolute; top: 14px; right: 14px; z-index: 10;
      width: 36px; height: 36px; border-radius: 50%;
      background: rgba(255,255,255,.9); border: none; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      color: #6B7FA3; font-size: .95rem;
      box-shadow: 0 2px 10px rgba(3,4,94,.15);
      transition: all .2s;
    }
    #detalleCls:hover { background:#fff; color:#FF6B6B; transform:scale(1.08); }

    .det-galeria {
      background: #EEF5FF;
      border-radius: 20px 0 0 20px;
      display: flex; flex-direction: column;
      padding: 24px 20px; gap: 14px;
      position: sticky; top: 0;
      align-self: start;
    }
    .det-img-main {
      width: 100%; aspect-ratio: 3/4;
      border-radius: 14px; overflow: hidden;
      background: #fff;
      display: flex; align-items: center; justify-content: center;
      position: relative;
    }
    .det-img-main img {
      width: 100%; height: 100%; object-fit: cover;
      transition: opacity .22s ease, transform .4s ease;
    }
    .det-img-main img.changing { opacity: 0; }
    .det-img-main:hover img { transform: scale(1.04); }
    .det-img-main .det-emoji-big {
      font-size: 8rem; user-select: none;
      transition: transform .3s;
    }
    .det-img-main:hover .det-emoji-big { transform: scale(1.07); }

    .det-badge-off {
      position: absolute; top: 12px; left: 12px;
      background: #FF6B6B; color: #fff;
      font-size: .72rem; font-weight: 800;
      padding: 4px 10px; border-radius: 20px;
      letter-spacing: .06em;
    }

    .det-thumbs { display: flex; gap: 8px; flex-wrap: wrap; }
    .det-thumb {
      width: 62px; height: 68px; border-radius: 10px;
      overflow: hidden; cursor: pointer;
      border: 2.5px solid transparent;
      background: #fff;
      display: flex; align-items: center; justify-content: center;
      font-size: 1.6rem;
      transition: border-color .2s, transform .2s, box-shadow .2s;
      flex-shrink: 0;
    }
    .det-thumb img { width:100%; height:100%; object-fit:cover; }
    .det-thumb.active { border-color: #0077B6; transform: scale(1.06); box-shadow: 0 3px 10px rgba(0,119,182,.25); }
    .det-thumb:hover  { border-color: #00B4D8; }

    .det-info {
      padding: 28px 28px 28px 24px;
      display: flex; flex-direction: column; gap: 0;
    }

    .det-breadcrumb {
      display: flex; align-items: center; gap: 5px;
      font-size: .72rem; color: #6B7FA3; margin-bottom: 12px;
    }
    .det-breadcrumb span { color: #0077B6; cursor: pointer; }
    .det-breadcrumb span:hover { text-decoration: underline; }
    .det-breadcrumb i { font-size: .55rem; color: #B0BEDB; }

    .det-cat-badge {
      display: inline-flex; align-items: center; gap: 5px;
      background: rgba(0,119,182,.08); color: #0077B6;
      font-size: .68rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; padding: 4px 12px; border-radius: 20px;
      margin-bottom: 10px; width: fit-content;
    }

    .det-nombre {
      font-family: 'Playfair Display', serif;
      font-size: 1.65rem; font-weight: 900;
      color: #03045E; line-height: 1.15;
      margin-bottom: 6px;
    }

    .det-subcat { font-size: .78rem; color: #6B7FA3; margin-bottom: 16px; }

    .det-precio-wrap {
      display: flex; align-items: baseline; gap: 10px;
      margin-bottom: 6px;
    }
    .det-precio-actual {
      font-family: 'Playfair Display', serif;
      font-size: 2rem; font-weight: 900; color: #03045E;
    }
    .det-precio-antes { font-size: 1rem; color: #B0BEDB; text-decoration: line-through; }
    .det-ahorro {
      font-size: .75rem; font-weight: 700;
      background: rgba(6,214,160,.12); color: #039d76;
      padding: 3px 9px; border-radius: 20px;
    }

    .det-precio-mayor {
      display: inline-flex; align-items: center; gap: 6px;
      background: linear-gradient(135deg,rgba(0,180,216,.08),rgba(0,119,182,.06));
      border: 1px solid rgba(0,119,182,.18);
      border-radius: 8px; padding: 7px 12px;
      font-size: .78rem; color: #0077B6; font-weight: 600;
      margin-bottom: 16px;
    }
    .det-precio-mayor i { color: #00B4D8; }
    .det-precio-mayor strong { color: #03045E; }

    .det-divider { border: none; border-top: 1px solid #EFF3FA; margin: 14px 0; }

    .det-sec-label {
      font-size: .72rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: #6B7FA3; margin-bottom: 9px;
      display: flex; align-items: center; gap: 7px;
    }
    .det-sec-label .det-seleccionado {
      font-size: .72rem; font-weight: 700; color: #03045E;
      text-transform: none; letter-spacing: 0;
      background: #EFF3FA; padding: 2px 8px; border-radius: 20px;
    }

    .det-tallas { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
    .det-talla-chip {
      min-width: 46px; height: 40px; padding: 0 14px;
      border-radius: 10px; border: 1.5px solid #D5DDEF;
      background: #fff; font-size: .85rem; font-weight: 600;
      color: #6B7FA3; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: all .18s; user-select: none;
    }
    .det-talla-chip:hover   { border-color: #0077B6; color: #03045E; }
    .det-talla-chip.on      { background: #03045E; color: #fff; border-color: #03045E; }

    .det-colores { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
    .det-color-chip {
      display: flex; align-items: center; gap: 6px;
      padding: 7px 13px; border-radius: 10px;
      border: 1.5px solid #D5DDEF; background: #fff;
      font-size: .82rem; font-weight: 500; color: #6B7FA3;
      cursor: pointer; transition: all .18s; user-select: none;
    }
    .det-color-chip:hover { border-color: #0077B6; color: #03045E; }
    .det-color-chip.on    { border-color: #0077B6; background: #EEF5FF; color: #03045E; }
    .det-color-dot { width: 15px; height: 15px; border-radius: 50%; border: 1px solid rgba(0,0,0,.12); flex-shrink: 0; }

    .det-aviso-multi {
      background: #EEF5FF; border-left: 3px solid #00B4D8;
      border-radius: 6px; padding: 8px 12px; margin-bottom: 14px;
      font-size: .74rem; color: #334166; line-height: 1.5;
    }
    .det-aviso-multi i { color: #00B4D8; margin-right: 5px; }

    .det-qty-wrap { display: flex; align-items: center; gap: 14px; margin-bottom: 18px; }
    .det-qty {
      display: flex; align-items: center; gap: 0;
      border: 1.5px solid #D5DDEF; border-radius: 12px;
      overflow: hidden; background: #fff;
    }
    .det-qty button {
      width: 40px; height: 42px; border: none;
      background: transparent; cursor: pointer;
      font-size: .9rem; color: #03045E;
      transition: background .15s;
    }
    .det-qty button:hover { background: #EEF5FF; }
    .det-qty span {
      min-width: 42px; text-align: center;
      font-weight: 700; font-size: 1rem; color: #03045E;
      border-left: 1px solid #EFF3FA; border-right: 1px solid #EFF3FA;
      line-height: 42px;
    }
    .det-qty-label { font-size: .78rem; color: #6B7FA3; }

    .det-acciones { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
    .det-btn-carrito {
      width: 100%; padding: 15px;
      background: linear-gradient(135deg, #0077B6, #00B4D8);
      color: #fff; border: none; border-radius: 14px;
      font-size: .95rem; font-weight: 700; cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 10px;
      box-shadow: 0 6px 20px rgba(0,119,182,.35);
      transition: all .2s;
    }
    .det-btn-carrito:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(0,119,182,.5); }
    .det-btn-wa {
      width: 100%; padding: 13px;
      background: linear-gradient(135deg, #128C7E, #25D366);
      color: #fff; border: none; border-radius: 14px;
      font-size: .9rem; font-weight: 700; cursor: pointer;
      display: flex; align-items: center; justify-content: center; gap: 10px;
      box-shadow: 0 4px 16px rgba(37,211,102,.3);
      transition: all .2s;
    }
    .det-btn-wa:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(37,211,102,.5); }

    .det-total-preview {
      text-align: center; font-size: .78rem; color: #6B7FA3;
      padding: 8px 0; background: #EFF3FA; border-radius: 10px;
      margin-bottom: 14px;
    }
    .det-total-preview strong { color: #03045E; font-size: .95rem; }

    .det-desc { font-size: .84rem; color: #6B7FA3; line-height: 1.75; margin-bottom: 16px; }

    .det-features { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 6px; }
    .det-feat { display: flex; align-items: center; gap: 7px; font-size: .75rem; color: #6B7FA3; }
    .det-feat i { color: #00B4D8; font-size: .8rem; width: 14px; }

    /* ── También te puede gustar ── */
    .det-tmb {
      grid-column: 1 / -1;
      border-top: 1px solid #EFF3FA;
      padding: 22px 28px 28px;
      background: #F8FBFF;
    }
    .det-tmb-title {
      font-family: 'Playfair Display', serif;
      font-size: 1.05rem; font-weight: 700;
      color: #03045E; margin-bottom: 16px;
      display: flex; align-items: center; gap: 8px;
    }
    .det-tmb-title i { color: #00B4D8; font-size: .9rem; }
    .det-tmb-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
    .det-tmb-card {
      border-radius: 12px; overflow: hidden;
      border: 1.5px solid #D5DDEF;
      background: #fff; cursor: pointer;
      transition: transform .2s, box-shadow .2s, border-color .2s;
    }
    .det-tmb-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(3,4,94,.12); border-color: #00B4D8; }
    .det-tmb-thumb {
      height: 100px;
      display: flex; align-items: center; justify-content: center;
      font-size: 2.6rem; overflow: hidden; position: relative;
    }
    .det-tmb-thumb img { width: 100%; height: 100%; object-fit: cover; transition: transform .3s; }
    .det-tmb-card:hover .det-tmb-thumb img { transform: scale(1.06); }
    .det-tmb-body { padding: 8px 10px 10px; }
    .det-tmb-nombre { font-size: .78rem; font-weight: 700; color: #03045E; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 3px; }
    .det-tmb-precio { font-family: 'Playfair Display', serif; font-size: .88rem; font-weight: 700; color: #03045E; }
    .det-tmb-viejo { font-size: .68rem; color: #B0BEDB; text-decoration: line-through; margin-left: 4px; }

    @media (max-width: 640px) {
      #detalleCard {
        grid-template-columns: 1fr;
        max-height: 95vh;
        border-radius: 16px 16px 0 0;
      }
      .det-galeria { border-radius: 16px 16px 0 0; position: static; }
      .det-img-main { aspect-ratio: 4/3; }
      .det-info { padding: 20px; }
      .det-nombre { font-size: 1.35rem; }
      .det-tmb { padding: 18px 20px 22px; }
      .det-tmb-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    }
  `;
  document.head.appendChild(style);
})();

/* ── Inyectar HTML del modal ── */
(function inyectarHTML() {
  const div = document.createElement('div');
  div.id = 'detalleOverlay';
  div.innerHTML = '<div id="detalleCard"></div>';
  div.addEventListener('click', function(e) {
    if (e.target === div) cerrarDetalle();
  });
  document.body.appendChild(div);
})();

/* ── Estado del modal ── */
var detalleProd        = null;
var detalleTallasSet   = new Set();
var detalleColoresSet  = new Set();
var detalleQty         = 1;

/* ════════════════════════════════════════════════════
   ABRIR / CERRAR DETALLE
   ════════════════════════════════════════════════════ */
function abrirDetalle(prodId) {
  var todos = typeof obtenerProductosActuales === 'function'
    ? obtenerProductosActuales()
    : (typeof products !== 'undefined' ? products : []);
  var p = todos.find(function(x) { return x.id == prodId; });
  if (!p) return;

  detalleProd       = p;
  detalleTallasSet  = new Set();
  detalleColoresSet = new Set();
  detalleQty        = 1;

  renderDetalleCard();
  document.getElementById('detalleOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';

  /* URL con hash para compartir */
  var nombre = (p.nombre || p.name || '').toLowerCase()
    .replace(/[áàä]/g,'a').replace(/[éèë]/g,'e')
    .replace(/[íìï]/g,'i').replace(/[óòö]/g,'o')
    .replace(/[úùü]/g,'u').replace(/ñ/g,'n')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
  history.pushState({ prodId: prodId }, '', '#producto-' + prodId + '-' + nombre);
  document.title = (p.nombre || p.name || 'Producto') + ' | MAGAMA';
}

function cerrarDetalle() {
  document.getElementById('detalleOverlay').classList.remove('open');
  document.body.style.overflow = '';
  detalleProd = null;
  if (window.location.hash.startsWith('#producto-')) {
    history.pushState(null, '', window.location.pathname);
    document.title = 'MAGAMA | Moda & Estilo';
  }
}

/* ════════════════════════════════════════════════════
   RENDERIZAR EL CARD
   ════════════════════════════════════════════════════ */
function renderDetalleCard() {
  var p = detalleProd;
  if (!p) return;

  var nombre    = p.nombre      || p.name        || '';
  var cat       = p.categoria   || p.cat         || '';
  var subcat    = p.subcategoria|| p.subcat       || '';
  var precio    = Number(p.precio || p.price || 0);
  var viejo     = p.precioAntes || p.old          || null;
  var badge     = p.badge       || p.tag          || null;
  var imagen    = p.imagen      || '';
  var emoji     = p.emoji       || '👕';
  var bg        = p.bg          || '#dbeafe';
  var desc      = p.descripcion || p.desc         || '';
  var tallas    = p.tallas      || [];
  var colores   = p.colores     || [];
  var stock     = p.stock !== undefined ? p.stock : true;
  var mayor     = p.precioMayor    ? Number(p.precioMayor)    : null;
  var cantMayor = p.cantidadMayor  ? Number(p.cantidadMayor)  : null;

  var catLabels  = {mujer:'Mujer',hombre:'Hombre',ninos:'Niños',ofertas:'Ofertas'};
  var subLabels  = {
    'polo-bodi':'Polo Bodi','polo-oversize':'Polo Oversize','polo-top':'Top',
    'pantalon-overol':'Overol','pantalon-varios':'Pantalón','chompa':'Chompa',
    'enterizo':'Enterizo','vestido':'Vestido',
    'polo-h':'Polo','casaca':'Casaca','pantalon-h':'Pantalón','camisa-h':'Camisa',
    'polo-n':'Polo Niño','pantalon-n':'Pantalón Niño','camisa-n':'Camisa Niño',
  };
  var catNombre    = catLabels[cat]   || cat;
  var subcatNombre = subLabels[subcat] || subcat;
  var pctOff = viejo ? Math.round((1 - precio / viejo) * 100) : 0;

  /* Galería múltiple */
  var galeria = (p.imagenes && p.imagenes.length > 0)
    ? p.imagenes
    : (imagen ? [imagen] : []);
  var imgPrincipal = galeria[0] || '';

  var imgMainHTML = imgPrincipal
    ? '<img id="detImgMain" src="' + imgPrincipal + '" alt="' + nombre + '">'
    : '<span class="det-emoji-big">' + emoji + '</span>';

  var thumbsHTML = galeria.length > 0
    ? galeria.map(function(src, i) {
        return '<div class="det-thumb ' + (i===0?'active':'') + '" onclick="cambiarFotoDetalle(this,\'' + src + '\')">' +
          '<img src="' + src + '" alt="' + nombre + ' foto ' + (i+1) + '">' +
        '</div>';
      }).join('')
    : '<div class="det-thumb active" style="background:' + bg + '"><span style="font-size:1.4rem">' + emoji + '</span></div>';

  /* Tallas */
  var tallasHTML = tallas.length
    ? tallas.map(function(t) {
        return '<div class="det-talla-chip" data-talla="' + t + '" onclick="detalleToggleTalla(this,\'' + t + '\')">' + t + '</div>';
      }).join('')
    : '<span style="font-size:.82rem;color:#6B7FA3">Talla única</span>';

  /* Colores */
  var coloresHTML = colores.length
    ? colores.map(function(c) {
        var hex = typeof hexDeColor === 'function' ? hexDeColor(c) : '#888';
        return '<div class="det-color-chip" data-color="' + c + '" onclick="detalleToggleColor(this,\'' + c + '\')">' +
          '<span class="det-color-dot" style="background:' + hex + '"></span>' + c +
        '</div>';
      }).join('')
    : '<span style="font-size:.82rem;color:#6B7FA3">Color único</span>';

  var mayorHTML = mayor && cantMayor
    ? '<div class="det-precio-mayor"><i class="fas fa-boxes"></i> Precio mayor: comprando <strong>' + cantMayor + '+ unidades → S/ ' + mayor.toFixed(2) + ' c/u</strong></div>'
    : '';

  var avisoHTML = (tallas.length > 0 || colores.length > 0)
    ? '<div class="det-aviso-multi"><i class="fas fa-info-circle"></i> Puedes elegir <strong>varias tallas y colores</strong> a la vez.</div>'
    : '';

  var descHTML = desc
    ? '<hr class="det-divider"><div class="det-desc">' + desc + '</div>'
    : '';

  var stockHTML = stock
    ? '<span style="color:#039d76;font-size:.75rem;font-weight:700"><i class="fas fa-circle" style="font-size:.5rem;margin-right:4px"></i>En stock</span>'
    : '<span style="color:#FF6B6B;font-size:.75rem;font-weight:700"><i class="fas fa-circle" style="font-size:.5rem;margin-right:4px"></i>Sin stock</span>';

  document.getElementById('detalleCard').innerHTML =
    '<button id="detalleCls" onclick="cerrarDetalle()"><i class="fas fa-times"></i></button>' +

    '<div class="det-galeria">' +
      '<div class="det-img-main" style="background:' + bg + '">' +
        imgMainHTML +
        (pctOff > 0 ? '<span class="det-badge-off">-' + pctOff + '% OFF</span>' : '') +
      '</div>' +
      '<div class="det-thumbs">' + thumbsHTML + '</div>' +
    '</div>' +

    '<div class="det-info">' +
      '<div class="det-breadcrumb">' +
        '<span onclick="cerrarDetalle();catFilter&&catFilter(\'' + cat + '\')">' + catNombre + '</span>' +
        '<i class="fas fa-chevron-right"></i>' +
        '<span>' + subcatNombre + '</span>' +
        '<i class="fas fa-chevron-right"></i>' +
        '<span style="color:#B0BEDB;cursor:default">' + nombre + '</span>' +
      '</div>' +
      '<div class="det-cat-badge"><i class="fas fa-tag"></i> ' + catNombre + ' · ' + subcatNombre + '</div>' +
      '<h2 class="det-nombre">' + nombre + '</h2>' +
      '<div style="margin-bottom:12px">' + stockHTML + '</div>' +
      '<div class="det-precio-wrap">' +
        '<span class="det-precio-actual">S/ ' + precio.toFixed(2) + '</span>' +
        (viejo ? '<span class="det-precio-antes">S/ ' + Number(viejo).toFixed(2) + '</span>' : '') +
        (pctOff > 0 ? '<span class="det-ahorro">Ahorras ' + pctOff + '%</span>' : '') +
      '</div>' +
      mayorHTML +
      '<hr class="det-divider">' +
      avisoHTML +
      (tallas.length ? '<div class="det-sec-label">TALLA <span style="color:#FF6B6B">*</span><span class="det-seleccionado" id="det-talla-lbl"></span></div><div class="det-tallas" id="det-tallas-wrap">' + tallasHTML + '</div>' : '') +
      (colores.length ? '<div class="det-sec-label">COLOR <span style="color:#FF6B6B">*</span><span class="det-seleccionado" id="det-color-lbl"></span></div><div class="det-colores" id="det-colores-wrap">' + coloresHTML + '</div>' : '') +
      '<div class="det-sec-label">CANTIDAD</div>' +
      '<div class="det-qty-wrap">' +
        '<div class="det-qty">' +
          '<button onclick="detalleQtyChange(-1)"><i class="fas fa-minus"></i></button>' +
          '<span id="det-qty-val">1</span>' +
          '<button onclick="detalleQtyChange(1)"><i class="fas fa-plus"></i></button>' +
        '</div>' +
        '<span class="det-qty-label" id="det-qty-label">1 unidad</span>' +
      '</div>' +
      '<div class="det-total-preview" id="det-total-preview">Total: <strong>S/ ' + precio.toFixed(2) + '</strong></div>' +
      '<div class="det-acciones">' +
        '<button class="det-btn-carrito" onclick="detalleAgregarAlCarrito()"><i class="fas fa-shopping-bag"></i> Agregar al carrito</button>' +
        '<button class="det-btn-wa" onclick="detalleConsultarWA()"><i class="fab fa-whatsapp"></i> Consultar por WhatsApp</button>' +
        '<button onclick="compartirProducto()" style="width:100%;padding:11px;border-radius:14px;border:1.5px solid #D5DDEF;background:#fff;font-size:.85rem;font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;color:#334166;transition:all .2s;" onmouseover="this.style.borderColor=\'#25D366\';this.style.color=\'#128C7E\'" onmouseout="this.style.borderColor=\'#D5DDEF\';this.style.color=\'#334166\'">' +
          '<i class="fas fa-share-alt" style="color:#25D366"></i> Compartir este producto' +
        '</button>' +
      '</div>' +
      '<div class="det-features">' +
        '<div class="det-feat"><i class="fas fa-shield-alt"></i> Calidad garantizada</div>' +
        '<div class="det-feat"><i class="fab fa-whatsapp"></i> Atención por WhatsApp</div>' +
        '<div class="det-feat"><i class="fas fa-exchange-alt"></i> Cambios disponibles</div>' +
        '<div class="det-feat"><i class="fas fa-tags"></i> Precio al por mayor</div>' +
      '</div>' +
      descHTML +
    '</div>' +

    '<div class="det-tmb" id="det-tmb-wrap"></div>';

  /* Renderizar sugeridos */
  setTimeout(function() { renderSugeridos(p); }, 50);
}

/* ════════════════════════════════════════════════════
   TAMBIÉN TE PUEDE GUSTAR
   ════════════════════════════════════════════════════ */
function renderSugeridos(prodActual) {
  var wrap = document.getElementById('det-tmb-wrap');
  if (!wrap) return;

  var todos = typeof obtenerProductosActuales === 'function'
    ? obtenerProductosActuales()
    : (typeof products !== 'undefined' ? products : []);

  var catActual    = prodActual.categoria || prodActual.cat || '';
  var subcatActual = prodActual.subcategoria || prodActual.subcat || '';

  var sugeridos = todos.filter(function(p) {
    if (p.id === prodActual.id) return false;
    return (p.subcategoria || p.subcat) === subcatActual;
  });

  if (sugeridos.length < 4) {
    var extras = todos.filter(function(p) {
      if (p.id === prodActual.id) return false;
      if (sugeridos.find(function(s) { return s.id === p.id; })) return false;
      return (p.categoria || p.cat) === catActual;
    });
    sugeridos = sugeridos.concat(extras);
  }

  sugeridos = sugeridos.sort(function() { return Math.random() - 0.5; }).slice(0, 4);

  if (!sugeridos.length) { wrap.style.display = 'none'; return; }

  var tarjetasHTML = sugeridos.map(function(p) {
    var n  = p.nombre  || p.name  || '';
    var pr = Number(p.precio || p.price || 0);
    var vj = p.precioAntes || p.old || null;
    var im = p.imagenes && p.imagenes[0] ? p.imagenes[0] : (p.imagen || '');
    var em = p.emoji || '👕';
    var bk = p.bg    || '#dbeafe';

    var th = im
      ? '<img src="' + im + '" alt="' + n + '" style="width:100%;height:100%;object-fit:cover;" onerror="this.style.display=\'none\'">'
      : '<span style="font-size:2.6rem">' + em + '</span>';

    var vH = vj ? '<span class="det-tmb-viejo">S/ ' + Number(vj).toFixed(2) + '</span>' : '';

    return '<div class="det-tmb-card" onclick="abrirDetalle(' + p.id + ')">' +
      '<div class="det-tmb-thumb" style="background:' + bk + '">' + th + '</div>' +
      '<div class="det-tmb-body">' +
        '<div class="det-tmb-nombre">' + n + '</div>' +
        '<div><span class="det-tmb-precio">S/ ' + pr.toFixed(2) + '</span>' + vH + '</div>' +
      '</div>' +
    '</div>';
  }).join('');

  wrap.style.display = 'block';
  wrap.innerHTML =
    '<div class="det-tmb-title"><i class="fas fa-magic"></i> También te puede gustar</div>' +
    '<div class="det-tmb-grid">' + tarjetasHTML + '</div>';
}

/* ════════════════════════════════════════════════════
   CAMBIAR FOTO EN GALERÍA
   ════════════════════════════════════════════════════ */
function cambiarFotoDetalle(thumb, src) {
  var main = document.getElementById('detImgMain');
  if (main) {
    main.classList.add('changing');
    setTimeout(function() { main.src = src; main.classList.remove('changing'); }, 180);
  }
  document.querySelectorAll('.det-thumb').forEach(function(t) { t.classList.remove('active'); });
  thumb.classList.add('active');
}

/* ════════════════════════════════════════════════════
   INTERACCIONES — TALLAS / COLORES / CANTIDAD
   ════════════════════════════════════════════════════ */
function detalleToggleTalla(el, talla) {
  detalleTallasSet.has(talla) ? detalleTallasSet.delete(talla) : detalleTallasSet.add(talla);
  el.classList.toggle('on', detalleTallasSet.has(talla));
  actualizarDetalleResumen();
}

function detalleToggleColor(el, color) {
  detalleColoresSet.has(color) ? detalleColoresSet.delete(color) : detalleColoresSet.add(color);
  el.classList.toggle('on', detalleColoresSet.has(color));
  actualizarDetalleResumen();
}

function detalleQtyChange(delta) {
  detalleQty = Math.max(1, detalleQty + delta);
  var el = document.getElementById('det-qty-val');
  if (el) el.textContent = detalleQty;
  actualizarDetalleResumen();
}

function actualizarDetalleResumen() {
  if (!detalleProd) return;
  var precio    = Number(detalleProd.precio || detalleProd.price || 0);
  var mayor     = detalleProd.precioMayor   ? Number(detalleProd.precioMayor)   : null;
  var cantMayor = detalleProd.cantidadMayor ? Number(detalleProd.cantidadMayor) : null;
  var tallas    = detalleProd.tallas  || [];
  var colores   = detalleProd.colores || [];

  var nT     = detalleTallasSet.size  || (tallas.length  === 0 ? 1 : 0);
  var nC     = detalleColoresSet.size || (colores.length === 0 ? 1 : 0);
  var combis = nT * nC;
  var totalU = combis * detalleQty;
  var precioU = (mayor && cantMayor && totalU >= cantMayor) ? mayor : precio;
  var total   = precioU * totalU;

  var elTL = document.getElementById('det-talla-lbl');
  if (elTL) elTL.textContent = detalleTallasSet.size > 0 ? [...detalleTallasSet].join(', ') : '';
  var elCL = document.getElementById('det-color-lbl');
  if (elCL) elCL.textContent = detalleColoresSet.size > 0 ? [...detalleColoresSet].join(', ') : '';

  var elQL = document.getElementById('det-qty-label');
  if (elQL) elQL.textContent = combis > 1
    ? combis + ' combinaciones × ' + detalleQty + ' = ' + totalU + ' unidades'
    : totalU + ' unidad' + (totalU !== 1 ? 'es' : '');

  var elTP = document.getElementById('det-total-preview');
  if (elTP) {
    var mayorOK = mayor && cantMayor && totalU >= cantMayor;
    elTP.innerHTML = mayorOK
      ? 'Total: <strong>S/ ' + total.toFixed(2) + '</strong> <span style="font-size:.72rem;background:rgba(6,214,160,.15);color:#039d76;padding:2px 8px;border-radius:20px;font-weight:700">Precio mayor aplicado</span>'
      : 'Total: <strong>S/ ' + total.toFixed(2) + '</strong>';
  }
}

/* ════════════════════════════════════════════════════
   AGREGAR AL CARRITO DESDE EL DETALLE
   ════════════════════════════════════════════════════ */
function detalleAgregarAlCarrito() {
  if (!detalleProd) return;
  var tallas  = detalleProd.tallas  || [];
  var colores = detalleProd.colores || [];

  if (tallas.length > 0 && detalleTallasSet.size === 0) {
    detalleShake('det-tallas-wrap');
    if (typeof mostrarToastCarrito === 'function') mostrarToastCarrito('Elige al menos una talla ⚠️', false);
    return;
  }
  if (colores.length > 0 && detalleColoresSet.size === 0) {
    detalleShake('det-colores-wrap');
    if (typeof mostrarToastCarrito === 'function') mostrarToastCarrito('Elige al menos un color ⚠️', false);
    return;
  }

  var tallasEf  = detalleTallasSet.size  > 0 ? [...detalleTallasSet]  : [null];
  var coloresEf = detalleColoresSet.size > 0 ? [...detalleColoresSet] : [null];

  var nombre    = detalleProd.nombre || detalleProd.name || '';
  var precio    = Number(detalleProd.precio || detalleProd.price || 0);
  var mayor     = detalleProd.precioMayor   ? Number(detalleProd.precioMayor)   : null;
  var cantMayor = detalleProd.cantidadMayor ? Number(detalleProd.cantidadMayor) : null;
  var imagen    = detalleProd.imagen || '';
  var emoji     = detalleProd.emoji  || '👕';
  var bg        = detalleProd.bg     || '#dbeafe';
  var totalU    = tallasEf.length * coloresEf.length * detalleQty;
  var precioU   = (mayor && cantMayor && totalU >= cantMayor) ? mayor : precio;
  var prodId    = detalleProd.id;

  for (var i = 0; i < tallasEf.length; i++) {
    for (var j = 0; j < coloresEf.length; j++) {
      var talla    = tallasEf[i];
      var color    = coloresEf[j];
      var colorHex = color && typeof hexDeColor === 'function' ? hexDeColor(color) : null;
      var arr      = window.carrito;
      if (!arr) return;
      var existente = arr.find(function(it) { return it.prodId === prodId && it.talla === talla && it.color === color; });
      if (existente) {
        existente.qty   += detalleQty;
        existente.precio = precioU;
      } else {
        arr.push({ prodId: prodId, nombre: nombre, emoji: emoji, bg: bg, imagen: imagen,
          talla: talla, color: color, colorHex: colorHex,
          precio: precioU, precioBase: precio, precioMayor: mayor, cantMayor: cantMayor, qty: detalleQty });
      }
    }
  }

  cerrarDetalle();
  setTimeout(function() {
    if (typeof recalcularPreciosMayor === 'function') recalcularPreciosMayor();
    if (typeof abrirCarrito    === 'function') abrirCarrito();
    if (typeof actualizarBadge === 'function') actualizarBadge();
    if (typeof mostrarToastCarrito === 'function') mostrarToastCarrito('✅ ' + nombre + ' agregado al carrito', true);
  }, 80);
}

/* ── Consultar por WhatsApp ── */
function detalleConsultarWA() {
  if (!detalleProd) return;
  var nombre = detalleProd.nombre || detalleProd.name || '';
  var precio = Number(detalleProd.precio || detalleProd.price || 0);
  var tallas = [...detalleTallasSet].join(', ') || 'sin especificar';
  var color  = [...detalleColoresSet].join(', ') || 'sin especificar';
  var msg = 'Hola MAGAMA 👋\n\nMe interesa este producto:\n\n*' + nombre + '*\n💰 Precio: S/ ' + precio.toFixed(2) + '\n📐 Talla: ' + tallas + '\n🎨 Color: ' + color + '\n\n¿Está disponible?';
  window.open('https://wa.me/51925995264?text=' + encodeURIComponent(msg), '_blank');
}

/* ── Compartir por WhatsApp ── */
function compartirProducto() {
  if (!detalleProd) return;
  var nombre = detalleProd.nombre || detalleProd.name || '';
  var precio = Number(detalleProd.precio || detalleProd.price || 0);
  var url    = window.location.href;
  var msg    = '👗 *' + nombre + '*\n💰 Precio: S/ ' + precio.toFixed(2) + '\n\n🛍️ Míralo aquí: ' + url + '\n\n¡Encuéntralo en MAGAMA Moda & Estilo!';
  window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank');
}

/* ── Shake de validación ── */
function detalleShake(id) {
  var el = document.getElementById(id);
  if (!el) return;
  el.style.animation = 'none';
  el.offsetHeight;
  el.style.animation = 'shake .4s ease';
}

/* ── Cerrar con Escape ── */
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && document.getElementById('detalleOverlay').classList.contains('open')) {
    cerrarDetalle();
  }
});

/* ── Botón atrás del navegador ── */
window.addEventListener('popstate', function() {
  if (!window.location.hash.startsWith('#producto-')) {
    var overlay = document.getElementById('detalleOverlay');
    if (overlay && overlay.classList.contains('open')) {
      document.getElementById('detalleOverlay').classList.remove('open');
      document.body.style.overflow = '';
      detalleProd = null;
      document.title = 'MAGAMA | Moda & Estilo';
    }
  }
});

/* ── Abrir producto desde URL hash al cargar ── */
(function leerHashInicial() {
  function intentarAbrir() {
    var hash = window.location.hash;
    if (!hash.startsWith('#producto-')) return;
    var match = hash.match(/^#producto-(\d+)/);
    if (!match) return;
    var prodId = Number(match[1]);
    var todos = typeof obtenerProductosActuales === 'function'
      ? obtenerProductosActuales()
      : (typeof products !== 'undefined' ? products : []);
    if (!todos.length) { setTimeout(intentarAbrir, 200); return; }
    var p = todos.find(function(x) { return x.id == prodId; });
    if (p) abrirDetalle(prodId);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { setTimeout(intentarAbrir, 300); });
  } else {
    setTimeout(intentarAbrir, 300);
  }
})();