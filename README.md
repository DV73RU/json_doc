# json_doc
 blockType:
          title: Тип блока
          type: integer
          description: |
            - 1 — **Текст**, обязательные поля: `text`, не обязательные: ``
            - 2 — **Цитата**, обязательные поля: `text`, `author`, не обязательные: `regalia`, `image`
            - 3 — **Видео**, обязательные поля: `link`, `duration`, `image`, не обязательные: `text`, `title`
            - 4 — **Аудио**, обязательные поля: `link`, `duration`, `title`, не обязательные: `text`
            - 5 — **Карусель изображений**, обязательные поля: `carousel`, не обязательные: ``
            - 6 — **Книга**, обязательные поля: `links`, не обязательные: ``
            - 7 — **Легенда**, обязательные поля: `company`, не обязательные: `geo`, `team`, `perYear`, `year`, `perMonth`, `countYear`, `city`
            - 8 — **Мнение**, обязательные поля: `text`, не обязательные: `regalia`, `image`, `title`, `author`
            - 9 — **Описание мероприятия**, обязательные поля: `address`, `date`, `cost`, `link`, не обязательные: ``
            - 10 — **Заголовок**, обязательные поля: `text`, не обязательные: ``
            - 11 — **Список**, обязательные поля: `elemList`, не обязательные: ``
            - 12 — **Промо-блок**, обязательные поля: `link`, `image`, не обязательные: `title`
            - 13 — **Карточка**, обязательные поля: `title`, `text`, не обязательные: `supportText`
            - 14 — **Тест**, обязательные поля: `link`, не обязательные: ``
            - 15 — **Опрос**, обязательные поля: `poll`, не обязательные: ``
            - 16 — **Список элементов кейса**, обязательные поля: `elemCaseList`, не обязательные: ``
            - 17 — **Баннер**, обязательные поля: `banner`, не обязательные: ``
            - 18 — **фрейм РКО**, обязательные поля: ``, не обязательные: ``
            - 19 — **Квиз (скрыт для мп)**, обязательные поля: `quiz`, не обязательные: ``
            - 20 — **Пушбук (скрыт для мп)** обязательные поля: `event`, не обязательные: ``
            - 21 — **Праздничная метка (скрыт для мп)** обязательные поля: `holidayMark`, не обязательные:
