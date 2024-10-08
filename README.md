# GP_DocumentProcessing

        Описание

"Web-приложение: `Сервис обработки загружаемых документов` 
Реализована бэкенд-часть SPA веб-приложения с созданием Docker-контейнеров.

- Авторизированный пользователь может загружать документы через API 
(при загрузке документов предусмотрена валидация, в том числе по объему загружаемого файла, 
который не может быть более 50 Гб).
- При загрузке документа администратор платформы получает уведомление по электронной почте 
со ссылкой на загруженные документы
- Администратор может просматривать, подтверждать или отклонять загруженные документы через Django admin,
но не имеет права изменять загруженный файл и данные от пользователя.
- После подтверждения или отклонения документа пользователю, загрузившему документ, 
направляется уведомление по электронной почте с указанием статуса документа (принято/отклонено).
- Пользователи могут просматривать, изменять только свои данные, а также 
могут просматривать только свои загруженные документы, не имеют прав их изменять.

Статус разработки: учебная, покрытие тестами 90% (в корне проекта файл test_data.txt)

        Использование

1. Для работы скаченного проекта создайте в корне проекта файл .env
Файл .env требуется заполнить по аналогии с образцом .env.sample

2. Для управления зависимостями используется `Poetry`

3. Для обработки уведомлений необходимо используется система очередей Celery

4. Чтобы развернуть проект на сервере/машине выполните команду:
    `docker-compose up --build`

5. После завершения установки, запустите следующие команды 
для создания миграций и суперпользователя:
    `docker-compose exec app python3 manage.py migrate`
    `docker-compose exec app python3 manage.py csu` 


Дипломный проект по направлению: "Профессия Python-разработчик", 
тема: "Сервис обработки загружаемых документов"
документация http://0.0.0.0:8000/redoc/ либо http://0.0.0.0:8000/swagger/
