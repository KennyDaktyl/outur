import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from django.utils.text import slugify

from web.constans import ADDED_BY_CHOICES, DAYS_OF_WEEK, ENTRY_CHOICES, EVENT_TYPE_CHOICES, LOCATION_CHOICES
from web.models.images import delete_thumbnails, make_thumbnail  


class Event(models.Model):
    # Informacje podstawowe o wydarzeniu
    name = models.CharField(
        max_length=140, 
        verbose_name="Nazwa wydarzenia",
        db_index=True
    )
    slug = models.SlugField(
        max_length=140, 
        verbose_name="Nazwa SEO",
        unique=True,
        blank=True,
        null=True
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
        verbose_name="Miejscowość wydarzenia"
    )
    street = models.CharField(
        max_length=255, 
        verbose_name="Ulica wydarzenia"
    )
    house_number = models.CharField(
        max_length=255, 
        verbose_name="Numer domu wydarzenia",
        blank=True,
        null=True
    )
    postal_code = models.CharField(
        max_length=6, 
        verbose_name="Kod pocztowy wydarzenia",
        blank=True,
        null=True
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
    thumbnails_cache = models.JSONField(default=dict, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktywne")
    
    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
        ordering = ["-created_at"]  
        indexes = [
            models.Index(fields=["name"], name="idx_event_name"),
            models.Index(fields=["created_at"], name="idx_event_created_at")
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name.replace("ł", "l"))
        
        old_main_image = self.__get_main_image()
        old_gallery_image_1 = self.__get_gallery_image_1()
        old_gallery_image_2 = self.__get_gallery_image_2()
        old_gallery_image_3 = self.__get_gallery_image_3()
        
        super(Event, self).save()
        
        if self.main_image != old_main_image:
            delete_thumbnails(self, self, 1, "event_id", "main_image")
            
            if self.main_image:
                self.thumbnails_cache["main_image"] = make_thumbnail(
                    self.main_image,
                    [(350, 260), (700, 520)],
                    1,
                    self,
                    "Event",
                )
            else:
                self.thumbnails_cache["main_image"] = {}
        
        if self.gallery_image_1 != old_gallery_image_1:
            delete_thumbnails(self, self, 2, "event_id", "gallery_image_1")
            
            if self.gallery_image_1:
                self.thumbnails_cache["gallery_image_1"] = make_thumbnail(
                    self.gallery_image_1,
                    [(350, 260), (700, 520)],
                    2,
                    self,
                    "Event",
                )
            else:
                self.thumbnails_cache["gallery_image_1"] = {}
        
        if self.gallery_image_2 != old_gallery_image_2:
            delete_thumbnails(self, self, 2, "event_id", "gallery_image_2")
            
            if self.gallery_image_2:
                self.thumbnails_cache["gallery_image_2"] = make_thumbnail(
                    self.gallery_image_1,
                    [(350, 260), (700, 520)],
                    2,
                    self,
                    "Event",
                )
            else:
                self.thumbnails_cache["gallery_image_2"] = {}
        
        if self.gallery_image_3 != old_gallery_image_3:
            delete_thumbnails(self, self, 3, "event_id", "gallery_image_3")
            
            if self.gallery_image_3:
                self.thumbnails_cache["gallery_image_3"] = make_thumbnail(
                    self.gallery_image_3,
                    [(350, 260), (700, 520)],
                    3,
                    self,
                    "Event",
                )
            else:
                self.thumbnails_cache["gallery_image_3"] = {}
        
        old_gallery_image_4 = self.__get_gallery_image_4()
        if self.gallery_image_4 != old_gallery_image_4:
            delete_thumbnails(self, self, 4, "event_id", "gallery_image_4")
            
            if self.gallery_image_4:
                self.thumbnails_cache["gallery_image_4"] = make_thumbnail(
                    self.gallery_image_4,
                    [(350, 260), (700, 520)],
                    4,
                    self,
                    "Event",
                )
            else:
                self.thumbnails_cache["gallery_image_4"] = {}
                
        super(Event, self).save()
        
    
    def __get_main_image(self):
        try:
            event = Event.objects.get(pk=self.pk)
            return event.main_image
        except Event.DoesNotExist:
            return None
    
    def __get_gallery_image_1(self):
        try:
            event = Event.objects.get(pk=self.pk)
            return event.gallery_image_1
        except Event.DoesNotExist:
            return None
    
    def __get_gallery_image_2(self):
        try:
            event = Event.objects.get(pk=self.pk)
            return event.gallery_image_2
        except Event.DoesNotExist:
            return None
    
    def __get_gallery_image_3(self):
        try:
            event = Event.objects.get(pk=self.pk)
            return event.gallery_image_3
        except Event.DoesNotExist:
            return None
    
    def __get_gallery_image_4(self):
        try:
            event = Event.objects.get(pk=self.pk)
            return event.gallery_image_4
        except Event.DoesNotExist:
            return None
    
    def __str__(self):
        return self.name

    def get_day_of_week_display(self):
        day_dict = dict(DAYS_OF_WEEK)
        return [day_dict.get(day, day) for day in self.day_of_week]

    
    @property
    def users_count(self):
        return self.participants.count()
    
    
    @property
    def address(self):
        parts = [self.street] 

        if self.house_number:
            house_part = f"{self.house_number}"
            if self.apartment_number:
                house_part += f"/{self.apartment_number}"
            parts.append(house_part)

        if self.postal_code:
            parts.append(f"{self.postal_code} {self.city}")
        else:
            parts.append(self.city)

        return ", ".join(parts)

    
    @property
    def date_info(self):
        if self.event_type == "one_day":
            return self.one_day_date.strftime("%d-%m-%Y %H:%M")
        elif self.event_type == "multi_day":
            return f"{self.start_date.strftime('%d-%m-%Y %H:%M')} - {self.end_date.strftime('%d-%m-%Y %H:%M')}"
        else:
            return f"{self.get_day_of_week_display()}"
        
    @property
    def gallery_images(self):
        gallery = []
        if self.gallery_image_1:
            gallery.append(self.gallery_image_1)
        if self.gallery_image_2:
            gallery.append(self.gallery_image_2)
        if self.gallery_image_3:
            gallery.append(self.gallery_image_3)
        if self.gallery_image_4:
            gallery.append(self.gallery_image_4)
        return gallery

    
    @property
    def formatted_one_day_date(self):
        if self.one_day_date:
            return self.one_day_date.strftime('%Y-%m-%d %H:%M')
        return ""
    

class EventMessage(models.Model):
    event = models.ForeignKey(Event, related_name="messages", on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, related_name="event_messages", on_delete=models.CASCADE, db_index=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
 

class EventLike(models.Model):
    event = models.ForeignKey(Event, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="event_likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "Polubienie"
        verbose_name_plural = "Polubienia"
           

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, related_name="participants", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="event_participations", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "Uczestnik"
        verbose_name_plural = "Uczestnicy"
        

@receiver(models.signals.post_delete, sender=Event)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.main_image:
        if os.path.isfile(instance.main_image.path):
            os.remove(instance.main_image.path)
    if instance.gallery_image_1:
        if os.path.isfile(instance.gallery_image_1.path):
            os.remove(instance.gallery_image_1.path)
    if instance.gallery_image_2:
        if os.path.isfile(instance.gallery_image_2.path):
            os.remove(instance.gallery_image_2.path)
    if instance.gallery_image_3:
        if os.path.isfile(instance.gallery_image_3.path):
            os.remove(instance.gallery_image_3.path)
    if instance.gallery_image_4:
        if os.path.isfile(instance.gallery_image_4.path):
            os.remove(instance.gallery_image_4.path)


@receiver(models.signals.pre_save, sender=Event)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Event.objects.get(pk=instance.pk).main_image
        new_file = instance.main_image
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Event.DoesNotExist:
        return False

    try:
        old_file = Event.objects.get(
            pk=instance.pk
        ).gallery_image_1
        new_file = instance.gallery_image_1
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Event.DoesNotExist:
        return False

    try:
        old_file = Event.objects.get(
            pk=instance.pk
        ).gallery_image_2
        new_file = instance.gallery_image_2
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Event.DoesNotExist:
        return False

    try:
        old_file = Event.objects.get(pk=instance.pk).gallery_image_3
        new_file = instance.gallery_image_3
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Event.DoesNotExist:
        return False
    
    try:
        old_file = Event.objects.get(pk=instance.pk).gallery_image_4
        new_file = instance.gallery_image_4
        if old_file and not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except Event.DoesNotExist:
        return False