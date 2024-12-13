from django.contrib.gis.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField(
        verbose_name="Numer kategorii", null=True, blank=True, default=0
    )
    name = models.CharField(
        verbose_name="Nazwa kategorii", max_length=512, db_index=True
    )
    slug = models.SlugField(
        verbose_name="Slug", blank=True, null=True, max_length=512
    )
    is_active = models.BooleanField(
        verbose_name="Czy jest dostępny?", default=True
    )

    class Meta:
        ordering = (
            "order",
            "name",
        )
        verbose_name_plural = "Kategorie wydarzeń"

    def __str__(self):
        return self.name
    