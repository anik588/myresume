from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique category name
    description = models.TextField(blank=True, null=True)  # Optional description of the category

    def __str__(self):
        return self.name


from django.db import models

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

    def get_field_names(self):
        """
        Return a dictionary of field names and values for this instance
        """
        field_names = {}
        for field in self._meta.fields:
            field_names[field.name] = getattr(self, field.name)
        return field_names



from django.db import models
from tinymce.models import HTMLField  # For rich text content (TinyMCE)
import emoji


# Category Model for Profile sections (e.g., "About Box", "Education", etc.)
class ProfileCategory(models.Model):
    name = models.CharField(max_length=100)  # e.g., "About Box", "Education", etc.
    description = models.TextField(blank=True, null=True)  # Optional description of the category

    def __str__(self):
        return self.name


# Content Model for storing actual profile content (linked to ProfileCategory)
class ProfileContent(models.Model):
    category = models.ForeignKey(ProfileCategory, on_delete=models.CASCADE, related_name="content")
    title = models.CharField(max_length=100)  # e.g., "My Bio", "Work Experience"
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Profile section image
    content = HTMLField()  # Rich text field (TinyMCE editor for styling, bold, italic, etc.)

    def __str__(self):
        return f"{self.category.name} - {self.title}"

    def add_emoji(self, emoji_text):
        """ Add emoji to the content dynamically (optional) """
        self.content = emoji.emojize(f"{self.content} {emoji_text}", use_aliases=True)
        self.save()


