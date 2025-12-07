const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const slidesContainer = document.querySelector('.slides-container');

// Получаем ширину одной карточки с учетом gap
function getScrollAmount() {
  const card = document.querySelector('.historical-line');
  const cardWidth = card.offsetWidth || 280; // fallback значение
  const gap = parseInt(window.getComputedStyle(slidesContainer).gap) || 60;
  
  // Определяем сколько карточек показывать в зависимости от ширины экрана
  let cardsToScroll = 1;
  
  if (window.innerWidth >= 1024) {
    cardsToScroll = 3; // Десктоп
  } else if (window.innerWidth >= 768) {
    cardsToScroll = 2; // Планшет
  } else {
    cardsToScroll = 1; // Телефон
  }
  
  return (cardWidth + gap) * cardsToScroll;
}

nextBtn.addEventListener('click', () => {
  const scrollAmount = getScrollAmount();
  slidesContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' });
});

prevBtn.addEventListener('click', () => {
  const scrollAmount = getScrollAmount();
  slidesContainer.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
});

// Обновляем при изменении размера окна
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    // Принудительно центрируем первую карточку после ресайза
    slidesContainer.scrollTo({ left: 0, behavior: 'auto' });
  }, 250);
});

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
  // Центрируем первую карточку на мобильных
  if (window.innerWidth < 768) {
    slidesContainer.scrollTo({ left: 0, behavior: 'auto' });
  }
});