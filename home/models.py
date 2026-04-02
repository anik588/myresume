from django.db import models
from tinymce.models import HTMLField
import emoji


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_1 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='projects/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    project_link = models.URLField(blank=True, null=True)
    client_review = models.TextField(blank=True, null=True)
    client_name = models.CharField(max_length=255, blank=True, null=True)
    client_description = models.TextField(blank=True, null=True)
    client_profile_link = models.URLField(blank=True, null=True)
    client_portfolio_pic = models.ImageField(upload_to='client_portfolios/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=0, choices=[(i, i) for i in range(1, 6)])
    category = models.ForeignKey(Category, related_name='projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def get_field_names(self):
        field_names = {}
        for field in self._meta.fields:
            field_names[field.name] = getattr(self, field.name)
        return field_names


class ProfileCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile Category"
        verbose_name_plural = "Profile Categories"


class ProfileContent(models.Model):
    category = models.ForeignKey(ProfileCategory, on_delete=models.CASCADE, related_name="content")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    content = HTMLField()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.category.name} - {self.title}"

    def add_emoji(self, emoji_text):
        self.content = emoji.emojize(f"{self.content} {emoji_text}", use_aliases=True)
        self.save()
