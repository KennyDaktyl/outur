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
