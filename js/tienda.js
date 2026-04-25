/* ============================================================
   MAGAMA — tienda.js
   Funciones de la tienda: render, filtros, buscador, carrito
   Compatible con carrito.js (nuevo sistema profesional)
   ============================================================ */

/* ── Labels de categorías y subcategorías ── */
const CAT_LBL = {
  mujer:   'Mujer',
  hombre:  'Hombre',
  ninos:   'Niños',
  ofertas: 'Ofertas',
};

const SUBCAT_LBL = {
  'polo-bodi':       'Polo Bodi',
  'polo-oversize':   'Polo Oversize',
  'polo-top':        'Top',
  'pantalon-overol': 'Overol',
  'pantalon-varios': 'Pantalón',
  'chompa':          'Chompa',
  'enterizo':        'Enterizo',
  'vestido':         'Vestido',
  'polo-h':          'Polo',
  'casaca':          'Casaca',
  'pantalon-h':      'Pantalón',
  'camisa-h':        'Camisa',
  'polo-n':          'Polo',
  'pantalon-n':      'Pantalón',
  'camisa-n':        'Camisa',
};

/* ============================================================
   RENDER DE PRODUCTOS
   ============================================================ */
function renderProds(lista) {
  const grilla = document.getElementById('prodGrid');
  if (!grilla) return;

  if (!lista || !lista.length) {
    grilla.innerHTML = `
      <p style="text-align:center;color:var(--gray-300);
                grid-column:1/-1;padding:60px 0;font-size:.95rem">
        No se encontraron productos.
      </p>`;
    return;
  }

  grilla.innerHTML = lista.map(p => {
    /* Soporte para ambos formatos: products[] y MAGAMA_DB.productos[] */
    const nombre  = p.nombre  || p.name  || '';
    const cat     = p.categoria || p.cat || '';
    const subcat  = p.subcategoria || p.subcat || '';
    const precio  = p.precio  || p.price || 0;
    const precioViejo = p.precioAntes || p.old || null;
    const badge   = p.badge   || p.tag  || null;
    const imagen  = p.imagen  || p.img  || '';
    const tallas  = p.tallas  || [];
    const precioMayor    = p.precioMayor    || null;
    const cantidadMayor  = p.cantidadMayor  || 6;

    /* Tag / Badge */
    const badgeMap = {
      new:  { txt: 'Nuevo',     cls: 'ptag-new'  },
      hot:  { txt: 'Popular',   cls: 'ptag-hot'  },
      sale: { txt: 'Oferta',    cls: 'ptag-sale' },
      dest: { txt: 'Destacado', cls: 'ptag-hot'  },
    };
    const badgeHtml = badge && badgeMap[badge]
      ? `<span class="ptag ${badgeMap[badge].cls}">${badgeMap[badge].txt}</span>`
      : '';

    /* Imagen o emoji */
    const thumbHtml = imagen
      ? `<img src="${imagen}" alt="${nombre}"
              style="width:100%;height:100%;object-fit:cover;position:absolute;inset:0"
              onerror="this.style.display='none'">`
      : `<span class="pemoji">${p.emoji || '👕'}</span>`;

    /* Tallas */
    const tallasHtml = tallas.length
      ? `<div style="display:flex;gap:4px;flex-wrap:wrap;padding:4px 16px 8px">
           ${tallas.slice(0,5).map(t =>
             `<span style="font-size:.6rem;padding:2px 7px;border-radius:4px;
                           background:#EFF3FA;color:#334166;font-weight:600">${t}</span>`
           ).join('')}
           ${tallas.length > 5 ? `<span style="font-size:.6rem;color:#6B7FA3">+${tallas.length-5}</span>` : ''}
         </div>`
      : '';

    /* Precio por mayor */
    const mayorHtml = precioMayor
      ? `<div style="font-size:.7rem;color:#06D6A0;font-weight:700;
                     padding:0 16px 8px;display:flex;align-items:center;gap:4px">
           <i class="fas fa-boxes" style="font-size:.65rem"></i>
           Mayor x${cantidadMayor}+: S/ ${precioMayor.toFixed(2)}
         </div>`
      : '';

    return `
      <div class="prod-card" data-cat="${cat}" data-subcat="${subcat}">
        <div class="prod-thumb" style="background:${p.bg || '#dbeafe'};position:relative">
          ${thumbHtml}
          ${badgeHtml}
          <button class="pwish" onclick="toggleWishlist(this)" title="Favorito">
            <i class="far fa-heart"></i>
          </button>
        </div>
        <div class="prod-body">
          <div class="prod-cat">${CAT_LBL[cat] || cat}</div>
          <div class="prod-name">${nombre}</div>
          <div class="prod-sub">${SUBCAT_LBL[subcat] || subcat}</div>
        </div>
        ${tallasHtml}
        ${mayorHtml}
        <div class="prod-foot">
          <div>
            <span class="prod-price">S/ ${Number(precio).toFixed(2)}</span>
            ${precioViejo
              ? `<span class="prod-old">S/ ${Number(precioViejo).toFixed(2)}</span>`
              : ''}
          </div>
          <button class="add-btn"
                  onclick="agregarAlCarrito(${p.id})"
                  title="Agregar al carrito">
            <i class="fas fa-plus"></i>
          </button>
        </div>
      </div>`;
  }).join('');
}

/* ============================================================
   FILTROS
   ============================================================ */
function filterProds(btn, cat) {
  document.querySelectorAll('.fb').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const lista = cat === 'all'
    ? obtenerProductos()
    : obtenerProductos().filter(p => (p.categoria || p.cat) === cat);
  renderProds(lista);
  document.getElementById('productos')?.scrollIntoView({ behavior: 'smooth' });
}

function catFilter(cat) {
  document.querySelectorAll('.fb').forEach(b => b.classList.remove('active'));
  renderProds(obtenerProductos().filter(p => (p.categoria || p.cat) === cat));
  document.getElementById('productos')?.scrollIntoView({ behavior: 'smooth' });
}

function subFilter(sub) {
  document.querySelectorAll('.fb').forEach(b => b.classList.remove('active'));
  renderProds(obtenerProductos().filter(p => (p.subcategoria || p.subcat) === sub));
  document.getElementById('productos')?.scrollIntoView({ behavior: 'smooth' });
}

/* Obtiene productos desde DB (database.js) o desde el array products[] */
function obtenerProductos(filtros) {
  /* Si existe database.js → usa MAGAMA_DB */
  if (typeof MAGAMA_DB !== 'undefined') {
    let lista = MAGAMA_DB.productos || [];
    if (filtros) {
      if (filtros.categoria)    lista = lista.filter(p => p.categoria    === filtros.categoria);
      if (filtros.subcategoria) lista = lista.filter(p => p.subcategoria === filtros.subcategoria);
      if (filtros.busqueda)     lista = lista.filter(p =>
        (p.nombre||'').toLowerCase().includes(filtros.busqueda.toLowerCase()));
    }
    return lista;
  }
  /* Si no → usa el array products[] del index.html */
  if (typeof products !== 'undefined') {
    let lista = products;
    if (filtros) {
      if (filtros.categoria)    lista = lista.filter(p => p.cat    === filtros.categoria);
      if (filtros.subcategoria) lista = lista.filter(p => p.subcat === filtros.subcategoria);
      if (filtros.busqueda)     lista = lista.filter(p =>
        (p.name||'').toLowerCase().includes(filtros.busqueda.toLowerCase()));
    }
    return lista;
  }
  return [];
}

/* Puente: carrito.js llama DB_getProductos() */
function DB_getProductos(filtros) {
  return obtenerProductos(filtros);
}

/* ============================================================
   BUSCADOR
   ============================================================ */
function doSearch(q) {
  const drop = document.getElementById('srchDrop');
  if (!drop) return;
  if (!q.trim()) { drop.classList.remove('open'); return; }

  const todos = obtenerProductos();
  const res = todos.filter(p => {
    const nombre = (p.nombre || p.name || '').toLowerCase();
    const cat    = (CAT_LBL[p.categoria || p.cat] || '').toLowerCase();
    const desc   = (p.descripcion || '').toLowerCase();
    return nombre.includes(q.toLowerCase())
        || cat.includes(q.toLowerCase())
        || desc.includes(q.toLowerCase());
  }).slice(0, 8);

  if (!res.length) { drop.classList.remove('open'); return; }

  drop.innerHTML = res.map(p => {
    const nombre = p.nombre || p.name || '';
    const cat    = p.categoria || p.cat || '';
    return `
      <div class="sri" onclick="srchClick(${p.id})">
        <div>
          <div class="sri-cat">${CAT_LBL[cat] || cat}</div>
          <div class="sri-name">${nombre}</div>
        </div>
      </div>`;
  }).join('');

  drop.classList.add('open');
}

function srchClick(id) {
  document.getElementById('srchDrop')?.classList.remove('open');
  const inp = document.getElementById('srchIn');
  if (inp) inp.value = '';
  const p = obtenerProductos().find(x => x.id == id);
  if (p) {
    renderProds([p]);
    document.getElementById('productos')?.scrollIntoView({ behavior: 'smooth' });
  }
}

document.addEventListener('click', e => {
  if (!e.target.closest('.srch-wrap')) {
    document.getElementById('srchDrop')?.classList.remove('open');
  }
});

/* ============================================================
   WISHLIST
   ============================================================ */
function toggleWishlist(btn) {
  btn.classList.toggle('active');
  btn.querySelector('i').className = btn.classList.contains('active')
    ? 'fas fa-heart'
    : 'far fa-heart';
}

/* ============================================================
   NAV MOBILE
   ============================================================ */
function toggleMob() {
  document.getElementById('mobNav')?.classList.toggle('open');
}

/* ============================================================
   SCROLL HEADER
   ============================================================ */
window.addEventListener('scroll', () => {
  document.getElementById('main-hdr')
    ?.classList.toggle('scrolled', window.scrollY > 40);
});

/* ============================================================
   INIT — Se ejecuta cuando el DOM está listo
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {

  /* 1. Mostrar todos los productos */
  renderProds(obtenerProductos());

  /* 2. Aplicar configuración dinámica de database.js (si existe) */
  if (typeof MAGAMA_DB !== 'undefined') {
    const cfg = MAGAMA_DB.config || {};

    /* Barra de anuncios dinámica */
    if (cfg.anuncio) {
      const track = document.querySelector('.ann-track');
      if (track) {
        const partes = cfg.anuncio.split('|').map(s => s.trim());
        const contenido = partes
          .map(p => `<span>${p}</span>`)
          .join('<span class="dot">◆</span>');
        /* Duplicar para el loop continuo del marquee */
        track.innerHTML = contenido
          + '<span class="dot">◆</span>'
          + contenido
          + '<span class="dot">◆</span>';
      }
    }

    /* Links de WhatsApp dinámicos */
    const wa = cfg.whatsapp || '51925995264';
    document.querySelectorAll('[data-wa]').forEach(el => {
      const msg = el.dataset.wa || '';
      el.href = `https://wa.me/${wa}?text=${encodeURIComponent(msg)}`;
    });

    /* Links de Google Maps dinámicos */
    if (cfg.maps) {
      document.querySelectorAll('[data-maps]').forEach(el => {
        el.href = cfg.maps;
      });
    }
  }

});
