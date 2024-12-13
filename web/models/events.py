from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from multiselectfield import MultiSelectField

from web.constans import ADDED_BY_CHOICES, DAYS_OF_WEEK, ENTRY_CHOICES, EVENT_TYPE_CHOICES, LOCATION_CHOICES  


class Event(models.Model):
    # Informacje podstawowe o wydarzeniu
    name = models.CharField(
        max_length=140, 
        verbose_name="Nazwa wydarzenia",
        db_index=True
    )
    short_description = models.TextField(
        max_length=840, 
        verbose_name="Krótki opis wydarzenia"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Opis wydarzenia"
    )
    city = models.CharField(
        max_length=255, 
        verbose_name="Miasto wydarzenia"
    )
    street = models.CharField(
        max_length=255, 
        verbose_name="Ulica wydarzenia"
    )
    house_number = models.CharField(
        max_length=255, 
        verbose_name="Numer domu wydarzenia"
    )
    postal_code = models.CharField(
        max_length=6, 
        verbose_name="Kod pocztowy wydarzenia"
    )
    apartment_number = models.CharField(
        max_length=255, 
        verbose_name="Numer lokalu wydarzenia",
        blank=True,
        null=True
    )

    # Obrazy
    main_image = models.ImageField(
        upload_to="events/main_images/", 
        verbose_name="Zdjęcie główne",
        blank=True,
        null=True
    )
    gallery_image_1 = models.ImageField(
        upload_to="media/events/gallery_images/", 
        verbose_name="Zdjęcie galerii 1",
        blank=True,
        null=True
    )
    gallery_image_2 = models.ImageField(
        upload_to="media/events/gallery_images/", 
        verbose_name="Zdjęcie galerii 2",
        blank=True,
        null=True
    )
    gallery_image_3 = models.ImageField(
        upload_to="media/events/gallery_images/", 
        verbose_name="Zdjęcie galerii 3",
        blank=True,
        null=True
    )
    gallery_image_4 = models.ImageField(
        upload_to="media/events/gallery_images/", 
        verbose_name="Zdjęcie galerii 4",
        blank=True,
        null=True
    )
    
    # Czas trwania wydarzenia
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default="one_day",
        verbose_name="Rodzaj wydarzenia"
    )
    
    one_day_date = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Data wydarzenia"
    )
    is_multi_day = models.BooleanField(
        default=False, 
        verbose_name="Kilku dniowe"
    )
    start_date = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Data rozpoczęcia"
    )
    end_date = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Data zakończenia"
    )

    # Wydarzenia cykliczne
    is_recurring = models.BooleanField(
        default=False, 
        verbose_name="Wydarzenie cykliczne"
    )
    day_of_week = MultiSelectField(
        choices=DAYS_OF_WEEK,
        blank=True,
        null=True,
        verbose_name="Dni tygodnia",
        help_text="Wybierz dni tygodnia, w których odbywa się wydarzenie"
    )
    # Dane kontaktowe
    website = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="Strona www"
    )
    contact_email = models.EmailField(
        verbose_name="Adres e-mail"
    )

    # Kategoria i lokalizacja
    categories = models.ManyToManyField(
        "web.Category", 
        verbose_name="Rodzaj",
        related_name="events"
    )
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_CHOICES,
        default="inside",
        verbose_name="Gdzie"
    )
    entry_type = models.CharField(
        max_length=20,
        choices=ENTRY_CHOICES,
        verbose_name="Wstęp",
        default="free"
    )
    added_by = models.CharField(
        max_length=20,
        choices=ADDED_BY_CHOICES,
        verbose_name="Dodane przez",
        default="organizer"
    )

    # Lokalizacja geograficzna
    location = PointField(
        blank=True, 
        null=True, 
        verbose_name="Lokalizacja (szerokość i długość geograficzna)"
    )

    # Metadane
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Utworzone przez"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Data utworzenia",
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Data ostatniej aktualizacji"
    )

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
        ordering = ["-created_at"]  
        indexes = [
            models.Index(fields=["name"], name="idx_event_name"),
            models.Index(fields=["created_at"], name="idx_event_created_at")
        ]

    def __str__(self):
        return self.name

    def get_day_of_week_display(self):
        day_dict = dict(DAYS_OF_WEEK)
        return [day_dict.get(day, day) for day in self.day_of_week]

    
    @property
    def users_count(self):
        return self.participants.count()
    

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, related_name="participants", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="event_participations", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "Uczestnik"