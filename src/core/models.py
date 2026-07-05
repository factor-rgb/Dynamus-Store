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


class Pet_image_type(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class sponsor(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    access_level = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    phone = models.CharField(max_length=20, blank=True, null=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.phone and not self.user.email:
            raise ValidationError(
                "The employee must have an email address or a phone number."
            )

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
            return f'R {self.right_eye_color} - L {self.left_eye_color}'
        return f"{self.right_eye_color}"

    def clean(self):
        super().clean()

        if self.left_eye_color and self.right_eye_color:
            if self.left_eye_color != self.right_eye_color and not self.heterochromia:
                raise ValidationError({
                    'heterochromia': _(
                        'If the eyes has unlike colors, heterochromia must be actived.'
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

    pattern = models.ForeignKey(Pattern, on_delete=models.SET_NULL, null=True)

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


class Pet_image(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    type = models.ForeignKey(Pet_image_type, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='pets/')

    def __str__(self):
        return f'{self.pet} - {self.type}'


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return self.title


class advertisement(models.Model):
    advertiser = models.ForeignKey(sponsor, on_delete=models.CASCADE)
    url = models.URLField(max_length=500, help_text="URL of the advertiser website")
    image = models.ImageField(upload_to='advertisements/')

    def __str__(self):
        return f'{self.advertiser} - {self.url}'