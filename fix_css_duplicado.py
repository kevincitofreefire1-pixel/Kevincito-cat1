#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_css_duplicado.py
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar y eliminar el segundo bloque CSS de contadores
# (puede tener ligeras variaciones de espaciado)
marcador = 'CONTADORES DE VISTAS Y VENDIDOS'
count = content.count(marcador)
print(f"Bloques CSS contadores encontrados: {count}")

if count == 2:
    # Encontrar ambas posiciones
    first  = content.find(marcador)
    second = content.find(marcador, first + len(marcador))

    # El segundo bloque empieza con el comentario CSS antes del marcador
    # Buscar el inicio real del segundo bloque (el /* antes del marcador)
    inicio_segundo = content.rfind('    /*', 0, second)

    # El segundo bloque termina con el último .prod-stat-sep antes del </style>
    fin_segundo = content.find('.prod-stat-sep { color: var(--gray-200); }', second)
    fin_segundo = content.find('\n', fin_segundo) + 1  # incluir el salto de línea

    # Eliminar el segundo bloque
    content = content[:inicio_segundo] + content[fin_segundo:]
    print("✅ Segundo bloque CSS contadores eliminado")
elif count == 1:
    print("✅ Ya estaba limpio — solo 1 bloque")
else:
    print(f"⚠️  {count} bloques encontrados")

# Verificación
print(f"\nVerificación final:")
print(f"  CSS contadores: {content.count(marcador)} vez (debe ser 1)")
print(f"  JS statsCargar: {content.count('function statsCargar()')} vez (debe ser 1)")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Listo")