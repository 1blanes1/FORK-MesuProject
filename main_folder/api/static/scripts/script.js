const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const slidesContainer = document.querySelector('.slides-container');

nextBtn.addEventListener('click', () => {
    slidesContainer.scrollBy({ left: 340, behavior: 'smooth' }); // width + gap
});

prevBtn.addEventListener('click', () => {
    slidesContainer.scrollBy({ left: -340, behavior: 'smooth' });
});