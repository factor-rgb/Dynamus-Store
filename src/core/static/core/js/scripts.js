const menuBtn = document.getElementById('menu-btn');
const menu = document.getElementById('menu');
const menuIcon = document.getElementById('menu-icon');
let menuOpen = false;

menuBtn.addEventListener('click', () => {
  if (!menuOpen) {
    // Abrir menú
    menu.style.maxHeight = menu.scrollHeight + 'px';
    menuOpen = true;
    menuIcon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
  } else {
    // Cerrar menú
    menu.style.maxHeight = '0px';
    menuOpen = false;
    menuIcon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
  }
});

// Ajustar en pantallas grandes
window.addEventListener('resize', () => {
  if (window.innerWidth >= 768) {
    menu.style.maxHeight = 'none';
  } else if (!menuOpen) {
    menu.style.maxHeight = '0px';
  }
});