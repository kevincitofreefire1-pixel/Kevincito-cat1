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

async function agregarProducto(producto) {
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

async function agregarProductoSupabase(producto) {
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
        'Content-Type': archivo.type
      },
      body: archivo
    }
  );
  if (res.ok) {
    return `${SUPABASE_URL}/storage/v1/object/public/imagenes/${nombre}`;
  }
  return null;
}
