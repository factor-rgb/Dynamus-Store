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

function closeModal() {
  const wrapper = document.getElementById('modal');
  const panel = document.getElementById('modal-panel');
  const backdrop = document.getElementById('modal-backdrop');

  if (!wrapper || !panel || !backdrop) return;

  panel.classList.remove('animate-fadeInScale');
  panel.classList.add('animate-fadeOutScale');

  backdrop.classList.remove('animate-fadeInBackdrop');
  backdrop.classList.add('animate-fadeOutBackdrop');

  setTimeout(() => {
    wrapper.remove();
  }, 220);
}

document.body.addEventListener('htmx:afterSwap', function (event) {
  // Solo reaccionar si el modal fue insertado
  const modal = document.getElementById('modal');
  if (!modal) return;

  const backdrop = document.getElementById('modal-backdrop');
  const panel = document.getElementById('modal-panel');

  if (backdrop && panel) {
    backdrop.classList.add('animate-fadeInBackdrop');
    panel.classList.add('animate-fadeInScale');
  }
});

document.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
    const modal = document.getElementById('modal');
    if (modal) {
      closeModal();
    }
  }
});