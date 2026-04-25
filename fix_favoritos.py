#!/usr/bin/env python3
"""
Ejecutar en la carpeta donde está tu index.html:
    python3 fix_favoritos.py

Solo hace 1 cambio: agrega <script src="js/favoritos.js"> en index.html
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

fixes = 0

# Agregar favoritos.js antes de producto-detalle.js
OLD = '<script src="js/producto-detalle.js"></script>'
NEW = '<script src="js/favoritos.js"></script>\n<script src="js/producto-detalle.js"></script>'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print("✅ favoritos.js agregado en index.html")
    fixes += 1
else:
    # Intentar antes de carrito.js como alternativa
    OLD2 = '<script src="js/carrito.js"></script>'
    NEW2 = '<script src="js/favoritos.js"></script>\n<script src="js/carrito.js"></script>'
    if OLD2 in content:
        content = content.replace(OLD2, NEW2, 1)
        print("✅ favoritos.js agregado antes de carrito.js")
        fixes += 1
    else:
        print("⚠️  No se encontró el punto de inserción automático.")
        print("   Agrega manualmente esta línea antes de carrito.js:")
        print('   <script src="js/favoritos.js"></script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'✅ index.html actualizado' if fixes else '⚠️  Agrega el script manualmente'}")
print("\nRECUERDA: copia favoritos.js a tu carpeta js/")
