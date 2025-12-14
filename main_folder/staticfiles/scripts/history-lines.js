function addLineCard(title, description, imgPath, lineUrl) {
    // Находим контейнер для исторических линий
    const linesWrapper = document.querySelector('.lines-wrapper');
    if (!linesWrapper) {
        console.error('Контейнер .lines-wrapper не найден!');
        return;
    }

    // Создаём основной элемент карточки
    const lineCard = document.createElement('div');
    lineCard.className = 'line-card';

    // Изображение
    const cardImage = document.createElement('div');
    cardImage.className = 'card-image';

    const img = document.createElement('img');
    img.src = imgPath || '#';
    img.alt = title || 'Историческая линия';

    cardImage.appendChild(img);

    // Контент карточки
    const cardContent = document.createElement('div');
    cardContent.className = 'card-content';

    // Верхняя часть карточки
    const cardContentTop = document.createElement('div');
    cardContentTop.className = 'card-content-top';

    // Ссылка на линию
    const lineLink = document.createElement('a');
    lineLink.href = lineUrl || '#';
    lineLink.className = 'line-link';

    const titleEl = document.createElement('h3');
    titleEl.textContent = title || 'Без названия';

    lineLink.appendChild(titleEl);

    // Ссылка "Смотреть"
    const viewLink = document.createElement('a');
    viewLink.href = lineUrl || '#';
    viewLink.className = 'line-view-link';

    const viewIcon = document.createElement('span');
    viewIcon.className = 'card-view-icon';
    viewIcon.textContent = '▶▶';

    const viewText = document.createElement('span');
    viewText.className = 'card-view-text';
    viewText.textContent = 'Смотреть';

    viewLink.appendChild(viewIcon);
    viewLink.appendChild(viewText);

    // Собираем верхнюю часть
    cardContentTop.appendChild(lineLink);
    cardContentTop.appendChild(viewLink);

    // Описание
    const descriptionEl = document.createElement('p');
    descriptionEl.className = 'card-description';
    descriptionEl.textContent = description || 'Описание отсутствует';

    // Собираем контент
    cardContent.appendChild(cardContentTop);
    cardContent.appendChild(descriptionEl);

    // Собираем всю карточку
    lineCard.appendChild(cardImage);
    lineCard.appendChild(cardContent);

    // Добавляем в контейнер
    linesWrapper.appendChild(lineCard);
}

async function loadHistoryLines() {
    try {
        const res = await fetch('/api/history-lines/');
        if (!res.ok) {
            throw new Error(`Ошибка загрузки: ${res.status}`);
        }

        const lines = await res.json(); // Ожидается массив объектов с полями: title, desc, img_path, url

        // Очищаем контейнер перед загрузкой
        const linesWrapper = document.querySelector('.lines-wrapper');
        if (linesWrapper) {
            linesWrapper.innerHTML = '';
        }

        // Добавляем каждую линию
        lines.forEach(line => {
            addLineCard(
                line.title,
                line.desc,
                line.img_path,
                line.url
            );
        });

        console.log(`Загружено ${lines.length} исторических линий`);
    } catch (error) {
        console.error('Ошибка при загрузке исторических линий:', error);
        const linesWrapper = document.querySelector('.lines-wrapper');
        if (linesWrapper) {
            linesWrapper.innerHTML = '<p>Не удалось загрузить исторические линии. Попробуйте позже.</p>';
        }
    }
}

// Загружаем линии при загрузке страницы
document.addEventListener('DOMContentLoaded', loadHistoryLines);