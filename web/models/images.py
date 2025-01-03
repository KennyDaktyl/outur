import logging
import os.path
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.core.files.base import ContentFile
from django.dispatch import receiver
from PIL import Image, ImageOps
from django.utils.text import slugify

from web.constans import IMAGE_TYPE

User = get_user_model()


class Thumbnail(models.Model):
    event_id = models.ForeignKey(
        "Event",
        db_index=True,
        verbose_name="Event",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="thumbs")
    mimetype = models.CharField(verbose_name="Typ pliku", max_length=16)
    width = models.IntegerField(verbose_name="Szerokość", default=0)
    height = models.IntegerField(verbose_name="Wysokość", default=0)
    image_type = models.IntegerField(
        db_index=True, verbose_name="Rodzaj zdjęcia", choices=IMAGE_TYPE
    )

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Thumbnails"

    def __str__(self):
        return self.image.path
    

def make_thumbnail(
    image, sizes, image_type, relation_object, relation_object_type, overwrite=True
):
    FTYPE = ["WEBP", "JPEG"]
    thumb_name, thumb_extension = os.path.splitext(image.name)
    thumb_name = slugify(thumb_name)
    if thumb_extension == ".png":
        FTYPE = ["WEBP", "PNG"]
    
    if relation_object_type == "Event" and overwrite:
        thumbnail_to_delete = Thumbnail.objects.filter(
            event_id=relation_object, image_type=image_type
        )
        thumbnail_to_delete.delete()
   
    thumbails_data = {"webp": {}, "jpeg": {}}
    for size in sizes:
        for ftype in FTYPE:
            try:
                img = Image.open(image)
            except IOError as e:
                logging.error(
                    f"Błąd otwarcia pliku: {image.path}. Error message: {str(e)}"
                )
                continue
            
            if ftype == "JPEG" and img.mode == "RGBA":
                img = img.convert("RGB")
                
            max_size = size
            width, height = img.size
            aspect_ratio = width / height

            new_width = min(width, max_size[0])
            new_height = int(new_width / aspect_ratio)
            if new_height > max_size[1]:
                new_height = max_size[1]
                new_width = int(new_height * aspect_ratio)

            image_crop = img.resize((new_width, new_height), resample=Image.LANCZOS)
            
            width, height = size
            thumb_extension = thumb_extension.lower()
            thumb_filename = (
                thumb_name + f"_{width}x{height}" + "." + ftype.lower()
            )
            temp_thumb = BytesIO()
            image_crop.save(temp_thumb, ftype, quality=100)
            temp_thumb.seek(0)
            thumbnail = Thumbnail()
            
            if relation_object_type == "Event":
                thumbnail.event_id = relation_object
                
            thumbnail.width = width
            thumbnail.height = height
            thumbnail.mimetype = "image/" + ftype.lower()
            thumbnail.image_type = image_type
            thumbnail.image.save(
                thumb_filename, ContentFile(temp_thumb.read()), save=False
            )
            thumbnail.save()
            temp_thumb.close()
            image_data = {f"{width}x{height}": str(thumbnail.image)}
            if ftype == "WEBP":
                thumbails_data["webp"].update(image_data)
            else:
                thumbails_data["jpeg"].update(image_data)
            # thumbails_data["oryg"].update(image.url)
    return thumbails_data


def delete_thumbnails(self, instance, image_type, field_name, cache_key):
    self.thumbnails_cache[cache_key] = {}

    filter_kwargs = {field_name: instance, "image_type": image_type}
    thumbs = Thumbnail.objects.filter(**filter_kwargs)
    if thumbs:
        thumbs.delete()
        
        
@receiver(models.signals.post_delete, sender=Thumbnail)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            try:
                os.remove(instance.image.path)
            except OSError:
                pass


@receiver(models.signals.pre_save, sender=Thumbnail)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Thumbnail.objects.get(pk=instance.pk).image
    except Thumbnail.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            try:
                os.remove(old_file.path)
            except OSError:
                pass