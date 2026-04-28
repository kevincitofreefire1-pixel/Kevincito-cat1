const SUPABASE_URL = 'https://bxwddgmpywgtibduhrgl.supabase.co';
const SUPABASE_KEY = 'sb_publishable_yDGytx5M-brZ_vBsAnqhFQ_Na9yHe_V';

async function getProductosFromSupabase() {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/productos?select=*`, {
    headers: {
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`
    }
  });
  return await res.json();
}

async function agregarProductoSupabase(producto) {  // ✅ quitado el { ... }
  const res = await fetch(`${SUPABASE_URL}/rest/v1/productos`, {
    method: 'POST',
    headers: {
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=representation'
    },
    body: JSON.stringify(producto)
  });
  return await res.json();
}

async function subirImagen(archivo, nombre) {
  const res = await fetch(
    `${SUPABASE_URL}/storage/v1/object/imagenes/${nombre}`,
    {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'x-upsert': 'true'
      },
      body: archivo
    }
  );
  const data = await res.json();
  console.log('Storage response:', data);
  if (res.ok) {
    return `${SUPABASE_URL}/storage/v1/object/public/imagenes/${nombre}`;
  }
  console.error('Error subiendo imagen:', data);
  return null;
}

async function comprimirImagen(archivo, maxKB = 200) {
  return new Promise((resolve) => {
    const img = new Image();
    const url = URL.createObjectURL(archivo);
    img.onload = () => {
      const canvas = document.createElement('canvas');
      let w = img.width, h = img.height;
      const maxDim = 1200;
      if (w > maxDim || h > maxDim) {
        if (w > h) { h = Math.round(h * maxDim / w); w = maxDim; }
        else { w = Math.round(w * maxDim / h); h = maxDim; }
      }
      canvas.width = w;
      canvas.height = h;
      canvas.getContext('2d').drawImage(img, 0, 0, w, h);
      let quality = 0.8;
      const tryCompress = () => {
        canvas.toBlob(blob => {
          if (blob.size / 1024 <= maxKB || quality <= 0.1) {
            resolve(new File([blob], archivo.name, { type: 'image/jpeg' })); // ✅ corregido
          } else {
            quality -= 0.1;
            tryCompress();
          }
        }, 'image/jpeg', quality);
      };
      tryCompress();
    };
    img.src = url;
  });
}

async function eliminarImagen(url) {
  if (!url || !url.includes('supabase')) return;
  const nombre = url.split('/imagenes/').pop();
  await fetch(
    `${SUPABASE_URL}/storage/v1/object/imagenes/${nombre}`,
    {
      method: 'DELETE',
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`
      }
    }
  );
}
