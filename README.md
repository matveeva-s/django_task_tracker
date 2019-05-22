# django_task_tracker
Требуемое API реализовано в приложении "catalog".

При проектировнии БД никак не разделяла понятия "Описание задачи" и "Комментарий к задаче" - для них одна модель Description.
Использовала MySQL СУБД.

При запуске сервера открывается список всех задач с возможностями поиска и фильтрации по основным полям, внизу есть кнопка "Create task" для перехода к форме создания задачи. Т.к. задача прикреплена к проекту и автору, предварительно стоит создать пару юзеров и проект в админке (этого в ТЗ не было :) ). 
После создания задачи она отобразится в списке, по ней можно будет тыкнуть и узнать подробную информацию, включая статистику по дням по количеству комментариев и пользователей, их оставивших. Внизу будут кнопки для создания комментария(description), обновления статуса задачи и исполнителя, удаления задачи.

Тесты находятся в catalog/tests - отдельно для отображний, форм и моделей. Кроме этого проверено покрытие через coverege: соответвенно 58%, 100%, 100%.

Не чистила содержимое SECRET_KEY и прочую информацию типа паролей к локальной БД в settings.

ЗАПУСК:
Скачать репозиторий, активировать env, создать суперюзера для админки, выполнить "python3 manage.py runserver", создать в админке пару юзеров и проект, после чего все API будет доступно по корневому адресу (порт 8000). 

Если при проверке возникнут вопросы (они конечно возникнут), пишите в телеграмм @matveeva_sn или на почту matveeva.sn@phystech.edu. Извините, что так долго, я новичок в Джанго, потребовалось время.