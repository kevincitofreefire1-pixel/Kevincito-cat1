/* ============================================================
   MAGAMA — favoritos.js
   Sistema de favoritos con persistencia en localStorage.
   - Toggle corazón en tarjetas de producto
   - Filtro "Favoritos" en la sección de productos
   - Badge con cantidad de favoritos
   - Persiste al recargar la página
   ============================================================ */

'use strict';

/* ── Clave de localStorage ── */
const FAV_KEY = 'magama_favoritos';

/* ── Cargar favoritos guardados ── */
function favCargar() {
  try {
    const raw = localStorage.getItem(FAV_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) return parsed;
    }
  } catch(e) { /* silent */ }
  return [];
}

/* ── Guardar favoritos ── */
function favGuardar(ids) {
  try {
    localStorage.setItem(FAV_KEY, JSON.stringify(ids));
  } catch(e) { /* silent */ }
}

/* ── Estado global de favoritos (array de prodId) ── */
var favoritos = favCargar();

/* ════════════════════════════════════════════════════════════
   TOGGLE FAVORITO — llamado desde el botón corazón
   ════════════════════════════════════════════════════════════ */
function toggleWishlist(btn) {
  const card = btn.closest('.prod-card');
  if (!card) return;

  /* Obtener prodId del botón del carrito dentro de la tarjeta */
  const addBtn = card.querySelector('.add-btn');
  if (!addBtn) return;

  /* Extraer el id del onclick="agregarAlCarrito(123)" */
  const match = (addBtn.getAttribute('onclick') || '').match(/\d+/);
  if (!match) return;
  const prodId = Number(match[0]);

  const esFav = favoritos.includes(prodId);

  if (esFav) {
    /* Quitar de favoritos */
    favoritos = favoritos.filter(function(id) { return id !== prodId; });
    btn.classList.remove('active');
    btn.querySelector('i').className = 'far fa-heart';
    favMostrarToast('Eliminado de favoritos', false);
  } else {
    /* Agregar a favoritos */
    favoritos.push(prodId);
    btn.classList.add('active');
    btn.querySelector('i').className = 'fas fa-heart';

    /* Animación del corazón */
    btn.style.transform = 'scale(1.35)';
    setTimeout(function() { btn.style.transform = ''; }, 250);

    favMostrarToast('¡Agregado a favoritos! ❤️', true);
  }

  favGuardar(favoritos);
  favActualizarBadge();

  /* Si estamos viendo el filtro favoritos, re-renderizar */
  if (favFiltroActivo()) {
    const btnFav = document.getElementById('btn-filtro-favoritos');
    if (btnFav) filterProds(btnFav, 'favoritos');
  }
}

/* ── Verificar si el filtro de favoritos está activo ── */
function favFiltroActivo() {
  const btn = document.getElementById('btn-filtro-favoritos');
  return btn && btn.classList.contains('active');
}

/* ════════════════════════════════════════════════════════════
   RESTAURAR CORAZONES al renderizar tarjetas
   Se llama después de renderProds()
   ════════════════════════════════════════════════════════════ */
function favRestaurarCorazones() {
  const grid = document.getElementById('prodGrid');
  if (!grid) return;

  grid.querySelectorAll('.prod-card').forEach(function(card) {
    const addBtn = card.querySelector('.add-btn');
    if (!addBtn) return;
    const match = (addBtn.getAttribute('onclick') || '').match(/\d+/);
    if (!match) return;
    const prodId = Number(match[0]);
    const btn = card.querySelector('.pwish');
    if (!btn) return;

    if (favoritos.includes(prodId)) {
      btn.classList.add('active');
      btn.querySelector('i').className = 'fas fa-heart';
    } else {
      btn.classList.remove('active');
      btn.querySelector('i').className = 'far fa-heart';
    }
  });
}

/* ════════════════════════════════════════════════════════════
   FILTRO DE FAVORITOS
   ════════════════════════════════════════════════════════════ */
function favMostrarProductos() {
  const todos = typeof obtenerProductosActuales === 'function'
    ? obtenerProductosActuales()
    : (typeof products !== 'undefined' ? products : []);

  const lista = todos.filter(function(p) {
    return favoritos.includes(p.id);
  });

  if (typeof renderProds === 'function') {
    renderProds(lista);
    /* Marcar corazones después de renderizar */
    setTimeout(favRestaurarCorazones, 50);
  }

  /* Scroll a productos */
  const sec = document.getElementById('productos');
  if (sec) sec.scrollIntoView({ behavior: 'smooth' });
}

/* ════════════════════════════════════════════════════════════
   BADGE de cantidad en el botón de favoritos
   ════════════════════════════════════════════════════════════ */
function favActualizarBadge() {
  const badge = document.getElementById('fav-badge');
  if (!badge) return;
  const total = favoritos.length;
  badge.textContent = total;
  badge.style.display = total > 0 ? 'flex' : 'none';
}

/* ════════════════════════════════════════════════════════════
   TOAST de favoritos
   ════════════════════════════════════════════════════════════ */
function favMostrarToast(msg, esAgregar) {
  /* Reutilizar toast del carrito si existe */
  if (typeof mostrarToastCarrito === 'function') {
    mostrarToastCarrito(msg, esAgregar);
    return;
  }
  /* Toast propio si no hay carrito */
  var t = document.getElementById('favToast');
  if (!t) return;
  t.querySelector('span').textContent = msg;
  t.querySelector('i').className = esAgregar ? 'fas fa-heart' : 'far fa-heart';
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(function() { t.classList.remove('show'); }, 2500);
}

/* ════════════════════════════════════════════════════════════
   INYECTAR botón FAVORITOS en la fila de filtros
   y en la tarjeta de categorías
   ════════════════════════════════════════════════════════════ */
(function inyectarFavoritos() {

  /* ── 1. Agregar botón en la fila de filtros de productos ── */
  function agregarBotonFiltro() {
    const filterRow = document.getElementById('filterRow');
    if (!filterRow || document.getElementById('btn-filtro-favoritos')) return;

    const btn = document.createElement('button');
    btn.className = 'fb';
    btn.id = 'btn-filtro-favoritos';
    btn.style.cssText = 'position:relative;display:inline-flex;align-items:center;gap:6px;';
    btn.innerHTML = `
      <i class="fas fa-heart" style="color:#FF6B6B;font-size:.85rem"></i>
      Favoritos
      <span id="fav-badge" style="
        position:absolute;top:-6px;right:-6px;
        background:#FF6B6B;color:#fff;
        border-radius:50%;width:18px;height:18px;
        font-size:.6rem;font-weight:700;
        display:none;align-items:center;justify-content:center;
        border:2px solid #fff;
      ">0</span>`;

    btn.onclick = function() {
      if (btn.classList.contains('active')) {
        /* Si ya está activo, volver a "Todos" */
        const btnTodos = filterRow.querySelector('.fb');
        if (btnTodos) filterProds(btnTodos, 'all');
      } else {
        document.querySelectorAll('.fb').forEach(function(b) {
          b.classList.remove('active');
        });
        btn.classList.add('active');
        favMostrarProductos();
      }
    };

    filterRow.appendChild(btn);
    favActualizarBadge();
  }

  /* ── 2. Agregar tarjeta FAVORITOS en la sección de categorías ── */
  function agregarTarjetaCategoria() {
    const catGrid = document.querySelector('.cat-grid');
    if (!catGrid || document.getElementById('cat-card-favoritos')) return;

    const card = document.createElement('div');
    card.className = 'cat-card';
    card.id = 'cat-card-favoritos';
    card.style.cssText = 'cursor:pointer;border:1.5px solid rgba(255,107,107,.2);';
    card.innerHTML = `
      <div class="cat-img" style="background:linear-gradient(145deg,#fff0f0,#ffd6d6)">
        <span style="font-size:5.5rem;transition:transform .3s">❤️</span>
      </div>
      <div class="cat-body">
        <div class="cat-name" style="color:#c04040">Favoritos</div>
        <div class="cat-desc">Tus prendas guardadas. Accede rápidamente a los productos que te gustaron.</div>
      </div>
      <div class="cat-foot">
        <span class="cat-lnk" style="color:#c04040">
          Ver favoritos <i class="fas fa-arrow-right"></i>
        </span>
        <span id="fav-cat-badge" style="
          background:#FF6B6B;color:#fff;
          font-size:.67rem;font-weight:700;
          padding:3px 9px;border-radius:20px;
          display:none;
        ">0 guardados</span>
      </div>`;

    card.onclick = function() {
      const btnFav = document.getElementById('btn-filtro-favoritos');
      if (btnFav) {
        document.querySelectorAll('.fb').forEach(function(b) {
          b.classList.remove('active');
        });
        btnFav.classList.add('active');
        favMostrarProductos();
        const sec = document.getElementById('productos');
        if (sec) sec.scrollIntoView({ behavior: 'smooth' });
      }
    };

    catGrid.appendChild(card);
    favActualizarBadgeCat();
  }

  /* ── Actualizar badge de la tarjeta categoría ── */
  window.favActualizarBadgeCat = function() {
    const badge = document.getElementById('fav-cat-badge');
    if (!badge) return;
    const total = favoritos.length;
    badge.textContent = total + (total === 1 ? ' guardado' : ' guardados');
    badge.style.display = total > 0 ? 'inline-block' : 'none';
  };

  /* ── Esperar a que el DOM esté listo ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      agregarBotonFiltro();
      agregarTarjetaCategoria();
    });
  } else {
    /* DOM ya listo */
    agregarBotonFiltro();
    agregarTarjetaCategoria();
  }

})();

/* ════════════════════════════════════════════════════════════
   HOOK: restaurar corazones después de cada renderProds
   Envuelve la función original para agregar el restore automático
   ════════════════════════════════════════════════════════════ */
(function hookRenderProds() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', _hookRenderProds);
  } else {
    setTimeout(_hookRenderProds, 100);
  }

  function _hookRenderProds() {
    if (typeof renderProds !== 'function') {
      setTimeout(_hookRenderProds, 150);
      return;
    }
    const _original = renderProds;
    window.renderProds = function(list) {
      _original(list);
      setTimeout(function() {
        favRestaurarCorazones();
        favActualizarBadge();
        if (typeof favActualizarBadgeCat === 'function') favActualizarBadgeCat();
      }, 60);
    };
  }
})();
