from django.contrib import admin
from web.models.categories import Category
from web.models.events import Event, EventMessage, EventParticipant

from django.contrib.admin import ModelAdmin
from django.contrib.gis.db import models
from django.contrib.gis.forms import OSMWidget


class GeoModelAdminMixin:
    gis_widget = OSMWidget
    gis_widget_kwargs = {}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.GeometryField) and (
            db_field.dim < 3 or self.gis_widget.supports_3d
        ):
            kwargs["widget"] = self.gis_widget(**self.gis_widget_kwargs)
            return db_field.formfield(**kwargs)
        else:
            return super().formfield_for_dbfield(db_field, request, **kwargs)


class GISModelAdmin(GeoModelAdminMixin, ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("order", "name")
    fields = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order", "is_active")
    list_per_page = 20
    save_on_top = True
    list_display_links = ("name",)
    list_select_related = True
    list_max_show_all = 100


@admin.register(Event)
class EventCategoryAdmin(GISModelAdmin):
    list_display = ("id", "name", "start_date", "end_date")
    list_filter = ("categories", )
    search_fields = ("name", "city", "street", "postal_code", "house_number", "apartment_number")
    ordering = ("-start_date", "name")
    fields = (
        "name", "location", "short_description", "city", "street", "postal_code", "house_number", "apartment_number",
        "description", "main_image", "gallery_image_1", "gallery_image_2", "gallery_image_3", "gallery_image_4", "categories", "event_type",
        "one_day_date", "start_date", "end_date", "website", "contact_email", "location_type", "added_by", "entry_type", "day_of_week",
        "created_by", "created_at", "updated_at"
    )
    list_per_page = 20
    save_on_top = True
    list_display_links = ("name",)
    list_select_related = True
    list_max_show_all = 100
    filter_horizontal = ("categories",)
    date_hierarchy = "start_date"
    readonly_fields = ("created_by", "created_at", "updated_at")
    

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ("event", "user")
    

@admin.register(EventMessage)
class EventMessageAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "created_at")
    search_fields = ("event__name", "user__username")
    list_filter = ("event", "user")
    list_per_page = 20
    save_on_top = True
    list_display_links = ("event",)
    list_select_related = True
    list_max_show_all = 100
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)