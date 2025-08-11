from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify
import os
from django.conf import settings
from django.contrib.staticfiles import finders



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def _get_logo_path():
    path = finders.find("images/logo.png")  
    if path and os.path.exists(path):
        return path
    fallback = os.path.join(settings.BASE_DIR, "static", "images", "logo.png")
    return fallback if os.path.exists(fallback) else None

class Project(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(default='2000-01-01')
    main_image = models.ImageField(upload_to='project_images/main/', null=True, blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    tags = TaggableManager(blank=True)

    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('preview_slug', kwargs={'project_id': self.id, 'slug': self.slug})

    def add_logo(self, img):
        """Dodaje logo w prawym dolnym rogu."""
        logo_path = _get_logo_path()
        if not logo_path:
            return img

        with Image.open(logo_path) as logo:
            logo = logo.convert("RGBA")
            logo_width = int(img.width * 0.1)
            ratio = logo_width / logo.width
            logo_height = int(logo.height * ratio)
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

            x = img.width - logo.width - 10
            y = img.height - logo.height - 10

            # mask=logo – gwarantuje użycie kanału alfa
            img.paste(logo, (x, y), mask=logo)
        return img


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # pierwszy zapis

        if self.main_image:
            img_path = self.main_image.path
            img = Image.open(img_path).convert("RGBA")

            # Dodanie logo
            img = self.add_logo(img)

            # Konwersja do WebP
            buffer = BytesIO()
            img = img.convert("RGB")
            filename = f"{slugify(self.title)}-main.webp"
            img.save(buffer, format='WEBP', quality=80)
            self.main_image.save(filename, ContentFile(buffer.getvalue()), save=False)
            buffer.close()

        super().save(*args, **kwargs)  # drugi zapis


class ProjectImage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/gallery/')

    def __str__(self):
        return f"Image for {self.project.title}"

    def add_logo(self, img):
        logo_path = _get_logo_path()
        if not logo_path:
            return img

        with Image.open(logo_path) as logo:
            logo = logo.convert("RGBA")
            logo_width = int(img.width * 0.1)
            ratio = logo_width / logo.width
            logo_height = int(logo.height * ratio)
            logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

            x = img.width - logo.width - 10
            y = img.height - logo.height - 10

            # mask=logo – gwarantuje użycie kanału alfa
            img.paste(logo, (x, y), mask=logo)
        return img


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # zapis oryginału

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path).convert("RGBA")

            # Dodanie logo
            img = self.add_logo(img)

            # Konwersja i zapis do WebP
            buffer = BytesIO()
            img = img.convert("RGB")
            filename = f"{slugify(self.project.title)}-{self.pk}.webp"
            img.save(buffer, format='WEBP', quality=80)
            self.image.save(filename, ContentFile(buffer.getvalue()), save=False)
            buffer.close()

        super().save(*args, **kwargs)  # zapis z logo

class Client(models.Model):
    name = models.CharField("Nazwa firmy", max_length=100)
    logo = models.ImageField("Logo (WebP, automatyczna konwersja)", upload_to='clients/')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # otwórz obraz
        img = Image.open(self.logo)
        img = img.convert("RGB")

        # kompresuj + konwertuj do WebP
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=75)
        file_name = os.path.splitext(self.logo.name)[0] + ".webp"
        self.logo.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
