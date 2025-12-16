function addTeamCard(member) {
  // Находим контейнер для карточек команды
  const teamGrid = document.querySelector('.team-grid');
  if (!teamGrid) {
    console.error('Контейнер .team-grid не найден!');
    return;
  }

  // Создаем элемент карточки с классом team-card
  const teamCard = document.createElement('div');
  teamCard.className = 'team-card';

  // Создаем изображение с классом team-photo
  const img = document.createElement('img');
  img.className = 'team-photo';
  img.src = member.img_path || '';
  img.alt = member.title || 'Фотография участника';

  // Создаем заголовок h3
  const titleEl = document.createElement('h3');
  titleEl.textContent = member.title || 'Без имени';

  // Создаем параграф для статуса с классом position
  const statusEl = document.createElement('p');
  statusEl.className = 'position';
  statusEl.textContent = member.status || '';

  // Создаем параграф для роли с классом role
  const roleEl = document.createElement('p');
  roleEl.className = 'role';
  roleEl.textContent = member.role || '';

  // Создаем ссылку на соцсеть с классом vk-link
  const link = document.createElement('a');
  link.href = member.url || '#';
  link.className = 'vk-link';
  link.target = '_blank';

  // Создаем иконку VK с классом vk-icon
  // Примечание: путь к иконке VK нужно будет указать валидный
  const vkIcon = document.createElement('img');
  vkIcon.className = 'vk-icon';
  vkIcon.src = 'static/img/team-page/vk.svg'; // Измените путь при необходимости
  vkIcon.alt = 'VK';

  // Собираем структуру
  link.appendChild(vkIcon);
  
  teamCard.appendChild(img);
  teamCard.appendChild(titleEl);
  if (member.status) teamCard.appendChild(statusEl);
  if (member.role) teamCard.appendChild(roleEl);
  if (member.url) teamCard.appendChild(link);
  
  teamGrid.appendChild(teamCard);
}

async function loadTeam() {
  try {
    // Загружаем данные о команде
    // Измените URL на актуальный для вашего проекта
    const res = await fetch('team_page/get'); 
    if (!res.ok) {
      throw new Error(`Ошибка загрузки: ${res.status}`);
    }

    const members = await res.json();
    console.log(`Загружено ${members.length} участников команды`);

    // Находим контейнер для карточек
    const teamGrid = document.querySelector('.team-grid');
    if (teamGrid) {
      // Очищаем контейнер перед добавлением новых карточек (опционально)
      // teamGrid.innerHTML = '';
    }

    // Добавляем каждую карточку участника
    for (let i = 0; i < members.length; i++) {
      addTeamCard(members[i]);
    }

  } catch (error) {
    console.error('Ошибка при загрузке участников команды:', error);
    // Можно показать сообщение об ошибке пользователю
    const teamGrid = document.querySelector('.team-grid');
    if (teamGrid) {
      teamGrid.innerHTML = '<p>Не удалось загрузить информацию об участниках команды. Попробуйте позже.</p>';
    }
  }
}

// Загружаем участников команды при загрузке страницы
document.addEventListener('DOMContentLoaded', loadTeam);