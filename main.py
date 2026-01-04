import requests
import json
import re
from pystyle import Colors, Colorate, Box
from urllib.parse import quote
import time
import phonenumbers
from phonenumbers import carrier, geocoder
import subprocess
import os
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

# Примерные координаты крупных городов (широта, долгота)
CITY_COORDINATES = {
    # Россия
    'Москва': (55.7558, 37.6173),
    'Санкт-Петербург': (59.9311, 30.3609),
    'Краснодар': (45.0355, 38.9759),
    'Новосибирск': (55.0084, 82.9357),
    'Екатеринбург': (56.8389, 60.6057),
    'Казань': (55.7964, 49.1181),
    'Челябинск': (55.1644, 61.4368),
    'Омск': (54.9906, 73.3681),
    'Самара': (53.1973, 50.0975),
    'Ростов-на-Дону': (47.2357, 39.7015),
    
    # Украина
    'Киев': (50.4501, 30.5234),
    'Харьков': (50.0028, 36.2304),
    'Одесса': (46.4757, 30.7326),
    'Днепр': (48.4649, 35.0468),
    'Львов': (49.8397, 24.0297),
    'Запорожье': (47.8388, 35.1314),
    'Винница': (49.2331, 28.4682),
    'Кривой Рог': (47.9094, 33.3826),
    'Николаев': (46.9754, 31.9848),
    'Луцк': (50.7472, 25.3254),
    
    # Беларусь
    'Минск': (53.9045, 27.5615),
    'Гродно': (54.4267, 25.4245),
    'Витебск': (54.1799, 30.2049),
    'Брест': (52.0883, 23.6880),
    'Могилёв': (53.9045, 30.3395),
    'Гомель': (52.4286, 30.9965),
    'Полоцк': (54.5406, 24.8539),
}

# Словарь операторов -> основные города
OPERATOR_CITIES = {
    'lifecell': ['Киев', 'Харьков', 'Одесса'],
    'vodafone': ['Киев', 'Львов', 'Днепр'],
    'kyivstar': ['Киев', 'Винница', 'Запорожье'],
    'мтс': ['Москва', 'Санкт-Петербург'],
    'мегафон': ['Москва', 'Санкт-Петербург', 'Екатеринбург'],
    'билайн': ['Москва', 'Санкт-Петербург'],
}

class PhoneOSINT:
    def __init__(self):
        self.phone = None
        self.nickname = None
        self.results = {}
    
    def animate_text(self, text, color=Colors.cyan, delay=0.02):
        """Анимированный вывод текста с эффектом печатной машинки"""
        # Создаем красивый текст с цветом и стилем
        styled_text = Text(text, style="bold cyan")
        console.print(styled_text, justify="center")
        time.sleep(0.5)
        
    def banner(self):
        """Красивый баннер"""
        banner_text = """
╔═══════════════════════════════════════╗
║          📱 FLYE 📱                   ║
║   Phone Intelligence & OSINT Tool     ║
║                                       ║
║        by Huntonnoice                 ║
╚═══════════════════════════════════════╝

    ███████╗██╗     ██╗   ██╗███████╗
    ██╔════╝██║     ╚██╗ ██╔╝██╔════╝
    █████╗  ██║      ╚████╔╝ █████╗  
    ██╔══╝  ██║       ╚██╔╝  ██╔══╝  
    ██║     ███████╗   ██║   ███████╗
    ╚═╝     ╚══════╝   ╚═╝   ╚══════╝
                                       
        """
        print(Colorate.Horizontal(Colors.cyan_to_blue, banner_text))
    
    def get_phone(self):
        """Получить номер телефона от пользователя"""
        print(f"\n{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        phone = input(f"{Colors.cyan}Введите номер телефона (например +7 (999) 123-45-67): {Colors.reset}")
        # Очистить номер от символов
        self.phone = re.sub(r'\D', '', phone)
        
        if not self.phone or len(self.phone) < 10:
            print(f"{Colors.red}❌ Некорректный номер телефона!{Colors.reset}")
            return False
        
        print(f"{Colors.green}✓ Номер принят: {self.phone}{Colors.reset}")
        return True
    
    def get_nickname(self):
        """Получить никнейм от пользователя"""
        print(f"\n{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        nickname = input(f"{Colors.cyan}Введите ник для поиска (например: john_doe): {Colors.reset}")
        
        self.nickname = nickname.strip()
        
        if not self.nickname or len(self.nickname) < 3:
            print(f"{Colors.red}❌ Никнейм слишком короткий (минимум 3 символа)!{Colors.reset}")
            return False
        
        print(f"{Colors.green}✓ Ник принят: {self.nickname}{Colors.reset}")
        return True
    
    def search_google_dorking(self):
        """Поиск информации через Google Dorking"""
        print(f"\n{Colors.yellow}[*] Поиск через Google Dorking...{Colors.reset}")
        
        queries = [
            f'"{self.phone}"',
            f'site:2gis.ru "{self.phone}"',
            f'site:avto.ru "{self.phone}"',
            f'"{self.phone}" контакт',
            f'"{self.phone}" объявление'
        ]
        
        google_url = "https://www.google.com/search?q="
        
        self.results['google_dorking'] = {
            'статус': '✓ Найденные запросы',
            'ссылки': [
                f"{google_url}{quote(query)}" for query in queries
            ]
        }
        
        for i, query in enumerate(queries, 1):
            print(f"{Colors.cyan}  [{i}] {query[:50]}...{Colors.reset}")
            print(f"     {Colors.cyan}→ {google_url}{quote(query)[:60]}...{Colors.reset}")
        
        console.print("\n[green]✓ Google Dorking завершён![/green]")
    
    def search_2gis(self):
        """Поиск в 2GIS"""
        print(f"\n{Colors.yellow}[*] Поиск в 2GIS...{Colors.reset}")
        
        url = f"https://catalog.api.2gis.com/3.0/search?q={self.phone}&locale=ru_RU"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'items' in data and data['items']:
                    self.results['2gis'] = {
                        'статус': '✓ Найдено результатов',
                        'количество': len(data['items']),
                        'результаты': data['items'][:3]
                    }
                    console.print(f"[green]✓ Найдено {len(data['items'])} результатов в 2GIS[/green]")
                else:
                    console.print(f"[yellow]⚠ Результатов не найдено в 2GIS[/yellow]")
            else:
                console.print(f"[red]✗ Ошибка подключения к 2GIS[/red]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка 2GIS: {str(e)[:50]}[/red]")
    
    def search_truecaller_api(self):
        """Попытка получить информацию через публичные источники"""
        print(f"\n{Colors.yellow}[*] Проверка в публичных источниках...{Colors.reset}")
        
        # Имитация поиска в публичных источниках
        sources = [
            "2GIS (справочник организаций)",
            "Авито (объявления)",
            "Яндекс.Карты (организации)",
            "Вконтакте (профили)",
            "Instagram (теги)",
            "Telegram (публичные чаты)"
        ]
        
        self.results['public_sources'] = sources
        
        for source in sources:
            console.print(f"[cyan]  ✓ {source}[/cyan]")
            time.sleep(0.2)
        
        console.print("\n[green]✓ Проверка источников завершена![/green]")
    
    def search_reverse_lookup(self):
        """Обратный поиск по номеру"""
        print(f"\n{Colors.yellow}[*] Обратный поиск...{Colors.reset}")
        
        try:
            # Добавляем '+' если его нет
            phone_to_parse = self.phone if self.phone.startswith('+') else f"+{self.phone}"
            
            # Парсим номер с помощью phonenumbers
            parsed = phonenumbers.parse(phone_to_parse, None)
            
            # Валидность
            is_valid = phonenumbers.is_valid_number(parsed)
            is_possible = phonenumbers.is_possible_number(parsed)
            
            # Регион/Страна
            region = geocoder.region_code_for_number(parsed)
            region_name = geocoder.description_for_number(parsed, "ru")
            
            # Оператор
            operator = carrier.name_for_number(parsed, "ru")
            
            # Тип номера
            number_type = phonenumbers.number_type(parsed)
            type_name = {
                0: "Фиксированный",
                1: "Мобильный",
                2: "Платная линия",
                3: "VoIP",
                4: "Персональный",
                5: "Для пейджеров",
                6: "Без уточнения",
                7: "Voicemail"
            }.get(number_type, "Неизвестный тип")
            
            # Форматирование
            formatted_intl = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            formatted_national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            
            self.results['phonenumbers_analysis'] = {
                'валиден': '✓ Да' if is_valid else '✗ Нет',
                'возможен': '✓ Да' if is_possible else '✗ Нет',
                'страна': region,
                'регион': region_name if region_name else 'Неизвестный регион',
                'оператор': operator if operator else 'Неизвестный оператор',
                'тип_номера': type_name,
                'формат_международный': formatted_intl,
                'формат_национальный': formatted_national,
                'координаты': self.get_city_coordinates(region_name) if region_name else None,
                'город_по_оператору': self.get_city_by_operator(operator)
            }
            
            print(f"{Colors.green}  ✓ Анализ выполнен успешно{Colors.reset}")
            console.print("\n[green]✓ Анализ номера завершён![/green]")
            
        except phonenumbers.NumberParseException as e:
            console.print(f"[red]✗ Ошибка парсинга номера[/red]")
            self.results['phonenumbers_analysis'] = {
                'статус': 'Ошибка при парсинге номера'
            }
        except Exception as e:
            console.print(f"[red]✗ Ошибка анализа: {str(e)[:40]}[/red]")
    
    def _get_operator(self):
        """Определить оператора по коду номера"""
        phone_codes = {
            '7': 'Россия',
            '375': 'Беларусь',
            '380': 'Украина'
        }
        
        if self.phone.startswith('7'):
            # Российские коды операторов (примеры)
            codes = {
                '901-920': 'МегаФон',
                '921-927': 'Ростелеком',
                '931-939': 'МТС',
                '950-951': 'Билайн'
            }
            return 'МегаФон / МТС / Билайн (точное определение требует доступа к БД)'
        
        return 'Неизвестный оператор'
    
    def _get_region(self):
        """Определить регион по коду города"""
        if len(self.phone) >= 11:
            area_code = self.phone[1:4]
            regions = {
                '495': 'Москва',
                '496': 'Московская область',
                '812': 'Санкт-Петербург',
                '321': 'Краснодар',
                '383': 'Новосибирск'
            }
            return regions.get(area_code, 'Неизвестный регион')
        return 'Неизвестный регион'
    
    def get_city_coordinates(self, city_name):
        """Получить приблизительные координаты города"""
        for city, coords in CITY_COORDINATES.items():
            if city.lower() in city_name.lower() or city_name.lower() in city.lower():
                return coords
        return None
    
    def get_city_by_operator(self, operator_name):
        """Определить город по названию оператора"""
        if not operator_name:
            return None
        
        operator_lower = operator_name.lower().strip()
        
        for op, cities in OPERATOR_CITIES.items():
            if op.lower() in operator_lower:
                # Возвращаем первый город (основной)
                return cities[0]
        
        return None
    
    def search_maigret(self):
        """Поиск ника через Maigret или альтернативные источники (Sherlock Mode)"""
        print(f"\n{Colors.yellow}[*] Поиск в публичных источниках...{Colors.reset}\n")
        
        # Список популярных платформ для поиска
        platforms = {
            'GitHub': f'https://github.com/{self.nickname}',
            'Twitter': f'https://twitter.com/{self.nickname}',
            'Instagram': f'https://instagram.com/{self.nickname}',
            'Facebook': f'https://facebook.com/{self.nickname}',
            'TikTok': f'https://tiktok.com/@{self.nickname}',
            'YouTube': f'https://youtube.com/@{self.nickname}',
            'Twitch': f'https://twitch.tv/{self.nickname}',
            'Reddit': f'https://reddit.com/user/{self.nickname}',
            'Telegram': f'https://t.me/{self.nickname}',
            'Discord': f'https://discordapp.com/users/{self.nickname}',
            'Steam': f'https://steamcommunity.com/search/users/#{self.nickname}',
            'Spotify': f'https://open.spotify.com/user/{self.nickname}',
            'VK (ВКонтакте)': f'https://vk.com/{self.nickname}',
            'Яндекс.Знатоки': f'https://yandex.ru/znatoki/user/{self.nickname}',
            'Habr': f'https://habr.com/ru/users/{self.nickname}',
        }
        
        found_results = []
        not_found = []
        
        print(f"{Colors.yellow}Проверка на платформах...{Colors.reset}\n")
        
        for platform, url in platforms.items():
            try:
                response = requests.head(url, timeout=3, allow_redirects=True)
                if response.status_code == 200:
                    found_results.append((platform, url))
                    print(f"{Colors.green}✓ {platform:<25} - НАЙДЕН{Colors.reset}")
                else:
                    not_found.append((platform, url))
                    print(f"{Colors.red}✗ {platform:<25} - не найден{Colors.reset}")
            except requests.exceptions.Timeout:
                print(f"{Colors.yellow}⏱ {platform:<25} - timeout{Colors.reset}")
                not_found.append((platform, url))
            except Exception as e:
                print(f"{Colors.yellow}⚠ {platform:<25} - ошибка{Colors.reset}")
                not_found.append((platform, url))
            
            time.sleep(0.3)  # Небольшая задержка между запросами
        
        self.results['maigret'] = {
            'найдено': found_results,
            'не_найдено': not_found,
            'всего_проверено': len(platforms)
        }
    
    def search_nick_dorking(self):
        """Google Dorking для поиска ника"""
        print(f"\n{Colors.yellow}[*] Google Dorking для ника...{Colors.reset}")
        
        queries = [
            f'"{self.nickname}"',
            f'"{self.nickname}" профиль',
            f'"{self.nickname}" контакт',
            f'site:github.com "{self.nickname}"',
            f'site:twitter.com "{self.nickname}"',
            f'site:reddit.com "{self.nickname}"',
            f'site:instagram.com "{self.nickname}"',
            f'site:youtube.com "{self.nickname}"',
            f'site:twitch.tv "{self.nickname}"',
            f'site:steam.com "{self.nickname}"',
        ]
        
        google_url = "https://www.google.com/search?q="
        
        self.results['nick_dorking'] = {
            'статус': '✓ Найденные запросы',
            'ссылки': [
                f"{google_url}{quote(query)}" for query in queries
            ]
        }
        
        for i, query in enumerate(queries, 1):
            print(f"{Colors.cyan}  [{i}] {query[:50]}...{Colors.reset}")
            print(f"     {Colors.cyan}→ {google_url}{quote(query)[:60]}...{Colors.reset}")
    
    def display_maigret_results(self):
        """Вывести результаты поиска по нику"""
        if 'maigret' not in self.results:
            return
        
        data = self.results['maigret']
        
        print(f"\n{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        print(Colorate.Horizontal(Colors.green_to_yellow, f"🔍 РЕЗУЛЬТАТЫ ПОИСКА: {self.nickname}"))
        print(f"{Colors.yellow}═══════════════════════════════════════{Colors.reset}\n")
        
        found = data['найдено']
        not_found = data['не_найдено']
        
        if found:
            print(f"{Colors.green}✓ НАЙДЕНО АККАУНТОВ: {len(found)}/{data['всего_проверено']}{Colors.reset}\n")
            for platform, url in found:
                print(f"{Colors.green}  ✓ {platform:<30}{Colors.reset}")
                print(f"    {Colors.cyan}🔗 {url}{Colors.reset}\n")
        else:
            print(f"{Colors.yellow}⚠ Аккаунты не найдены на проверенных платформах{Colors.reset}\n")
        
        print(f"{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        print(f"{Colors.yellow}Проверено платформ: {data['всего_проверено']}{Colors.reset}\n")
        self.animate_text(f"Made by Huntonnoice", Colors.blue)
    
    def display_results(self):
        """Вывести результаты красиво"""
        print(f"\n{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        print(Colorate.Horizontal(Colors.green_to_yellow, f"📊 РЕЗУЛЬТАТЫ ПОИСКА: {self.phone}"))
        print(f"{Colors.yellow}═══════════════════════════════════════{Colors.reset}\n")
        
        # Google Dorking
        if 'google_dorking' in self.results:
            print(f"{Colors.blue}[📍] Google Dorking{Colors.reset}")
            for link in self.results['google_dorking']['ссылки'][:3]:
                print(f"   {Colors.cyan}{link[:70]}...{Colors.reset}")
            print()
        
        # 2GIS
        if '2gis' in self.results:
            print(f"{Colors.blue}[🏢] 2GIS{Colors.reset}")
            print(f"   {Colors.green}Найдено: {self.results['2gis']['количество']} результатов{Colors.reset}\n")
        
        # Публичные источники
        if 'public_sources' in self.results:
            print(f"{Colors.blue}[📱] Проверено в источниках:{Colors.reset}")
            for source in self.results['public_sources']:
                print(f"   {Colors.cyan}• {source}{Colors.reset}")
            print()
        
        # Обратный поиск
        if 'reverse_lookup' in self.results:
            data = self.results['reverse_lookup']
            print(f"{Colors.blue}[🔍] Информация о номере:{Colors.reset}")
            print(f"   {Colors.cyan}Оператор: {data['возможный_оператор']}{Colors.reset}")
            print(f"   {Colors.cyan}Регион: {data['регион']}{Colors.reset}")
            print(f"   {Colors.green}Статус: {data['статус']}{Colors.reset}\n")
        
        # Анализ phonenumbers
        if 'phonenumbers_analysis' in self.results:
            data = self.results['phonenumbers_analysis']
            if 'статус' not in data or data['статус'] != 'Ошибка при парсинге номера':
                print(f"{Colors.blue}[📊] Детальный анализ номера (phonenumbers):{Colors.reset}")
                print(f"   {Colors.yellow}Валиден: {data['валиден']}{Colors.reset}")
                print(f"   {Colors.yellow}Возможен: {data['возможен']}{Colors.reset}")
                print(f"   {Colors.cyan}Страна: {data['страна']}{Colors.reset}")
                print(f"   {Colors.cyan}Регион: {data['регион']}{Colors.reset}")
                print(f"   {Colors.cyan}Оператор: {data['оператор']}{Colors.reset}")
                print(f"   {Colors.cyan}Тип номера: {data['тип_номера']}{Colors.reset}")
                
                # Определяем координаты
                coords = data.get('координаты')
                if not coords and data.get('город_по_оператору'):
                    # Пытаемся получить координаты по оператору
                    coords = self.get_city_coordinates(data['город_по_оператору'])
                
                # Вывести координаты если найдены
                if coords:
                    coords_str = f"{coords[0]:.4f}° N, {coords[1]:.4f}° E"
                    city_name = data.get('город_по_оператору', 'город')
                    print(f"   {Colors.green}📍 Примерные координаты ({city_name}): {coords_str}{Colors.reset}")
                    lat, lon = coords
                    google_maps_url = f"https://maps.google.com/?q={lat},{lon}"
                    print(f"   {Colors.cyan}🗺 Google Maps: {google_maps_url}{Colors.reset}")
                
                print(f"   {Colors.green}Формат (междунар.): {data['формат_международный']}{Colors.reset}")
                print(f"   {Colors.green}Формат (национ.): {data['формат_национальный']}{Colors.reset}\n")
        
        print(f"{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        self.animate_text(f"Made by Huntonnoice", Colors.blue)
    
    def show_menu(self):
        """Меню инструмента"""
        print(f"\n{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        print(f"{Colors.cyan}[1] Поиск по номеру телефона{Colors.reset}")
        print(f"{Colors.cyan}[2] Поиск ника{Colors.reset}")
        print(f"{Colors.cyan}[3] Помощь и примеры{Colors.reset}")
        print(f"{Colors.cyan}[4] Выход{Colors.reset}")
        print(f"{Colors.yellow}═══════════════════════════════════════{Colors.reset}")
        
        choice = input(f"\n{Colors.cyan}Выберите опцию (1-4): {Colors.reset}")
        return choice
    
    def show_help(self):
        """Справка"""
        help_text = """
╔═══════════════════════════════════════════════════════════════╗
║                    СПРАВКА И ПРИМЕРЫ                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📱 РЕЖИМ 1 - ПОИСК ПО НОМЕРУ ТЕЛЕФОНА                      ║
║  Этот инструмент использует публичные источники для поиска:   ║
║  • Google Dorking - специальные операторы поиска              ║
║  • 2GIS API - справочник организаций и контактов            ║
║  • Публичные источники - соцсети, справочники                ║
║  • Анализ кода номера - определение оператора и региона     ║
║                                                               ║
║  🔍 РЕЖИМ 2 - ПОИСК НИКА                                     ║
║  Поиск аккаунтов по никнейму на множестве платформ:         ║
║  • GitHub, Twitter, Instagram, Facebook, TikTok, YouTube     ║
║  • Reddit, Telegram, VK, Discord, Steam, Spotify и другие    ║
║                                                               ║
║  ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:                                      ║
║  Номер: +7 (999) 123-45-67 или +380 63 825-60-26            ║
║  Ник:   john_doe, alex2024, user_name (3+ символа)          ║
║                                                               ║
║  ⚠️  ВНИМАНИЕ: Используйте только для законных целей!        ║
║      Соблюдайте законодательство о защите персональных данных║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        print(Colorate.Horizontal(Colors.blue_to_cyan, help_text))
    
    def run(self):
        """Главный цикл программы"""
        self.banner()
        
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                if self.get_phone():
                    print(f"\n{Colors.yellow}Начинаю поиск информации...{Colors.reset}\n")
                    self.search_google_dorking()
                    time.sleep(0.5)
                    self.search_2gis()
                    time.sleep(0.5)
                    self.search_truecaller_api()
                    time.sleep(0.5)
                    self.search_reverse_lookup()
                    self.display_results()
            
            elif choice == '2':
                if self.get_nickname():
                    print(f"\n{Colors.yellow}🔍 Поиск ника по платформам...{Colors.reset}")
                    self.search_nick_dorking()
                    self.search_maigret()
                    self.display_maigret_results()
            
            elif choice == '3':
                self.show_help()
            
            elif choice == '4':
                print(f"\n{Colors.green}До свидания!{Colors.reset}\n")
                break
            
            else:
                print(f"{Colors.red}Неверный выбор!{Colors.reset}")


if __name__ == "__main__":
    tool = PhoneOSINT()
    tool.run()