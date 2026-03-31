// Modern Pure CSS/JS Category Project Slider - 3/2 cards responsive
document.addEventListener('DOMContentLoaded', () => {
  const categoryBtns = document.querySelectorAll('.category-btn');
  const portfolioSliders = document.querySelectorAll('.portfolio-slider');
  const leftArrow = document.querySelector('.arrow.left');
  const rightArrow = document.querySelector('.arrow.right');
  const sliderTrack = document.querySelector('.slider-track');
  const slides = document.querySelectorAll('.slide');

  let currentIndex = 0;
  let currentCategory = 0;

  // Category switching
  categoryBtns.forEach((btn, index) => {
    btn.addEventListener('click', () => {
      categoryBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      currentCategory = index;
      currentIndex = 0;
      updateSlider();
    });
  });

  // Arrow navigation
  leftArrow.addEventListener('click', () => {
    if (currentIndex > 0) currentIndex--;
    else currentIndex = slides.length - 1;
    updateSlider();
  });

  rightArrow.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % slides.length;
    updateSlider();
  });

  function updateSlider() {
    // Filter slides by current category
    const categorySlides = Array.from(slides).filter(s => {
      return s.dataset.category === categoryBtns[currentCategory].dataset.category;
    });

    // Center current slide
    const slideWidth = slides[currentIndex].offsetWidth + 20; // + gap
    const offset = slides[currentIndex].offsetLeft - (sliderTrack.offsetWidth / 2) + (slideWidth / 2);
    sliderTrack.scrollTo({
      left: offset,
      behavior: 'smooth'
    });

    // Update active states
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === currentIndex);
      slide.classList.remove('prev', 'next');
      if (i === currentIndex - 1) slide.classList.add('prev');
      if (i === currentIndex + 1) slide.classList.add('next');
    });
  }

  // Responsive resize
  window.addEventListener('resize', updateSlider);

  // Init
  if (categoryBtns[0]) categoryBtns[0].click();
});
