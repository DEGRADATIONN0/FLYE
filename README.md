# FLYE — Phone Intelligence & OSINT Tool

**FLYE** — консольный инструмент для быстрой OSINT-аналитики по номеру телефона и поиску аккаунтов по нику.

**Автор:** Huntonnoice

---

## Что делает
- Поиск по номеру телефона: Google Dorking, 2GIS (API), проверка публичных источников
- Детальный анализ номера с помощью `phonenumbers` (валидность, страна, регион, оператор, форматы)
- Приблизительные координаты города и ссылка на Google Maps
- Поиск ника: проверка популярных платформ (GitHub, Twitter, Instagram и др.) и Google Dorking
- Красивый цветной вывод и простые анимации (используются `pystyle` и `rich`)

## Файлы в репозитории
- `main.py` — основной скрипт
- `requirements.txt` — зависимости (pip install -r requirements.txt)
- `FLYE.exe` — (опционально) собранный исполняемый файл для Windows (если добавите в репозиторий/релиз)

## Установка и запуск (локально)
Рекомендуется создать виртуальное окружение, но можно установить зависимости глобально.

```bash
# на Windows / Linux
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## Запуск в Termux (Android)
Обычно проще запускать скрипт прямо в Termux:

```bash
pkg update
pkg install python-pip -y
python -m pip install --upgrade pip
pip install -r requirements.txt
# переместите main.py в Termux (scp/adb/git)
python main.py
```

> Примечание: PyInstaller в Termux/Android работает ненадёжно — лучше запускать как скрипт.

## Сборка .exe для Windows
Собирайте на Windows той же архитектуры, куда будете запускать; PyInstaller создаёт бинарник под текущую ОС.

```bash
pip install pyinstaller
pyinstaller --onefile --name "FLYE" main.py
# результат: dist/FLYE.exe
```

## Как выложить на GitHub (рекомендация)
Лучше не коммитить большие бинарные файлы в основную ветку; используйте GitHub Releases для exe.

Пример команд:

```bash
# инициализация репозитория (если ещё не создан)
git init
git add .
git commit -m "Initial commit: FLYE"
# создать репо на GitHub и связать (или используйте GitHub Desktop)
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Чтобы загрузить exe в релиз:
- Откройте страницу репозитория на GitHub → Releases → Draft a new release
- Прикрепите `dist/FLYE.exe` (или переименуйте в `FLYE-v1.0.exe`) и опубликуйте релиз

Или через `gh` CLI:

```bash
# предварительно установить GitHub CLI и выполнить gh auth login
gh release create v1.0 dist/FLYE.exe --title "FLYE v1.0" --notes "Windows build"
```

## Безопасность и законность
Используйте инструмент только для законных целей. Соблюдайте местные законы и правила по обработке персональных данных.

## Дополнительно
- Добавьте больше городов в словарь `CITY_COORDINATES` внутри `main.py` для улучшения геолокации
- По желанию можно добавить конфигурационный файл для API-ключей и дополнительных сервисов

---

Если хотите, могу автоматически создать репозиторий на GitHub и выполнить первый коммит/пуш (нужен доступ/gh cli), или подготовить `dist/FLYE.exe` и прикрепить инструкции по релизу.