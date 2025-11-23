from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.db import models
import uuid


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Fur_shape(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Pattern(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genres'


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    access_level = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])

    def __str__(self):
        return self.user.username


class Eyes_color(models.Model):
    right_eye_color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        related_name="right_eye_usages"
    )

    left_eye_color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        related_name="left_eye_usages"
    )

    heterochromia = models.BooleanField()

    def __str__(self):
        if self.right_eye_color != self.left_eye_color:
            return f'Right {self.right_eye_color} - Left {self.left_eye_color}'
        return f"{self.right_eye_color}"

    def clean(self):
        super().clean()

        if self.left_eye_color and self.right_eye_color:
            if self.left_eye_color != self.right_eye_color and not self.heterochromia:
                raise ValidationError({
                    'heterochromia': _(
                        'Si los ojos tienen diferente color, debe activar heterocromia.'
                    )
                })

    class Meta:
        ordering = ('right_eye_color', 'left_eye_color')
        constraints = [
            models.UniqueConstraint(
                fields=['right_eye_color', 'left_eye_color'],
                name='unique_eye_color_pair'
            )
        ]


class Fur(models.Model):
    shape = models.ForeignKey(Fur_shape, on_delete=models.SET_NULL, null=True)
    primary_color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        related_name="fur_styles_usages"
    )

    secondary_color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="fur_syles_usages"
    )

    pattern = models.ForeignKey(Pattern, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.primary_color} - {self.pattern}'
    
    class Meta:
        ordering = ('shape', 'primary_color', 'secondary_color', 'pattern')
        constraints = [
            models.UniqueConstraint(
                fields=['shape', 'primary_color', 'secondary_color', 'pattern'],
                name='unique_fur_style'
            )
        ]


class Breed(models.Model):
    name = models.CharField(max_length=30)
    fur = models.ForeignKey(Fur, on_delete=models.SET_NULL, null=True)
    eyes_color = models.ForeignKey(Eyes_color, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.fur} - {self.eyes_color}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'fur', 'eyes_color'],
                name='unique_race_characteristics'
            )
        ]


class Pet(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    entry_date = models.DateTimeField(auto_now_add=True, editable=False)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    size = models.DecimalField(max_digits=4, decimal_places=2)
    annotations = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.breed} - {self.entry_date}'
    
    class Meta:
        ordering = ('name', 'breed', '-entry_date')