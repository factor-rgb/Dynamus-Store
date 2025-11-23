from django.contrib import admin
from .models import (
    Color, Fur_shape, Pattern, Gender,
    Employee, Eyes_color, Fur, Breed, Pet
)


# <-------------------
# Inlines
# <-------------------
class BreedInline(admin.TabularInline):
    model = Breed
    extra = 0
    fields = ("name", "fur", "eyes_color")
    show_change_link = True


class PetInline(admin.TabularInline):
    model = Pet
    extra = 0
    fields = ("name", "age", "gender", "entry_date", "size")
    readonly_fields = ("entry_date",)
    show_change_link = True


# <-------------------
# MODELOS SIMPLES
# <-------------------
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Fur_shape)
class FurShapeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


# <-------------------
# MODELOS COMPLEJOS
# <-------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "age", "access_level")
    search_fields = ("user__username", "user__email")
    list_filter = ("access_level",)
    readonly_fields = ("id",)
    raw_id_fields = ("user",)
    ordering = ("user__username",)
    save_on_top = True


@admin.register(Eyes_color)
class EyesColorAdmin(admin.ModelAdmin):
    list_display = ("right_eye_color", "left_eye_color", "heterochromia")
    list_filter = ("heterochromia", "right_eye_color", "left_eye_color")
    search_fields = (
        "right_eye_color__name",
        "left_eye_color__name",
    )
    autocomplete_fields = ("right_eye_color", "left_eye_color")
    ordering = ("right_eye_color__name", "left_eye_color__name")
    inlines = [BreedInline]
    save_on_top = True


@admin.register(Fur)
class FurAdmin(admin.ModelAdmin):
    list_display = ("shape", "primary_color", "secondary_color", "pattern")
    list_filter = ("shape", "primary_color", "secondary_color", "pattern")
    search_fields = (
        "shape__name",
        "primary_color__name",
        "secondary_color__name",
        "pattern__name",
    )
    autocomplete_fields = ("shape", "primary_color", "secondary_color", "pattern")
    ordering = ("shape__name", "primary_color__name")
    inlines = [BreedInline]
    save_on_top = True


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ("name", "fur", "eyes_color")
    list_filter = ("fur", "eyes_color")
    search_fields = (
        "name",
        "fur__shape__name",
        "eyes_color__right_eye_color__name",
    )
    autocomplete_fields = ("fur", "eyes_color")
    inlines = [PetInline]
    ordering = ("name",)
    save_on_top = True


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "gender", "age", "entry_date")
    list_filter = ("breed", "gender")
    search_fields = ("name", "breed__name")
    autocomplete_fields = ("breed", "gender")
    readonly_fields = ("entry_date",)
    ordering = ("name", "-entry_date")
    list_select_related = ("breed", "gender")
    fieldsets = (
        (None, {
            "fields": ("name", "age", "breed", "gender", "size", "annotations")
        }),
        ("Control", {
            "fields": ("entry_date",),
            "description": "Fecha generada automáticamente (no editable)."
        }),
    )
    save_on_top = True