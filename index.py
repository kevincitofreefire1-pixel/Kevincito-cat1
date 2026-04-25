#!/usr/bin/env python3
# Ejecutar este script en la carpeta donde está tu index.html
# python3 fix_index.py

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

fixes = 0

# FIX 1: srchClick usa products[] fijo → obtenerProductosActuales()
old1 = "if(type==='prod') { const p=products.find(x=>x.id==val); if(p){renderProds([p]);document.getElementById('productos').scrollIntoView({behavior:'smooth'});} }"
new1 = "if(type==='prod') { const p=obtenerProductosActuales().find(x=>x.id==val); if(p){renderProds([p]);document.getElementById('productos').scrollIntoView({behavior:'smooth'});} }"
if old1 in content:
    content = content.replace(old1, new1, 1)
    print("✅ FIX 1 aplicado: srchClick")
    fixes += 1
else:
    print("⚠️  FIX 1: texto no encontrado (puede que ya esté aplicado)")

# FIX 2: Init agrega storage listener
old2 = "const productosFinales = obtenerProductosActuales();\nrenderProds(productosFinales);"
new2 = """const productosFinales = obtenerProductosActuales();
renderProds(productosFinales);

window.addEventListener('storage', function(e){
  if(e.key === 'magama_productos'){
    renderProds(obtenerProductosActuales());
  }
});"""
if old2 in content:
    content = content.replace(old2, new2, 1)
    print("✅ FIX 2 aplicado: storage listener")
    fixes += 1
else:
    print("⚠️  FIX 2: texto no encontrado (puede que ya esté aplicado)")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{'✅ index.html actualizado con ' + str(fixes) + ' fix(es)' if fixes else '⚠️  No se aplicaron cambios'}")
