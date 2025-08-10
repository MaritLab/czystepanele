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

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # pierwszy zapis, żeby mieć dostęp do image.path

        if self.main_image:
            from PIL import Image, ImageDraw, ImageFont
            from io import BytesIO
            from django.core.files.base import ContentFile

            img_path = self.main_image.path
            img = Image.open(img_path).convert("RGBA")

            # Znak wodny
            watermark_text = "© czystepanele.pl"
            draw = ImageDraw.Draw(img)
            font_size = int(min(img.size) * 0.04)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            textwidth = bbox[2] - bbox[0]
            textheight = bbox[3] - bbox[1]
            x = img.width - textwidth - 10
            y = img.height - textheight - 10
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

            # Kompresja i konwersja do WebP
            buffer = BytesIO()
            img = img.convert("RGB")
            filename = f"{slugify(self.title)}-main.webp"
            img.save(buffer, format='WEBP', quality=80)
            self.main_image.save(filename, ContentFile(buffer.getvalue()), save=False)
            buffer.close()

        super().save(*args, **kwargs)  # drugi zapis z przetworzonym plikiem


class ProjectImage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/gallery/')

    def __str__(self):
        return f"Image for {self.project.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Zapisz oryginał, żeby mieć dostęp do pliku

        if self.image:
            img_path = self.image.path
            img = Image.open(img_path).convert("RGBA")

            # Dodanie znaku wodnego
            watermark_text = "© czystepanele.pl"
            draw = ImageDraw.Draw(img)
            font_size = int(min(img.size) * 0.04)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            textwidth = bbox[2] - bbox[0]
            textheight = bbox[3] - bbox[1]
            x = img.width - textwidth - 10
            y = img.height - textheight - 10
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

            # Konwersja i zapis do WebP
            buffer = BytesIO()
            img = img.convert("RGB")
            filename = f"{slugify(self.project.title)}-{self.pk}.webp"
            img.save(buffer, format='WEBP', quality=80)
            self.image.save(filename, ContentFile(buffer.getvalue()), save=False)
            buffer.close()

        super().save(*args, **kwargs)  # drugi zapis z przetworzonym plikiem


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
