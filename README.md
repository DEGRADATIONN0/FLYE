<img width="885" height="779" alt="изображение" src="https://github.com/user-attachments/assets/78f7b5f7-42b2-4b3c-b066-793bed7a429c" />


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
- `FLYE.exe` — (опционально) собранный исполняемый файл для Windows

## Установка и запуск (локально)
Рекомендуется создать виртуальное окружение, но можно установить зависимости глобально.

```bash
# на Windows / Linux
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```
либо использовать собраный exe файл для windows 


## Запуск в Termux (Android)
Обычно проще запускать скрипт прямо в Termux:

```bash
pkg update
pkg install python-pip git -y
git clone https://github.com/DEGRADATIONN0/FLYE.git
cd FLYE
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


## Безопасность и законность
Используйте инструмент только для законных целей. Соблюдайте местные законы и правила по обработке персональных данных.

## Дополнительно
- Добавьте больше городов в словарь `CITY_COORDINATES` внутри `main.py` для улучшения геолокации
- По желанию можно добавить конфигурационный файл для API-ключей и дополнительных сервисов

---

have fun

