#!/usr/bin/env python3
"""
Ejecutar en magama-web/:
    python3 fix_redes_sociales.py
"""

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

fixes = 0

# ══ FIX: Reemplazar enlaces de redes sociales en el footer ══
OLD_SOCIALS = """      <div class="ft-socials">
        <a class="soc-btn" href="https://wa.me/51925995264" target="_blank"><i class="fab fa-whatsapp"></i></a>
        <a class="soc-btn" href="#"><i class="fab fa-facebook-f"></i></a>
        <a class="soc-btn" href="#"><i class="fab fa-instagram"></i></a>
        <a class="soc-btn" href="#"><i class="fab fa-tiktok"></i></a>
      </div>"""

NEW_SOCIALS = """      <div class="ft-socials">
        <a class="soc-btn" href="https://wa.me/51925995264" target="_blank" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a class="soc-btn" href="https://www.facebook.com/profile.php?id=61565921951892" target="_blank" title="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a class="soc-btn" href="https://www.instagram.com/magama_huanuco" target="_blank" title="Instagram"><i class="fab fa-instagram"></i></a>
        <a class="soc-btn" href="https://www.tiktok.com/@magama" target="_blank" title="TikTok"><i class="fab fa-tiktok"></i></a>
      </div>"""

if OLD_SOCIALS in idx:
    idx = idx.replace(OLD_SOCIALS, NEW_SOCIALS, 1)
    print("✅ Enlaces de redes sociales actualizados en footer")
    fixes += 1
else:
    print("⚠️  Bloque de redes sociales no encontrado")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)

print(f"\n✅ {fixes}/1 fixes aplicados")
print()
print("🎉 Listo. Los iconos ahora llevan a:")
print("   WhatsApp  → wa.me/51925995264")
print("   Facebook  → facebook.com/profile.php?id=61565921951892")
print("   Instagram → instagram.com/magama_huanuco")
print("   TikTok    → tiktok.com/@magama")