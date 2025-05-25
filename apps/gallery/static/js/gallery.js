const carouselElements = document.querySelectorAll('#hover-carousel');

carouselElements.forEach((carouselEl) => {
  const carousel = new bootstrap.Carousel(carouselEl, {
    interval: 1500,
    ride: false,
    pause: false,
    wrap: true
  });

  carouselEl.addEventListener('mouseenter', () => {
    carousel.cycle();
  });

  carouselEl.addEventListener('mouseleave', () => {
    carousel.pause();
  });
});