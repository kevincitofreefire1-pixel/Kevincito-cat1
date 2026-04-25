#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_urgencia.py

Actualiza el Feature #8 para mostrar mensajes de urgencia persuasivos:
- "👁 127 personas vieron esto hoy"
- "🔥 3 personas lo están viendo ahora"
- "⚡ 8 vendidos en las últimas 24h"
"""

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes = 0

# ══ FIX 1: Actualizar CSS de prod-stats ══
OLD_CSS = """    /* ============================================================
       CONTADORES DE VISTAS Y VENDIDOS
       ============================================================ */
    .prod-stats {
      display: flex; align-items: center; gap: 10px;
      padding: 0 16px 10px;
      font-size: .68rem; color: var(--gray-500);
    }
    .prod-stat {
      display: flex; align-items: center; gap: 4px;
      font-weight: 600;
    }
    .prod-stat i { font-size: .62rem; }
    .prod-stat.vistas i  { color: var(--navy-mid); }
    .prod-stat.vendidos i { color: #06D6A0; }
    .prod-stat-sep { color: var(--gray-200); }"""

NEW_CSS = """    /* ============================================================
       CONTADORES DE URGENCIA — VISTAS Y VENDIDOS
       ============================================================ */
    .prod-stats {
      display: flex; flex-direction: column; gap: 4px;
      padding: 0 16px 10px;
    }
    .prod-stat {
      display: flex; align-items: center; gap: 5px;
      font-size: .7rem; font-weight: 600;
      line-height: 1.3;
    }
    .prod-stat i { font-size: .65rem; flex-shrink: 0; }
    .prod-stat.vistas   { color: var(--navy-mid); }
    .prod-stat.viendo   { color: var(--accent); }
    .prod-stat.vendidos { color: #039d76; }
    .prod-stat.vistas i  { color: var(--navy-mid); }
    .prod-stat.viendo i  { color: var(--accent); animation: urgPulse 1.2s ease-in-out infinite; }
    .prod-stat.vendidos i { color: #039d76; }
    @keyframes urgPulse { 0%,100%{opacity:1} 50%{opacity:.45} }
    .prod-stat-sep { display: none; }"""

if OLD_CSS in idx:
    idx = idx.replace(OLD_CSS, NEW_CSS, 1)
    print("✅ FIX 1: CSS urgencia actualizado")
    fixes += 1
else:
    print("⚠️  FIX 1: CSS prod-stats no encontrado")

# ══ FIX 2: Actualizar statsFormatear y agregar función de urgencia ══
OLD_FORMAT = """function statsFormatear(n) {
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
  return String(n);
}"""

NEW_FORMAT = """function statsFormatear(n) {
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
  return String(n);
}

function statsUrgenciaHTML(prodId) {
  const st = statsObtener(prodId);
  const vistas   = st.vistas   || 0;
  const vendidos = st.vendidos || 0;

  if (!vistas && !vendidos) return '';

  /* Simular "viendo ahora" = entre 2 y 8, basado en vistas recientes */
  const viendoAhora = vistas > 0 ? Math.max(2, Math.min(8, Math.floor(vistas * 0.08) + 1)) : 0;

  var html = '<div class="prod-stats">';

  if (vistas > 0) {
    var textoVistas = vistas === 1
      ? '1 persona vio esto hoy'
      : statsFormatear(vistas) + ' personas vieron esto hoy';
    html += '<div class="prod-stat vistas"><i class="fas fa-eye"></i> ' + textoVistas + '</div>';
  }

  if (viendoAhora > 0 && vistas >= 3) {
    html += '<div class="prod-stat viendo"><i class="fas fa-fire"></i> ' + viendoAhora + ' personas lo están viendo ahora</div>';
  }

  if (vendidos > 0) {
    var textoVendidos = vendidos === 1
      ? '⚡ 1 vendido recientemente'
      : '⚡ ' + statsFormatear(vendidos) + ' vendidos recientemente';
    html += '<div class="prod-stat vendidos"><i class="fas fa-bolt"></i> ' + textoVendidos + '</div>';
  }

  html += '</div>';
  return html;
}"""

if OLD_FORMAT in idx:
    idx = idx.replace(OLD_FORMAT, NEW_FORMAT, 1)
    print("✅ FIX 2: función statsUrgenciaHTML agregada")
    fixes += 1
else:
    print("⚠️  FIX 2: statsFormatear no encontrado")

# ══ FIX 3: Reemplazar el bloque de stats en renderProds ══
OLD_RENDER_STATS = """      ${mayorHtml}
      ${countdownHtml}
      ${(function() {
        const st = statsObtener(p.id);
        const v  = st.vistas   || 0;
        const ve = st.vendidos || 0;
        if (!v && !ve) return '';
        return '<div class="prod-stats">' +
          (v  ? '<span class="prod-stat vistas"><i class="fas fa-eye"></i> ' + statsFormatear(v) + ' vistas</span>' : '') +
          (v && ve ? '<span class="prod-stat-sep">·</span>' : '') +
          (ve ? '<span class="prod-stat vendidos"><i class="fas fa-shopping-bag"></i> ' + statsFormatear(ve) + ' vendidos</span>' : '') +
        '</div>';
      })()}"""

NEW_RENDER_STATS = """      ${mayorHtml}
      ${countdownHtml}
      ${statsUrgenciaHTML(p.id)}"""

if OLD_RENDER_STATS in idx:
    idx = idx.replace(OLD_RENDER_STATS, NEW_RENDER_STATS, 1)
    print("✅ FIX 3: render de urgencia en tarjetas")
    fixes += 1
else:
    # Intentar sin countdown
    OLD_RENDER_STATS2 = """      ${mayorHtml}
      ${(function() {
        const st = statsObtener(p.id);
        const v  = st.vistas   || 0;
        const ve = st.vendidos || 0;
        if (!v && !ve) return '';
        return '<div class="prod-stats">' +
          (v  ? '<span class="prod-stat vistas"><i class="fas fa-eye"></i> ' + statsFormatear(v) + ' vistas</span>' : '') +
          (v && ve ? '<span class="prod-stat-sep">·</span>' : '') +
          (ve ? '<span class="prod-stat vendidos"><i class="fas fa-shopping-bag"></i> ' + statsFormatear(ve) + ' vendidos</span>' : '') +
        '</div>';
      })()}"""
    NEW_RENDER_STATS2 = """      ${mayorHtml}
      ${statsUrgenciaHTML(p.id)}"""
    if OLD_RENDER_STATS2 in idx:
        idx = idx.replace(OLD_RENDER_STATS2, NEW_RENDER_STATS2, 1)
        print("✅ FIX 3b: render de urgencia en tarjetas (alternativo)")
        fixes += 1
    else:
        print("⚠️  FIX 3: bloque stats en renderProds no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ {fixes}/3 fixes aplicados")
print()
print("🎉 Listo. Ahora los productos mostrarán:")
print("   👁 127 personas vieron esto hoy")
print("   🔥 3 personas lo están viendo ahora")
print("   ⚡ 8 vendidos recientemente")
print()
print("Los números aparecen después de que alguien haga clic en el producto.")