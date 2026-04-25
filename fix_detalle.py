#!/usr/bin/env python3
"""
Ejecutar en la carpeta donde está tu index.html:
    python3 fix_detalle.py

Hace 3 cambios en index.html:
  1. Agrega <script src="js/producto-detalle.js"> antes de carrito.js
  2. Hace la imagen de cada tarjeta clickeable para abrir el detalle
  3. Hace el nombre del producto clickeable para abrir el detalle
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

fixes = 0

# ── FIX 1: Agregar script de detalle antes de carrito.js ──
OLD1 = '<script src="js/carrito.js"></script>'
NEW1 = '<script src="js/producto-detalle.js"></script>\n<script src="js/carrito.js"></script>'

if OLD1 in content:
    content = content.replace(OLD1, NEW1, 1)
    print("✅ FIX 1: script producto-detalle.js agregado")
    fixes += 1
else:
    print("⚠️  FIX 1: no se encontró <script src='js/carrito.js'>")
    print("   Agrega manualmente antes de carrito.js:")
    print('   <script src="js/producto-detalle.js"></script>')

# ── FIX 2: Hacer la imagen de la tarjeta clickeable ──
# En renderProds(), el thumb tiene: onclick="agregarAlCarrito(${p.id})"  NO
# El prod-thumb NO tiene onclick, lo agregamos apuntando a abrirDetalle
OLD2 = """      <div class="prod-thumb" style="background:${p.bg||'#dbeafe'};position:relative">
        ${thumbContent}
        ${badge ? `<span class="ptag ptag-${badge}">${tagTxt}</span>` : ''}
        <button class="pwish" onclick="toggleWishlist(this)"><i class="far fa-heart"></i></button>
      </div>"""

NEW2 = """      <div class="prod-thumb" style="background:${p.bg||'#dbeafe'};position:relative;cursor:pointer" onclick="abrirDetalle(${p.id})">
        ${thumbContent}
        ${badge ? `<span class="ptag ptag-${badge}">${tagTxt}</span>` : ''}
        <button class="pwish" onclick="event.stopPropagation();toggleWishlist(this)"><i class="far fa-heart"></i></button>
      </div>"""

if OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    print("✅ FIX 2: imagen de tarjeta clickeable (abrirDetalle)")
    fixes += 1
else:
    print("⚠️  FIX 2: no se encontró el bloque prod-thumb exacto")
    print("   Busca en renderProds() la línea class='prod-thumb'")
    print("   y agrega: onclick=\"abrirDetalle(${p.id})\"")

# ── FIX 3: Hacer el nombre del producto clickeable ──
OLD3 = '        <div class="prod-name">${nombre}</div>'
NEW3 = '        <div class="prod-name" style="cursor:pointer" onclick="abrirDetalle(${p.id})">${nombre}</div>'

if OLD3 in content:
    content = content.replace(OLD3, NEW3, 1)
    print("✅ FIX 3: nombre del producto clickeable (abrirDetalle)")
    fixes += 1
else:
    print("⚠️  FIX 3: no se encontró el div prod-name exacto")
    print("   Busca: <div class=\"prod-name\">${nombre}</div>")
    print("   y agrega: style=\"cursor:pointer\" onclick=\"abrirDetalle(${p.id})\"")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'✅ index.html actualizado con ' + str(fixes) + ' cambio(s)' if fixes else '⚠️  No se aplicaron cambios automáticos'}")
print("\nRECUERDA: copia producto-detalle.js a tu carpeta js/")
