#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_admin_oferta_fin.py

Hace SOLO 3 cambios en admin/index.html:
1. Agrega campo de fecha fin de ofertas en el panel Últimas Unidades
2. guardarConfig() guarda también la fecha
3. cargarHeroAdmin() carga también la fecha
"""

with open('admin/index.html', 'r', encoding='utf-8') as f:
    adm = f.read()

print(f"Admin leído: {adm.count(chr(10))} líneas")
fixes = 0

# ══ FIX 1: Agregar campo de fecha al panel Últimas Unidades ══
OLD_1 = """          <div class="form-group">
            <label class="form-label">Límite para mostrar alerta "Últimas unidades"</label>
            <input class="form-input" type="number" min="1" max="20" id="cfg-stock-limite" value="5" placeholder="5" style="max-width:200px"/>
            <div style="font-size:.7rem;color:var(--g500);margin-top:6px">Si un producto tiene ≤ este número de unidades, aparece la alerta roja en la tarjeta.</div>
          </div>"""

NEW_1 = """          <div class="form-group">
            <label class="form-label">Límite para mostrar alerta "Últimas unidades"</label>
            <input class="form-input" type="number" min="1" max="20" id="cfg-stock-limite" value="5" placeholder="5" style="max-width:200px"/>
            <div style="font-size:.7rem;color:var(--g500);margin-top:6px">Si un producto tiene ≤ este número de unidades, aparece la alerta roja en la tarjeta.</div>
          </div>
          <div class="form-group" style="margin-top:16px">
            <label class="form-label"><i class="fas fa-clock" style="color:var(--sky);margin-right:4px"></i>Fecha fin de ofertas</label>
            <input class="form-input" type="datetime-local" id="cfg-oferta-fin" style="max-width:280px"/>
            <div style="font-size:.7rem;color:var(--g500);margin-top:6px">Fecha y hora en que terminan las ofertas. Si está vacío, usa el próximo domingo a medianoche.</div>
          </div>"""

if OLD_1 in adm:
    adm = adm.replace(OLD_1, NEW_1, 1)
    print("✅ FIX 1: campo fecha fin de ofertas agregado")
    fixes += 1
else:
    print("⚠️  FIX 1: panel Últimas Unidades no encontrado")

# ══ FIX 2: guardarConfig() guarda la fecha ══
OLD_2 = """function guardarConfig(){
  const limite = document.getElementById('cfg-stock-limite');
  if(limite && limite.value) localStorage.setItem('magama_stock_limite', limite.value);
  showToast('Configuración guardada correctamente');
}"""

NEW_2 = """function guardarConfig(){
  const limite = document.getElementById('cfg-stock-limite');
  if(limite && limite.value) localStorage.setItem('magama_stock_limite', limite.value);
  const ofertaFin = document.getElementById('cfg-oferta-fin');
  if(ofertaFin && ofertaFin.value) localStorage.setItem('magama_oferta_fin', ofertaFin.value);
  else localStorage.removeItem('magama_oferta_fin');
  showToast('Configuración guardada correctamente');
}"""

if OLD_2 in adm:
    adm = adm.replace(OLD_2, NEW_2, 1)
    print("✅ FIX 2: guardarConfig() guarda fecha fin de ofertas")
    fixes += 1
else:
    print("⚠️  FIX 2: guardarConfig() no encontrado")

# ══ FIX 3: cargarHeroAdmin() carga la fecha ══
OLD_3 = """  const limite = localStorage.getItem('magama_stock_limite');
  const elLimite = document.getElementById('cfg-stock-limite');
  if(limite && elLimite) elLimite.value = limite;"""

NEW_3 = """  const limite = localStorage.getItem('magama_stock_limite');
  const elLimite = document.getElementById('cfg-stock-limite');
  if(limite && elLimite) elLimite.value = limite;
  const ofertaFin = localStorage.getItem('magama_oferta_fin');
  const elOferta = document.getElementById('cfg-oferta-fin');
  if(ofertaFin && elOferta) elOferta.value = ofertaFin;"""

if OLD_3 in adm:
    adm = adm.replace(OLD_3, NEW_3, 1)
    print("✅ FIX 3: cargarHeroAdmin() carga fecha fin de ofertas")
    fixes += 1
else:
    print("⚠️  FIX 3: cargarHeroAdmin() no encontrado")

with open('admin/index.html', 'w', encoding='utf-8') as f:
    f.write(adm)

print(f"\n✅ {fixes}/3 fixes aplicados")
if fixes == 3:
    print("\n🎉 Admin listo.")
    print("   En Admin → Configuración → 'Últimas Unidades'")
    print("   ahora verás el campo 'Fecha fin de ofertas'")
    print("   Guarda y el contador regresivo en la tienda usará esa fecha.")