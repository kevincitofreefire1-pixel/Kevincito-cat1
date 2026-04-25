/* ============================================================
   MAGAMA — carrito.js
   Carrito completo con selección MÚLTIPLE de tallas y colores.
   Cada combinación talla+color se agrega como ítem independiente.
   ============================================================ */

'use strict';

/* ── Estado global ── */
var carrito   = [];          // [{prodId, nombre, emoji, bg, imagen, talla, color, colorHex, precio, precioMayor, cantMayor, qty}]
let cuponActivo = null;      // {codigo, tipo:'%'|'S/', valor}

const CUPONES = {
  'MAGAMA10': { tipo:'%',   valor:10 },
  'MAGAMA20': { tipo:'%',   valor:20 },
  'DESCUENTO': { tipo:'S/', valor:15 },
};

const WA_NUMBER = '51925995264';
const META_ENVIO = 100;   // monto para envío gratis (barra de progreso)

/* ── Mapa de colores nombre→hex para mostrar el punto de color ── */
const COLOR_HEX = {
  'Blanco':'#ffffff','Negro':'#1a1a1a','Gris':'#6b7280','Azul':'#3b82f6',
  'Rojo':'#ef4444','Naranja':'#f97316','Amarillo':'#eab308','Verde':'#22c55e',
  'Rosado':'#ec4899','Morado':'#a855f7','Marrón':'#92400e','Celeste':'#0891b2',
  'Coral':'#f43f5e','Turquesa':'#14b8a6','Lima':'#84cc16','Dorado':'#f59e0b',
  'Lila':'#c084fc','Crema':'#fef3c7','Beige':'#d6b89a','Marino':'#1e3a5f',
  'Café':'#6d4c41','Plateado':'#b0bec5','Champagne':'#d4af37',
};

function hexDeColor(nombre) {
  if (!nombre) return '#888';
  if (nombre.startsWith('#')) return nombre;
  return COLOR_HEX[nombre] || '#888';
}

/* ════════════════════════════════════════════════════════════
   MODAL SELECTOR — tallas y colores MÚLTIPLES
   ════════════════════════════════════════════════════════════ */

/* Estado del selector actual */
let selectorProd    = null;
let tallasSeleccionadas  = new Set();
let coloresSeleccionados = new Set();
let selectorQty     = 1;

function agregarAlCarrito(prodId) {
  const todos = typeof obtenerProductosActuales === 'function'
    ? obtenerProductosActuales()
    : (typeof products !== 'undefined' ? products : []);
  const p = todos.find(x => x.id == prodId);
  if (!p) return;
  abrirSelector(p);
}

function abrirSelector(p) {
  selectorProd = p;
  tallasSeleccionadas  = new Set();
  coloresSeleccionados = new Set();
  selectorQty = 1;

  const nombre   = p.nombre   || p.name  || '';
  const precio   = Number(p.precio || p.price || 0);
  const viejo    = p.precioAntes || p.old || null;
  const mayor    = p.precioMayor   ? Number(p.precioMayor)   : null;
  const cantMayor= p.cantidadMayor ? Number(p.cantidadMayor) : null;
  const tallas   = p.tallas  || [];
  const colores  = p.colores || [];
  const imagen   = p.imagen  || '';
  const emoji    = p.emoji   || '👕';
  const bg       = p.bg      || '#dbeafe';

  /* Thumb: imagen real o emoji */
  const thumbHTML = imagen
    ? `<img src="${imagen}" style="width:56px;height:64px;object-fit:cover;border-radius:10px;" onerror="this.outerHTML='<span style=font-size:1.8rem>${emoji}</span>'">`
    : `<span style="font-size:1.8rem">${emoji}</span>`;

  /* Precio mayor */
  const mayorHTML = mayor && cantMayor
    ? `<div class="sel-mayor">Mayor x${cantMayor}+: S/ ${mayor.toFixed(2)}</div>` : '';

  /* Chips de tallas */
  const tallasHTML = tallas.length
    ? tallas.map(t => `
        <div class="sel-chip" data-talla="${t}" onclick="toggleTalla(this,'${t}')">
          ${t}
        </div>`).join('')
    : `<p style="font-size:.8rem;color:#6B7FA3;margin:4px 0">Este producto no tiene tallas específicas.</p>`;

  /* Chips de colores */
  const coloresHTML = colores.length
    ? colores.map(c => {
        const hex = hexDeColor(c);
        return `
        <div class="sel-chip" data-color="${c}" onclick="toggleColor(this,'${c}')">
          <span class="sel-color-dot" style="background:${hex};border:1px solid rgba(0,0,0,.15)"></span>
          ${c}
        </div>`;
      }).join('')
    : `<p style="font-size:.8rem;color:#6B7FA3;margin:4px 0">Este producto no tiene colores específicos.</p>`;

  /* Aviso multi-selección */
  const avisoHTML = (tallas.length || colores.length)
    ? `<div style="background:#EEF5FF;border-left:3px solid #00B4D8;border-radius:6px;padding:8px 12px;margin-bottom:14px;font-size:.76rem;color:#334166;">
        <i class="fas fa-info-circle" style="color:#00B4D8;margin-right:5px"></i>
        Puedes seleccionar <strong>varias tallas y varios colores</strong>. Se agregará una combinación por cada par talla×color.
      </div>` : '';

  document.getElementById('selectorModal').innerHTML = `
    <div class="sel-overlay" onclick="cerrarSelector()"></div>
    <div class="sel-card">
      <div class="sel-hdr">
        <div class="sel-prod-info">
          <div class="sel-thumb" style="background:${bg}">${thumbHTML}</div>
          <div>
            <div class="sel-name">${nombre}</div>
            <div class="sel-price">S/ ${precio.toFixed(2)}
              ${viejo ? `<span style="font-size:.8rem;color:#B0BEDB;text-decoration:line-through;margin-left:6px">S/ ${Number(viejo).toFixed(2)}</span>` : ''}
            </div>
            ${mayorHTML}
          </div>
        </div>
        <button class="sel-cls" onclick="cerrarSelector()"><i class="fas fa-times"></i></button>
      </div>
      <div class="sel-body">
        ${avisoHTML}

        ${tallas.length ? `
        <div class="sel-section">
          <div class="sel-section-title">
            TALLA <span class="sel-required">*</span>
            <span id="sel-talla-count" style="margin-left:8px;font-size:.68rem;color:#00B4D8;font-weight:700"></span>
          </div>
          <div class="sel-chips">${tallasHTML}</div>
        </div>` : ''}

        ${colores.length ? `
        <div class="sel-section">
          <div class="sel-section-title">
            COLOR <span class="sel-required">*</span>
            <span id="sel-color-count" style="margin-left:8px;font-size:.68rem;color:#00B4D8;font-weight:700"></span>
          </div>
          <div class="sel-chips">${coloresHTML}</div>
        </div>` : ''}

        <div class="sel-section">
          <div class="sel-section-title">CANTIDAD <span style="font-size:.68rem;color:#6B7FA3">(por combinación)</span></div>
          <div class="sel-qty-row">
            <div class="sel-qty">
              <button class="sel-qty-btn" onclick="cambiarSelectorQty(-1)"><i class="fas fa-minus"></i></button>
              <span class="sel-qty-val" id="selQtyVal">1</span>
              <button class="sel-qty-btn" onclick="cambiarSelectorQty(1)"><i class="fas fa-plus"></i></button>
            </div>
            <div id="sel-resumen-combis" style="font-size:.76rem;color:#6B7FA3;text-align:right;max-width:200px"></div>
          </div>
        </div>

      </div>
      <div class="sel-footer">
        <div>
          <div class="sel-total" id="selTotal">S/ ${precio.toFixed(2)}</div>
          <div style="font-size:.7rem;color:#6B7FA3;margin-top:2px" id="selTotalSub">1 unidad</div>
        </div>
        <button class="sel-add-btn" onclick="confirmarAgregarAlCarrito()">
          <i class="fas fa-shopping-bag"></i> Agregar al carrito
        </button>
      </div>
    </div>`;

  document.getElementById('selectorModal').classList.add('open');
  actualizarResumenSelector();
}

function cerrarSelector() {
  document.getElementById('selectorModal').classList.remove('open');
  selectorProd = null;
}

function toggleTalla(el, talla) {
  if (tallasSeleccionadas.has(talla)) {
    tallasSeleccionadas.delete(talla);
    el.classList.remove('on');
  } else {
    tallasSeleccionadas.add(talla);
    el.classList.add('on');
  }
  actualizarResumenSelector();
}

function toggleColor(el, color) {
  if (coloresSeleccionados.has(color)) {
    coloresSeleccionados.delete(color);
    el.classList.remove('on');
  } else {
    coloresSeleccionados.add(color);
    el.classList.add('on');
  }
  actualizarResumenSelector();
}

function cambiarSelectorQty(delta) {
  selectorQty = Math.max(1, selectorQty + delta);
  const el = document.getElementById('selQtyVal');
  if (el) el.textContent = selectorQty;
  actualizarResumenSelector();
}

function actualizarResumenSelector() {
  if (!selectorProd) return;

  const precio    = Number(selectorProd.precio || selectorProd.price || 0);
  const mayor     = selectorProd.precioMayor   ? Number(selectorProd.precioMayor)   : null;
  const cantMayor = selectorProd.cantidadMayor ? Number(selectorProd.cantidadMayor) : null;
  const tallas    = selectorProd.tallas  || [];
  const colores   = selectorProd.colores || [];

  /* Contar combinaciones */
  const nTallas  = tallasSeleccionadas.size  || (tallas.length  === 0 ? 1 : 0);
  const nColores = coloresSeleccionados.size || (colores.length === 0 ? 1 : 0);
  const combis   = nTallas * nColores;
  const totalUnidades = combis * selectorQty;

  /* Precio unitario: aplicar precio mayor si corresponde */
  const precioUnit = (mayor && cantMayor && totalUnidades >= cantMayor) ? mayor : precio;
  const totalPrecio = precioUnit * totalUnidades;

  /* Actualizar contador tallas */
  const elTC = document.getElementById('sel-talla-count');
  if (elTC) elTC.textContent = tallasSeleccionadas.size > 0 ? `(${tallasSeleccionadas.size} seleccionada${tallasSeleccionadas.size>1?'s':''})` : '';

  /* Actualizar contador colores */
  const elCC = document.getElementById('sel-color-count');
  if (elCC) elCC.textContent = coloresSeleccionados.size > 0 ? `(${coloresSeleccionados.size} seleccionado${coloresSeleccionados.size>1?'s':''})` : '';

  /* Resumen de combinaciones */
  const elRes = document.getElementById('sel-resumen-combis');
  if (elRes) {
    if (combis > 1) {
      elRes.innerHTML = `<span style="color:#03045E;font-weight:700">${combis} combinaciones × ${selectorQty} = <strong>${totalUnidades} unidades</strong></span>`;
    } else {
      elRes.innerHTML = '';
    }
  }

  /* Total */
  const elTot = document.getElementById('selTotal');
  if (elTot) {
    const mayorActivo = mayor && cantMayor && totalUnidades >= cantMayor;
    elTot.innerHTML = mayorActivo
      ? `S/ ${totalPrecio.toFixed(2)} <span style="font-size:.7rem;background:rgba(6,214,160,.15);color:#039d76;padding:2px 7px;border-radius:20px;font-weight:700">Precio mayor</span>`
      : `S/ ${totalPrecio.toFixed(2)}`;
  }

  const elSub = document.getElementById('selTotalSub');
  if (elSub) {
    elSub.textContent = totalUnidades === 1
      ? '1 unidad'
      : `${totalUnidades} unidades`;
  }
}

function confirmarAgregarAlCarrito() {
  if (!selectorProd) return;

  const tallas  = selectorProd.tallas  || [];
  const colores = selectorProd.colores || [];

  /* Validar: si tiene tallas definidas, debe elegir al menos una */
  if (tallas.length > 0 && tallasSeleccionadas.size === 0) {
    shakearElemento('.sel-section-title');
    mostrarToastCarrito('Elige al menos una talla ⚠️', false);
    return;
  }
  /* Validar: si tiene colores definidos, debe elegir al menos uno */
  if (colores.length > 0 && coloresSeleccionados.size === 0) {
    mostrarToastCarrito('Elige al menos un color ⚠️', false);
    return;
  }

  /* Generar lista de tallas y colores efectivos */
  const tallasEfectivas  = tallasSeleccionadas.size  > 0 ? [...tallasSeleccionadas]  : [null];
  const coloresEfectivos = coloresSeleccionados.size > 0 ? [...coloresSeleccionados] : [null];

  const nombre    = selectorProd.nombre   || selectorProd.name  || '';
  const precio    = Number(selectorProd.precio || selectorProd.price || 0);
  const mayor     = selectorProd.precioMayor   ? Number(selectorProd.precioMayor)   : null;
  const cantMayor = selectorProd.cantidadMayor ? Number(selectorProd.cantidadMayor) : null;
  const imagen    = selectorProd.imagen  || '';
  const emoji     = selectorProd.emoji   || '👕';
  const bg        = selectorProd.bg      || '#dbeafe';

  /* Calcular total de unidades para precio mayor */
  const totalUnidades = tallasEfectivas.length * coloresEfectivos.length * selectorQty;
  const precioUnit = (mayor && cantMayor && totalUnidades >= cantMayor) ? mayor : precio;

  let itemsAgregados = 0;

  /* Agregar una entrada por cada combinación talla×color */
  for (const talla of tallasEfectivas) {
    for (const color of coloresEfectivos) {
      const hex = color ? hexDeColor(color) : null;

      /* Buscar ítem existente idéntico */
      const existente = carrito.find(i =>
        i.prodId === selectorProd.id &&
        i.talla  === talla  &&
        i.color  === color
      );

      if (existente) {
        existente.qty += selectorQty;
        existente.precio = precioUnit; /* actualizar precio mayor si aplica */
      } else {
        carrito.push({
          prodId:     selectorProd.id,
          nombre,
          emoji,
          bg,
          imagen,
          talla,
          color,
          colorHex:   hex,
          precio:     precioUnit,
          precioBase: precio,        /* precio normal guardado para recalcular */
          precioMayor: mayor,
          cantMayor,
          qty:        selectorQty,
        });
      }
      itemsAgregados++;
    }
  }

  recalcularPreciosMayor();
  cerrarSelector();
  abrirCarrito();
  actualizarBadge();

  const msg = itemsAgregados === 1
    ? `✅ ${nombre} agregado`
    : `✅ ${itemsAgregados} combinaciones de ${nombre} agregadas`;
  mostrarToastCarrito(msg, true);
}

/* ════════════════════════════════════════════════════════════
   CARRITO SIDEBAR
   ════════════════════════════════════════════════════════════ */

function abrirCarrito() {
  document.getElementById('cartOverlay').classList.add('open');
  document.getElementById('cartSidebar').classList.add('open');
  requestAnimationFrame(function() { renderCarrito(); });
}

function cerrarCarrito() {
  document.getElementById('cartOverlay').classList.remove('open');
  document.getElementById('cartSidebar').classList.remove('open');
}

function renderCarrito() {
  const wrap  = document.getElementById('cartItemsWrap');
  const empty = document.getElementById('cartEmptyState');
  const footer= document.getElementById('cartFooter');
  const res   = document.getElementById('cart-resumen');
  const fAct  = document.getElementById('cartFooterActions');
  const floatBtn = document.getElementById('cartFloatBtn');

  if (!wrap) return;

  if (carrito.length === 0) {
    empty.style.display = 'flex';
    wrap.innerHTML = '';
    if (footer) footer.style.display = 'none';
    if (res)    res.style.display    = 'none';
    if (fAct)   fAct.style.display   = 'none';
    if (floatBtn) floatBtn.classList.remove('has-items');
    actualizarProgreso(0);
    return;
  }

  empty.style.display = 'none';
  if (footer) footer.style.display = 'block';
  if (res)    res.style.display    = 'block';
  if (fAct)   fAct.style.display   = 'block';
  if (floatBtn) floatBtn.classList.add('has-items');

  wrap.innerHTML = carrito.map((item, idx) => {
    const thumbHTML = item.imagen
      ? `<img src="${item.imagen}" style="width:100%;height:100%;object-fit:cover;border-radius:10px;" onerror="this.outerHTML='<span style=font-size:2rem>${item.emoji}</span>'">`
      : `<span style="font-size:2rem">${item.emoji}</span>`;

    /* Tags de talla y color */
    const tallaTag  = item.talla ? `<span class="ci-tag">${item.talla}</span>` : '';
    const colorDot  = item.colorHex ? `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${item.colorHex};border:1px solid rgba(0,0,0,.1);margin-right:3px;vertical-align:middle"></span>` : '';
    const colorTag  = item.color ? `<span class="ci-tag">${colorDot}${item.color}</span>` : '';

    /* Badge precio mayor */
    const mayorActual = item.precioMayor && item.cantMayor && item.qty >= item.cantMayor;
    const mayorTag = mayorActual
      ? `<span class="ci-tag ci-mayor">🏷️ Mayor</span>` : '';

    const subtotal = item.precio * item.qty;

    return `
    <div class="cart-item" id="ci-${idx}">
      <div class="ci-thumb" style="background:${item.bg}">${thumbHTML}</div>
      <div class="ci-info">
        <div class="ci-name">${item.nombre}</div>
        <div class="ci-vars">${tallaTag}${colorTag}${mayorTag}</div>
        <div class="ci-price-row">
          <div class="ci-qty">
            <button onclick="cambiarQtyCarrito(${idx},-1)"><i class="fas fa-minus"></i></button>
            <span>${item.qty}</span>
            <button onclick="cambiarQtyCarrito(${idx},1)"><i class="fas fa-plus"></i></button>
          </div>
          <div class="ci-price">S/ ${subtotal.toFixed(2)}</div>
        </div>
      </div>
      <button class="ci-del" onclick="eliminarItemCarrito(${idx})"><i class="fas fa-trash"></i></button>
    </div>`;
  }).join('');

  renderResumen();
  actualizarProgreso(calcularSubtotal());
}

function cambiarQtyCarrito(idx, delta) {
  if (!carrito[idx]) return;
  carrito[idx].qty = Math.max(1, carrito[idx].qty + delta);
  recalcularPreciosMayor();
  renderCarrito();
  actualizarBadge();
}

/* ── Recalcula precio mayor según el TOTAL de unidades del carrito completo.
      Si la suma de TODOS los productos >= 3, se aplica precio mayor
      a cada ítem que tenga precio mayor definido. ── */
function recalcularPreciosMayor() {
  const MINIMO_MAYOR = 3; /* unidades totales del carrito para activar precio mayor */

  const todosProductos = typeof obtenerProductosActuales === 'function'
    ? obtenerProductosActuales()
    : (typeof products !== 'undefined' ? products : []);

  /* Sumar TODAS las unidades del carrito (sin importar el producto) */
  const totalUnidCarrito = carrito.reduce(function(sum, item) {
    return sum + item.qty;
  }, 0);

  const aplicaMayor = totalUnidCarrito >= MINIMO_MAYOR;

  /* Actualizar precio de cada ítem */
  carrito.forEach(function(item) {
    if (!item.precioMayor) return; /* producto sin precio mayor → no tocar */

    /* Usar precioBase guardado en el ítem; si no existe, buscarlo en DB */
    var base = item.precioBase;
    if (!base) {
      const prod = todosProductos.find(function(p) { return p.id === item.prodId; });
      base = prod ? Number(prod.precio || prod.price || 0) : item.precio;
      item.precioBase = base; /* guardar para futuras llamadas */
    }

    item.precio = aplicaMayor ? item.precioMayor : base;
  });
}

function eliminarItemCarrito(idx) {
  carrito.splice(idx, 1);
  recalcularPreciosMayor();
  renderCarrito();
  actualizarBadge();
}

function vaciarCarrito() {
  if (!carrito.length) return;
  if (!confirm('¿Vaciar todo el carrito?')) return;
  carrito = [];
  cuponActivo = null;
  renderCarrito();
  actualizarBadge();
}

/* ── Resumen ── */
function calcularSubtotal() {
  return carrito.reduce((s, i) => s + i.precio * i.qty, 0);
}

function renderResumen() {
  const el = document.getElementById('cart-resumen');
  if (!el) return;

  const sub   = calcularSubtotal();
  let desc    = 0;
  let descTxt = '';
  let descHTML= '';

  if (cuponActivo) {
    if (cuponActivo.tipo === '%') {
      desc    = sub * (cuponActivo.valor / 100);
      descTxt = `-${cuponActivo.valor}%`;
      } else {
      desc    = Math.min(cuponActivo.valor, sub);
      descTxt = `-S/ ${cuponActivo.valor.toFixed(2)}`;
    }
    descHTML = `
      <div class="cr-row cr-desc">
        <span>Descuento <button class="cr-quitar" onclick="quitarCupon()">✕ quitar</button></span>
        <span>-S/ ${desc.toFixed(2)}</span>
      </div>`;
  }

  const total = Math.max(0, sub - desc);
  const nItems = carrito.reduce((s, i) => s + i.qty, 0);

  el.innerHTML = `
    <div class="cr-row"><span>${nItems} producto${nItems!==1?'s':''}</span><span>S/ ${sub.toFixed(2)}</span></div>
    ${descHTML}
    <div class="cr-divider"></div>
    <div class="cr-row cr-total"><span>Total</span><span>S/ ${total.toFixed(2)}</span></div>`;
}

/* ── Progreso de envío ── */
function actualizarProgreso(monto) {
  const fill  = document.getElementById('progressFill');
  const label = document.getElementById('progressAmt');
  if (!fill || !label) return;
  const pct  = Math.min(100, (monto / META_ENVIO) * 100);
  fill.style.width = pct + '%';
  if (monto >= META_ENVIO) {
    label.innerHTML = '<strong style="color:#06D6A0">🎉 ¡Envío gratis!</strong>';
  } else {
    const faltan = (META_ENVIO - monto).toFixed(2);
    label.innerHTML = `Agrega <strong>S/ ${faltan}</strong> más para envío gratis`;
  }
}

/* ── Badge ── */
function actualizarBadge() {
  const total = carrito.reduce((s, i) => s + i.qty, 0);

  /* Header badge */
  const hb = document.getElementById('cBadge');
  if (hb) { hb.textContent = total; hb.style.display = total ? 'flex' : 'none'; }

  /* Float badge */
  const fb = document.getElementById('floatBadge');
  if (fb) { fb.textContent = total; fb.style.display = total ? 'flex' : 'none'; }
}

/* ════════════════════════════════════════════════════════════
   CUPÓN
   ════════════════════════════════════════════════════════════ */
function aplicarCupon() {
  const inp = document.getElementById('cupon-inp');
  const msg = document.getElementById('cupon-msg');
  if (!inp || !msg) return;

  const codigo = (inp.value || '').trim().toUpperCase();
  if (!codigo) { msg.textContent = 'Ingresa un código.'; msg.className = 'cupon-msg err'; return; }

  const cupon = CUPONES[codigo];
  if (!cupon) {
    msg.textContent = 'Código inválido.';
    msg.className   = 'cupon-msg err';
    return;
  }

  cuponActivo = { codigo, ...cupon };
  msg.textContent = `✅ Cupón aplicado: ${cupon.tipo==='%' ? cupon.valor+'%' : 'S/'+cupon.valor} de descuento`;
  msg.className   = 'cupon-msg ok';
  inp.value       = '';
  renderResumen();
}

function quitarCupon() {
  cuponActivo = null;
  const msg = document.getElementById('cupon-msg');
  if (msg) { msg.textContent = ''; msg.className = 'cupon-msg'; }
  renderResumen();
}

/* ════════════════════════════════════════════════════════════
   PEDIDO POR WHATSAPP
   ════════════════════════════════════════════════════════════ */
function hacerPedido() {
  if (!carrito.length) return;

  const sub   = calcularSubtotal();
  let   desc  = 0;
  if (cuponActivo) {
    desc = cuponActivo.tipo === '%'
      ? sub * (cuponActivo.valor / 100)
      : Math.min(cuponActivo.valor, sub);
  }
  const total = Math.max(0, sub - desc);
  const nItems = carrito.reduce((s, i) => s + i.qty, 0);

  let lineas = `🛍️ *Pedido MAGAMA*\n`;
  lineas += `━━━━━━━━━━━━━━━━━━━\n`;

  carrito.forEach((item, i) => {
    lineas += `\n*${i+1}. ${item.nombre}*\n`;
    if (item.talla)  lineas += `   📐 Talla: ${item.talla}\n`;
    if (item.color)  lineas += `   🎨 Color: ${item.color}\n`;
    lineas += `   🔢 Cantidad: ${item.qty}\n`;
    lineas += `   💰 Precio: S/ ${item.precio.toFixed(2)} c/u\n`;
    lineas += `   💵 Subtotal: S/ ${(item.precio * item.qty).toFixed(2)}\n`;
  });

  lineas += `\n━━━━━━━━━━━━━━━━━━━\n`;
  lineas += `📦 ${nItems} producto${nItems!==1?'s':''}\n`;
  if (desc > 0) {
    lineas += `🏷️ Descuento (${cuponActivo.codigo}): -S/ ${desc.toFixed(2)}\n`;
  }
  lineas += `✅ *TOTAL: S/ ${total.toFixed(2)}*\n`;
  lineas += `\n¡Hola! Me gustaría hacer este pedido 😊`;

  const url = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(lineas)}`;
  window.open(url, '_blank');
}

/* ════════════════════════════════════════════════════════════
   UTILIDADES
   ════════════════════════════════════════════════════════════ */
function mostrarToastCarrito(msg, ok = true) {
  const toast = document.getElementById('cartToast');
  if (!toast) return;
  toast.querySelector('span').textContent = msg;
  const ico = toast.querySelector('i');
  if (ico) ico.className = ok ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), 3000);
}

function shakearElemento(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  el.style.animation = 'shake .4s ease';
  setTimeout(() => el.style.animation = '', 400);
}
