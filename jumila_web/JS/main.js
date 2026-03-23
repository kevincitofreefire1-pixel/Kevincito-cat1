// ================================================
// Jumila Importaciones - JavaScript principal
// ================================================
 
// --- MENÚ HAMBURGUESA ---
const hamburguesa = document.getElementById('hamburguesa');
const navLinks    = document.getElementById('nav-links');
 
hamburguesa.addEventListener('click', function() {
    navLinks.classList.toggle('abierto');
    hamburguesa.classList.toggle('activo');
});
 
navLinks.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', function() {
        navLinks.classList.remove('abierto');
        hamburguesa.classList.remove('activo');
    });
});
 
// --- SCROLL SUAVE ---
document.querySelectorAll('a[href^="#"]').forEach(function(enlace) {
    enlace.addEventListener('click', function(e) {
        e.preventDefault();
        const destino = document.querySelector(this.getAttribute('href'));
        if (destino) destino.scrollIntoView({ behavior: 'smooth' });
    });
});
 
// --- NAVBAR: sombra al hacer scroll ---
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 20px rgba(233,30,140,0.2)';
    } else {
        navbar.style.boxShadow = '0 2px 12px rgba(0,0,0,0.08)';
    }
});
 
// --- ANIMACIÓN DE ENTRADA DEL HERO ---
window.addEventListener('load', function() {
 
    // Cargar productos del panel admin automáticamente
    if (typeof JumilaStore !== 'undefined') {
        JumilaStore.renderizarTienda();
    }
 
    // Animar elementos del hero
    const elementos = [
        '.hero-badge',
        '.hero-titulo',
        '.hero-subtitulo',
        '.hero-botones'
    ];
 
    elementos.forEach(function(selector, indice) {
        const el = document.querySelector(selector);
        if (el) {
            el.style.opacity    = '0';
            el.style.transform  = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease';
            setTimeout(function() {
                el.style.opacity   = '1';
                el.style.transform = 'translateY(0)';
            }, 200 + (indice * 200));
        }
    });
 
    // Animar tarjetas al hacer scroll
    const elementosAnimar = document.querySelectorAll(
        '.producto-card, .categoria-card, .contacto-card, .badge-item'
    );
 
    elementosAnimar.forEach(function(el) {
        el.classList.add('animar');
    });
 
    const observador = new IntersectionObserver(function(entradas) {
        entradas.forEach(function(entrada) {
            if (entrada.isIntersecting) {
                entrada.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });
 
    elementosAnimar.forEach(function(el) {
        observador.observe(el);
    });
});
 
// --- FILTRO DE CATEGORÍAS ---
function filtrar(categoria, event) {
    // Resaltar categoría activa
    document.querySelectorAll('.categoria-card').forEach(function(card) {
        card.classList.remove('activa');
    });
    if (event && event.currentTarget) {
        event.currentTarget.classList.add('activa');
    }
 
    // Filtrar productos
    document.querySelectorAll('.producto-card').forEach(function(producto) {
        const cats = (producto.getAttribute('data-categoria') || '').split(' ');
        if (categoria === 'todos' || cats.includes(categoria)) {
            producto.classList.remove('oculto');
        } else {
            producto.classList.add('oculto');
        }
    });
}
 
console.log('✅ Jumila Importaciones cargado correctamente');