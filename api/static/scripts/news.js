
let allNews = []; // Глобальный массив всех новостей
const ITEMS_PER_PAGE = 10;
let currentPage = 1;

function renderNewsPage(page) {
    const startIndex = (page - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const pageNews = allNews.slice(startIndex, endIndex);

    const newsWrapper = document.getElementById('news-wrapper');
    if (!newsWrapper) {
        console.error('Контейнер .news-wrapper не найден!');
        return;
    }

    // Очищаем контейнер
    newsWrapper.innerHTML = '';

    // Добавляем карточки
    pageNews.forEach(news => {
        const newsItem = document.createElement('div');
        newsItem.className = 'news-item';

        // Изображение слева
        const newsImg = document.createElement('img');
        newsImg.className = 'news-img';
        newsImg.src = news.img_path || '';
        newsImg.alt = news.title || 'Изображение новости';

        // Контейнер для правой части
        const cardWrapper = document.createElement('div');
        cardWrapper.className = 'news-card-wrapper';

        // Создаём ссылку-обёртку
        const newsLink = document.createElement('a');
        newsLink.href = news.url || '#';
        newsLink.className = 'news-link';

        // Название 
        const newsTitle = document.createElement('h3');
        newsTitle.className = 'news-title';
        newsTitle.textContent = news.title || 'Без названия';

        // Описание
        const newDesc = document.createElement('p');
        newDesc.className = 'news-desc';
        newDesc.textContent = news.description || news.title || 'Без описания';

        // Сборка
        newsLink.appendChild(newsTitle);
        newsLink.appendChild(newDesc);

        cardWrapper.appendChild(newsLink);

        newsItem.appendChild(newsImg);
        newsItem.appendChild(cardWrapper);
        newsWrapper.appendChild(newsItem);
    });

    renderPagination();
}

function renderPagination() {
    const totalPages = Math.ceil(allNews.length / ITEMS_PER_PAGE);
    const paginationContainer = document.getElementById('pagination');

    if (!paginationContainer || totalPages <= 1) {
        if (paginationContainer) paginationContainer.innerHTML = '';
        return;
    }

    paginationContainer.innerHTML = '';

    // --- Вспомогательные функции ---

    const createPageButton = (pageNum) => {
        const btn = document.createElement('button');
        btn.className = 'page-btn';
        btn.textContent = pageNum;
        if (pageNum === currentPage) {
            btn.classList.add('active');
        }
        btn.onclick = () => {
            currentPage = pageNum;
            renderNewsPage(currentPage);
        };
        return btn;
    };

    const createDots = () => {
        const dots = document.createElement('span');
        dots.className = 'dots';
        dots.textContent = '...';
        return dots;
    };

    // --- Кнопка "Назад" ---
    if (currentPage > 1) {
        const prevBtn = document.createElement('button');
        prevBtn.className = 'last-btn'; // используем тот же класс, что и у "Вперёд"
        prevBtn.textContent = '◀◀';
        prevBtn.onclick = () => {
            currentPage--;
            renderNewsPage(currentPage);
        };
        paginationContainer.appendChild(prevBtn);
    }

    // --- Страницы ---

    // Всегда показываем первую страницу
    paginationContainer.appendChild(createPageButton(1));

    let showDotsBefore = false;
    let showDotsAfter = false;

    if (totalPages <= 5) {
        // Если ≤5 страниц — показываем все
        for (let i = 2; i <= totalPages; i++) {
            paginationContainer.appendChild(createPageButton(i));
        }
    } else {
        // Иначе — умная пагинация
        const siblingCount = 1; // сколько страниц отображать рядом с текущей

        const startPage = Math.max(2, currentPage - siblingCount);
        const endPage = Math.min(totalPages - 1, currentPage + siblingCount);

        // Троеточие перед блоком, если первая страница "отделена"
        if (startPage > 2) {
            showDotsBefore = true;
        }

        // Троеточие после блока, если последняя страница "отделена"
        if (endPage < totalPages - 1) {
            showDotsAfter = true;
        }

        // Добавляем блок страниц
        if (showDotsBefore) {
            paginationContainer.appendChild(createDots());
        }

        for (let i = startPage; i <= endPage; i++) {
            paginationContainer.appendChild(createPageButton(i));
        }

        if (showDotsAfter) {
            paginationContainer.appendChild(createDots());
        }

        // Всегда показываем последнюю страницу
        if (totalPages > 1) {
            paginationContainer.appendChild(createPageButton(totalPages));
        }
    }

    // --- Кнопка "Вперёд" ---
    if (currentPage < totalPages) {
        const nextBtn = document.createElement('button');
        nextBtn.className = 'last-btn';
        nextBtn.textContent = '▶▶';
        nextBtn.onclick = () => {
            currentPage++;
            renderNewsPage(currentPage);
        };
        paginationContainer.appendChild(nextBtn);
    }
}

async function loadNews() {
    try {
        const res = await fetch('/news');
        if (!res.ok) {
            throw new Error(`Ошибка загрузки: ${res.status}`);
        }

        allNews = await res.json(); // Загружаем все новости
        console.log(`Загружено ${allNews.length} новостей`);

        currentPage = 1;
        renderNewsPage(currentPage);

    } catch (error) {
        console.error('Ошибка при загрузке новостей:', error);
        const newsWrapper = document.getElementById('news-wrapper');
        if (newsWrapper) {
            newsWrapper.innerHTML = '<p>Не удалось загрузить новости. Попробуйте позже.</p>';
        }
    }
}

// Загружаем новости при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadNews();
});
