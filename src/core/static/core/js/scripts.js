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

// SLIDE VARIABLES
let slides = Array.from(track.children)
let index = 1
let autoplayInterval

const firstClone = slides[0].cloneNode(true)
const lastClone = slides[slides.length - 1].cloneNode(true)
const nextBtn = document.getElementById("nextBtn")
const prevBtn = document.getElementById("prevBtn")
const indicatorsContainer = document.getElementById("indicators")
const slider = document.getElementById("slider")

track.appendChild(firstClone)
track.insertBefore(lastClone, slides[0])
track.style.transform = `translateX(-${index * 100}%)`

slides = Array.from(track.children)


// INDICATORS
const realSlidesCount = slides.length - 2
for(let i = 0; i < realSlidesCount; i++){

    const dot = document.createElement("button")
    dot.className = "w-3 h-3 rounded-full bg-white/50 hover:bg-white transition-all duration-300 scale-100 hover:scale-125"

    dot.addEventListener("click", ()=>{
        index = i + 1
        updateSlide()
        resetAutoplay()
    })

    indicatorsContainer.appendChild(dot)
}

const indicators = indicatorsContainer.children

function updateIndicators(){

    let activeIndex = index - 1

    if(index === 0){
        activeIndex = realSlidesCount - 1
    }

    if(index === slides.length - 1){
        activeIndex = 0
    }

    for(let i = 0; i < indicators.length; i++){

        indicators[i].classList.remove("bg-white")
        indicators[i].classList.add("bg-white/50")

    }

    indicators[activeIndex].classList.add("bg-white")
}


// SLIDE CHANGER FUNCTIONS
function updateSlide(){
    track.style.transform = `translateX(-${index * 100}%)`
    updateIndicators()
}

track.addEventListener("transitionend", (e) => {

    if (e.propertyName !== "transform") return;

    if(index === slides.length - 1){

        track.style.transition = "none";

        index = 1;

        track.style.transform = `translateX(-${index * 100}%)`;

        track.offsetHeight;

        track.style.transition = "";

    }

    if(index === 0){

        track.style.transition = "none";

        index = slides.length - 2;

        track.style.transform = `translateX(-${index * 100}%)`;

        track.offsetHeight;

        track.style.transition = "";

    }

});

function nextSlide(){

    if(index >= slides.length - 1) return

    index++
    updateSlide()

}

function prevSlide(){

    if(index <= 0) return

    index--
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

    clearInterval(autoplayInterval)

    autoplayInterval = setInterval(() => {

        if(isInteracting) return

        nextSlide()

    }, 5000)

}

function stopAutoplay(){
    clearInterval(autoplayInterval)
}

function resetAutoplay(){

    if(slider.matches(":hover")){
        return
    }

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
let isInteracting = false

// SWIPE INTERACTIONS
slider.addEventListener("touchstart", (e) => {

    isInteracting = true
    stopAutoplay()

    startX = e.touches[0].clientX

})

slider.addEventListener("touchmove", () => {

    isInteracting = true

})

slider.addEventListener("touchend", (e) => {

    endX = e.changedTouches[0].clientX

    handleSwipe()

    isInteracting = false

    startAutoplay()

})

slider.addEventListener("touchcancel", () => {

    isInteracting = false
    startAutoplay()

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