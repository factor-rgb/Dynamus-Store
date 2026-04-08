// MOBILE NAVBAR SCRIPT
const menuBtn = document.getElementById('menu-btn');
const menu = document.getElementById('menu');
const menuIcon = document.getElementById('menu-icon');
let menuOpen = false;

menuBtn.addEventListener('click', () => {
  if (!menuOpen) {
    // OPEN MENU
    menu.style.maxHeight = menu.scrollHeight + 'px';
    menuOpen = true;
    menuIcon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
  } else {
    // CLOSE MENU
    menu.style.maxHeight = '0px';
    menuOpen = false;
    menuIcon.innerHTML =
      '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
  }
});


window.addEventListener('resize', () => {
  if (window.innerWidth >= 768) {
    menu.style.maxHeight = 'none';
  } else if (!menuOpen) {
    menu.style.maxHeight = '0px';
  }
});


// MODAL SCRIPT
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


// HEADER SCRIPT
document.addEventListener("DOMContentLoaded", function(){

const track = document.getElementById("sliderTrack")
if(!track) return

const slides = track.children
const nextBtn = document.getElementById("nextBtn")
const prevBtn = document.getElementById("prevBtn")
const indicatorsContainer = document.getElementById("indicators")
const slider = document.getElementById("slider")

let index = 0
let autoplayInterval


// INDICATORS
for(let i = 0; i < slides.length; i++){

    const dot = document.createElement("button")
    dot.className = "w-3 h-3 rounded-full bg-white/50 hover:bg-white transition-all duration-300 scale-100 hover:scale-125"

    dot.addEventListener("click", ()=>{
        index = i
        updateSlide()
        resetAutoplay()
    })

    indicatorsContainer.appendChild(dot)
}

const indicators = indicatorsContainer.children


function updateIndicators(){

    for(let i = 0; i < indicators.length; i++){
        indicators[i].classList.remove("bg-white")
        indicators[i].classList.add("bg-white/50")
    }

    indicators[index].classList.add("bg-white")
}


function updateSlide(){
    track.style.transform = `translateX(-${index * 100}%)`
    updateIndicators()
}


function nextSlide(){
    index++
    if(index >= slides.length){
        index = 0
    }
    updateSlide()
}


function prevSlide(){
    index--
    if(index < 0){
        index = slides.length - 1
    }
    updateSlide()
}


// BUTTONS
nextBtn.addEventListener("click", ()=>{
    nextSlide()
    resetAutoplay()
})

prevBtn.addEventListener("click", ()=>{
    prevSlide()
    resetAutoplay()
})


// AUTOPLAY
function startAutoplay(){
    autoplayInterval = setInterval(nextSlide, 4000)
}

function stopAutoplay(){
    clearInterval(autoplayInterval)
}

function resetAutoplay(){
    stopAutoplay()
    startAutoplay()
}

startAutoplay()


// PAUSE HOVER
slider.addEventListener("mouseenter", stopAutoplay)
slider.addEventListener("mouseleave", startAutoplay)


// SWIPE MOBILE
let startX = 0
let endX = 0

slider.addEventListener("touchstart", (e)=>{
    startX = e.touches[0].clientX
})

slider.addEventListener("touchend", (e)=>{
    endX = e.changedTouches[0].clientX
    handleSwipe()
})

function handleSwipe(){

    const diff = startX - endX

    if(Math.abs(diff) > 50){

        if(diff > 0){
            nextSlide()
        }else{
            prevSlide()
        }

        resetAutoplay()
    }
}

updateIndicators()

})


// ROADMAP CARDS SCRIPT
const steps = document.querySelectorAll(".step");

const observer = new IntersectionObserver(entries => {
  entries.forEach((entry, index) => {
    if (entry.isIntersecting) {
      entry.target.style.transitionDelay = `${index * 0.3}s`;

      entry.target.classList.remove("opacity-0","translate-y-10");
      entry.target.classList.add("opacity-100","translate-y-0");
    }
  });
}, { threshold: 0.3 });

steps.forEach(step => observer.observe(step));


// MESSAGES SCRIPT
document.addEventListener("DOMContentLoaded", function () {
    const toast = document.getElementById("toast");
    const closeBtn = document.getElementById("closeToast");

    if (toast) {
        setTimeout(() => {
            toast.classList.remove("opacity-0", "translate-y-5");
        }, 100);

        const hideToast = () => {
            toast.classList.add("opacity-0", "translate-y-5");
        };

        setTimeout(hideToast, 5000);

        if (closeBtn) {
            closeBtn.addEventListener("click", hideToast);
        }
    }
});