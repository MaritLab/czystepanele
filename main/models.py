from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.staticfiles import finders
from django.conf import settings

import os


# ============================================================
# LOGO FINDER
# ============================================================

def _get_logo_path():
    """
    Wyszukuje logo w staticfiles. Działa poprawnie przy collectstatic.
    """
    path = finders.find("images/logo.png")
    if path and os.path.exists(path):
        return path

    # fallback
    fallback = os.path.join(settings.BASE_DIR, "static", "images", "logo.png")
    return fallback if os.path.exists(fallback) else None


def add_logo_to_image(img, scale=0.1):
    """
    Nakłada logo na obrazek (w prawym dolnym rogu).
    scale = procent szerokości obrazu (np. 0.1 = 10%)
    """
    logo_path = _get_logo_path()
    if not logo_path:
        return img

    with Image.open(logo_path).convert("RGBA") as logo:
        logo_width = int(img.width * scale)
        ratio = logo_width / logo.width
        logo_height = int(logo.height * ratio)

        logo = logo.resize((logo_width, logo_height), Image.LANCZOS)

        x = img.width - logo.width - 10
        y = img.height - logo.height - 10

        img.paste(logo, (x, y), logo)

    return img


def convert_to_webp(img, quality=80):
    """
    Konwertuje obraz do WebP i zwraca ContentFile.
    """
    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=quality)
    return ContentFile(buffer.getvalue())


# ============================================================
# CATEGORY (dla realizacji)
# ============================================================

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# PROJECT (REALIZACJA) — NOWA WERSJA PREMIUM
# ============================================================

class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    main_image = models.ImageField(upload_to="project_images/main/", blank=True, null=True)

    slug = models.SlugField(max_length=200, blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("preview_slug", kwargs={"project_id": self.id, "slug": self.slug})

    def save(self, *args, **kwargs):
        # slug
        if not self.slug:
            self.slug = slugify(self.title)

        # standardowy save (musi być pierwszy)
        super().save(*args, **kwargs)

        # przetwarzanie miniatury
        if self.main_image:
            self.main_image.open()
            img = Image.open(self.main_image).convert("RGBA")

            img = add_logo_to_image(img, scale=0.10)

            img = img.convert("RGB")
            file = convert_to_webp(img)

            filename = f"{slugify(self.title)}-main.webp"
            self.main_image.save(filename, file, save=False)

            super().save(update_fields=["main_image"])


# ============================================================
# PROJECT IMAGE (GALERIA REALIZACJI)
# ============================================================

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="project_images/gallery/")

    def __str__(self):
        return f"Image for {self.project.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # musimy mieć pk i path

        self.image.open()
        img = Image.open(self.image).convert("RGBA")

        img = add_logo_to_image(img, scale=0.20)

        img = img.convert("RGB")
        file = convert_to_webp(img)

        filename = f"{slugify(self.project.title)}-{self.pk}.webp"
        self.image.save(filename, file, save=False)

        super().save(update_fields=["image"])


# ============================================================
# CLIENT (dynamiczna sekcja „Zaufali nam”)
# ============================================================

class Client(models.Model):
    name = models.CharField("Nazwa firmy", max_length=100)
    logo = models.ImageField("Logo (WebP, automatyczna konwersja)", upload_to="clients/")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.logo.open()
        img = Image.open(self.logo).convert("RGB")

        file = convert_to_webp(img, quality=75)
        filename = f"{os.path.splitext(self.logo.name)[0]}.webp"

        self.logo.save(filename, file, save=False)

        super().save(update_fields=["logo"])


# ============================================================
# BLOG — CATEGORY
# ============================================================

class BlogCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# BLOG POST MODEL
# ============================================================

class BlogPost(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    intro = models.TextField(help_text="Krótki opis widoczny na liście wpisów.")
    content = models.TextField(help_text="Treść pełnego artykułu (HTML lub Markdown).")

    thumbnail = models.ImageField(upload_to="blog/thumbnails/", blank=True, null=True)

    published = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_post", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.thumbnail:
            self.thumbnail.open()
            img = Image.open(self.thumbnail).convert("RGBA")

            img = add_logo_to_image(img, scale=0.12)

            img = img.convert("RGB")
            file = convert_to_webp(img)

            filename = f"{slugify(self.title)}-thumb.webp"
            self.thumbnail.save(filename, file, save=False)

            super().save(update_fields=["thumbnail"])


# ============================================================
# BLOG GALLERY
# ============================================================

class BlogImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog/gallery/")

    def __str__(self):
        return f"Image for: {self.post.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.image.open()
        img = Image.open(self.image).convert("RGBA")

        img = add_logo_to_image(img, scale=0.15)

        img = img.convert("RGB")
        file = convert_to_webp(img)

        filename = f"{slugify(self.post.title)}-{self.pk}.webp"
        self.image.save(filename, file, save=False)

        super().save(update_fields=["image"])
