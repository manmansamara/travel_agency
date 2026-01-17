-- Создаем базу данных
DROP DATABASE IF EXISTS agency;
CREATE DATABASE agency;
USE agency;

-- Таблица туров (tours)
CREATE TABLE tours (
    tour_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(1000) NOT NULL,
    duration VARCHAR(1000) NOT NULL,
    from_where VARCHAR(1000) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image_place VARCHAR(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Таблица заказов (orders)
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    who VARCHAR(200) NOT NULL,
    description VARCHAR(200) NOT NULL,
    datetime DATETIME(6) NOT NULL,
    tour_number INT,
    FOREIGN KEY (tour_number) REFERENCES tours(tour_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Добавляем первый тур (из примера)
INSERT INTO tours (name, duration, from_where, price, image_place) VALUES (
    'На море',
    '7 дней',
    'Самара, 25.01.2026 в 10:00 - Сочи 26.01.2026 в 9:00',
    150000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image1.jpg'
);

-- Добавляем 9 придуманных туров
INSERT INTO tours (name, duration, from_where, price, image_place) VALUES
-- Тур 2: Горный
(
    'Альпийские каникулы',
    '5 дней',
    'Москва, 15.02.2026 в 08:00 - Инсбрук (Австрия) 15.02.2026 в 12:00',
    210000.50,
    'https://github.com/manmansamara/travel_agency/blob/main/image2.jpg'
),
-- Тур 3: Исторический
(
    'Тур по Золотому кольцу',
    '4 дня',
    'Нижний Новгород, 10.03.2026 в 07:30 - Владимир 10.03.2026 в 11:00',
    85000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image3.jpg'
),
-- Тур 4: Экзотический
(
    'Отдых в Тайланде',
    '10 дней',
    'Санкт-Петербург, 05.04.2026 в 23:00 - Пхукет 06.04.2026 в 14:00',
    320000.75,
    'https://github.com/manmansamara/travel_agency/blob/main/image4.jpg'
),
-- Тур 5: Городской
(
    'Уикенд в Праге',
    '3 дня',
    'Казань, 20.05.2026 в 06:45 - Прага 20.05.2026 в 09:30',
    120000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image5.jpg'
),
-- Тур 6: Приключенческий
(
    'Сафари в Кении',
    '8 дней',
    'Москва, 12.06.2026 в 21:15 - Найроби 13.06.2026 в 06:00',
    450000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image6.jpg'
),
-- Тур 7: Зимний
(
    'Новогодние каникулы в Финляндии',
    '6 дней',
    'Санкт-Петербург, 29.12.2026 в 10:00 - Рованиеми 29.12.2026 в 13:30',
    280000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image7.jpg'
),
-- Тур 8: Пляжный
(
    'Мальдивская сказка',
    '7 дней',
    'Москва, 01.07.2026 в 16:00 - Мале 02.07.2026 в 08:00',
    550000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image8.jpg'
),
-- Тур 9: Кулинарный
(
    'Гастрономический тур по Италии',
    '5 дней',
    'Ростов-на-Дону, 15.09.2026 в 05:30 - Рим 15.09.2026 в 10:00',
    195000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image9.jpg'
),
-- Тур 10: Лечебный
(
    'Оздоровление в Карловых Варах',
    '7 дней',
    'Екатеринбург, 10.10.2026 в 08:00 - Карловы Вары 10.10.2026 в 12:30',
    175000.00,
    'https://github.com/manmansamara/travel_agency/blob/main/image10.jpg'
);