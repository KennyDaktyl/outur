DAYS_OF_WEEK = [
    ('monday', 'Poniedziałek'),
    ('tuesday', 'Wtorek'),
    ('wednesday', 'Środa'),
    ('thursday', 'Czwartek'),
    ('friday', 'Piątek'),
    ('saturday', 'Sobota'),
    ('sunday', 'Niedziela'),
]

EVENT_TYPE_CHOICES = [
    ('one_day', "Jednodniowe"),
    ('multi_day', "Kilkudniowe"),
    ('recurring', "Cykliczne"),
]

LOCATION_CHOICES = [
    ('inside', 'Wewnątrz'),
    ('outside', 'Na zewnątrz'),
]

ENTRY_CHOICES = [
    ('free', 'Wolny'),
    ('paid', 'Płatny'),
]

ADDED_BY_CHOICES = [
    ('organizer', 'Organizatora'),
    ('participant', 'Uczestnika'),
]

IMAGE_TYPE = [
    (1, "Zdjęcie głowne"),
    (2, "Galeria 1"),
    (3, "Galeria 2"),
    (4, "Galeria 3"),
    (5, "Galeria 4"),
]

DATE_CHOICES = [
    ('all', 'Wszystkie'),
    ('today', 'Dzisiaj'),
    ('tomorrow', 'Jutro'),
    ('select_date', 'Wybierz datę'),
]