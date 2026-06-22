function addPartnerCard(title, img_path, url) {
    // Находим контейнер для партнёров
    const partnersWrapper = document.getElementById('partners-wrapper');
    if (!partnersWrapper) {
        console.error('Контейнер #partners-wrapper не найден!');
        return;
    }

    // Создаём карточку партнёра
    const partnerCard = document.createElement('div');
    partnerCard.className = 'organizer-card partner-card'; // класс остаётся как в разметке

    // Создаём изображение
    const img = document.createElement('img');
    img.className = 'organizer-logo';
    img.src = img_path;
    img.alt = title || 'Логотип партнёра';

    // Создаём заголовок
    const titleEl = document.createElement('h3');
    titleEl.textContent = title || 'Без названия';

    // Создаём абзац с описанием (в текущих данных его нет, оставим пустым или можно позже расширить)
    const descEl = document.createElement('p');
    descEl.textContent = ''; // чтобы карточка не "схлопывалась", если описания нет

    // Собираем структуру карточки
    partnerCard.appendChild(img);
    partnerCard.appendChild(titleEl);
    partnerCard.appendChild(descEl);

    // Оборачиваем в ссылку
    const link = document.createElement('a');
    link.href = url || '#';
    link.className = 'partner-link';
    link.appendChild(partnerCard);
    partnersWrapper.appendChild(link);
}

async function loadPartners() {
    try {
        const res = await fetch('/partners'); // Эндпоинт, откуда приходят партнёры
        if (!res.ok) {
            throw new Error(`Ошибка загрузки партнёров: ${res.status}`);
        }

        const partners = await res.json();
        console.log(`Загружено ${partners.length} партнёров`);

        // Очищаем контейнер перед добавлением
        const partnersWrapper = document.getElementById('partners-wrapper');
        if (partnersWrapper) {
            partnersWrapper.innerHTML = '';
        }

        // Добавляем каждого партнёра
        for (const partner of partners) {
            addPartnerCard(
                partner.title,
                partner.img_path,
                partner.url
            );
        }

    } catch (error) {
        console.error('Ошибка при загрузке партнёров:', error);
        const partnersWrapper = document.getElementById('partners-wrapper');
        if (partnersWrapper) {
            partnersWrapper.innerHTML = '<p>Не удалось загрузить партнёров. Попробуйте позже.</p>';
        }
    }
}

// Загружаем партнёров при загрузке страницы
document.addEventListener('DOMContentLoaded', loadPartners);
