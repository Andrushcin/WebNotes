# WebNotes
WebNotes - веб-приложение для создания заметок. С помощью данного приложения вы можете записывать любую информацию и получать к ней доступ с любого устройства. 

Далее рассмотрим развёртывание приложения локально на вашем компьютере на примере ОС Windows 10
1) В любой рабочей папке откройте терминал и клонируйте репозиторий командой 
  git clone https://github.com/Andrushcin/WebNotes 
2) Перейдите в созданную папку проекта командой 
  cd WebNotes
3) Создайте виртуальное окружение командой 
  python -m venv venv
4) Перейдите в папку Scripts виртуального окружения с помощью команды 
  cd venv/Scripts/
5) Активируйте виртуальное окружение, запустив:
  activate.bat
6) Вернитесь в папку проекта с помощью команды
  cd ../../
7) Установите зависимости из файла requirements.txt с помощью команды 
  pip install -r requirements.txt
8) Перейдите в папку webnotes:
  cd webnotes
9) Выполните миграции командой
  python manage.py migrate
10) Зарегистрируйте суперпользователя (администратора) командой
  python manage.py createsuperuser
11) Установите переменную среды с именем 'SECRET_KEY'. Значением может быть произвольный набор символов, известный только вам.
  Альтернативный, но нежелательный вариант установки значения секретного ключа:
  В файле settings.py замените настройку SECRET_KEY = os.environ.get('SECRET_KEY') на SECRET_KEY = "<your-secret-key>"
12) Запустите локальный сервер командой 
  python manage.py runserver
13) Перейдите в браузере по адресу http://127.0.0.1:8000/
  Вы должны попасть на главную страницу сайта.
