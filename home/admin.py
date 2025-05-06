from django.contrib import admin
from django import forms
from .models import Category, Project, ProfileCategory, ProfileContent
from tinymce.widgets import TinyMCE
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.templatetags.static import static


# Custom AdminSite class
def get_site_url():
    return format_html('<a href="/" class="btn btn-primary">Go to Site</a>')


class MyAdminSite(AdminSite):
    site_header = "My Custom Admin Panel"
    site_title = "Admin Panel"

    class Media:
        css = {
            'all': [static('assets/css/admin.css')]
        }


custom_admin_site = MyAdminSite(name='custom_admin')


# -------------------- Project Admin ----------------------
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'rating')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'client_name')
    list_editable = ('category',)


# -------------------- Profile Admin ----------------------
class ProfileContentAdminForm(forms.ModelForm):
    class Meta:
        model = ProfileContent
        fields = ['category', 'title', 'image', 'content']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class ProfileCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class ProfileContentAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'image']
    search_fields = ['title', 'category__name']
    form = ProfileContentAdminForm


# Register models to custom admin
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Project, ProjectAdmin)
custom_admin_site.register(ProfileCategory, ProfileCategoryAdmin)
custom_admin_site.register(ProfileContent, ProfileContentAdmin)
