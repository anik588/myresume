from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic import CreateView
from .models import ProfileCategory, Project, Category
import datetime

# Home view (index page)
from .forms import ContactForm
from django.contrib.auth.models import User

MODEL_MAP = {
    'user': User,
    'project': Project,
    'category': Category,
}

def home(request):
    form = ContactForm()

    categories = Category.objects.prefetch_related('projects').all()
    profile_categories = ProfileCategory.objects.all()
    categorized_projects = [
        {
            'name': category.name,
            'projects': category.projects.all()
        }
        for category in categories
        if category.projects.exists()
    ]

    context = {
        'form': form,
        'categorized_projects': categorized_projects,
        'projects': Project.objects.all()[:12],
        'title': 'Welcome to My Resume',
        'content': 'This is the home page of my resume website.',
        'profile_categories': profile_categories
    }

    return render(request, 'index.html', context)

# Portfolio views
def portfolio_ecommerce(request):
    return render(request, 'portfolio-ecommerce.html')

def portfolio_newspaper_site(request):
    return render(request, 'portfolio-newspaper-site.html')

def portfolio_skill(request):
    form = ContactForm()

    categories = Category.objects.prefetch_related('projects').all()
    profile_categories = ProfileCategory.objects.all()
    categorized_projects = [
        {
            'name': category.name,
            'projects': category.projects.all()
        }
        for category in categories
        if category.projects.exists()
    ]

    context = {
        'form': form,
        'categorized_projects': categorized_projects,
        'profile_categories': profile_categories
    }

    return render(request, 'portfolio_skill.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            context = {
                'name': name,
                'email': email,
                'message': message,
                'year': datetime.datetime.now().year
            }
            html_content = render_to_string('email.html', context)

            subject = 'New Message Request'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.DEFAULT_FROM_EMAIL]
            email_message = EmailMultiAlternatives(subject, '', from_email, recipient_list)
            email_message.attach_alternative(html_content, "text/html")

            try:
                email_message.send()
                return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
            except Exception as e:
                print(f"Error sending email: {e}")
                return JsonResponse({'success': False, 'message': 'An error occurred while sending the message.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form submission.'})
    return render(request, 'index.html', {'form': ContactForm()})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    image_url = request.build_absolute_uri(project.image_1.url) if project.image_1 else None
    filled_stars = range(project.rating)
    empty_stars = range(5 - project.rating)

    return render(request, 'project.html', {
        'project': project,
        'filled_stars': filled_stars,
        'empty_stars': empty_stars,
        'project_image_absolute_url': image_url,
    })

from django.apps import apps
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_model_by_name(model_name):
    for app in apps.get_app_configs():
        try:
            return apps.get_model(app.label, model_name)
        except LookupError:
            continue
    raise LookupError(f"Model '{model_name}' not found in any app.")

@login_required
def dashboard_home(request):
    admin_models = []
    project_models = []
    profile_models = []

    for app in apps.get_app_configs():
        for model in app.get_models():
            try:
                model_info = {
                    'name': model.__name__,
                    'verbose_name': model._meta.verbose_name_plural,
                }

                if model.__name__ in ['User', 'Group', 'Permission', 'LogEntry', 'ContentType', 'Session']:
                    admin_models.append(model_info)
                elif model.__name__ in ['Category', 'Project']:
                    project_models.append(model_info)
                elif model.__name__ in ['ProfileCategory', 'ProfileContent']:
                    profile_models.append(model_info)

            except Exception:
                continue

    user_id = request.user.id or 0
    colors = ['red', 'blue', 'green', 'orange', 'indigo', 'teal', 'pink', 'yellow', 'purple', 'rose']
    user_color = colors[user_id % len(colors)]

    return render(request, 'dashboard/dashboard.html', {
        'admin_models': admin_models,
        'project_models': project_models,
        'profile_models': profile_models,
        'user_color': user_color,
        'recent': []
    })

@login_required
def model_list(request, model_name):
    model = get_model_by_name(model_name)

    objects = model.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(objects, 10)
    paginated_objects = paginator.get_page(page)

    fields = [field.name for field in model._meta.fields]

    objects_with_values = []
    for obj in paginated_objects:
        values = [getattr(obj, field) for field in fields]
        objects_with_values.append({'object': obj, 'values': values})

    return render(request, 'dashboard/model_list.html', {
        'objects_with_values': objects_with_values,
        'fields': fields,
        'model_name': model_name,
    })

@login_required
def model_add_edit(request, model_name, pk=None):
    model = get_model_by_name(model_name)
    instance = get_object_or_404(model, pk=pk) if pk else None
    Form = modelform_factory(model, fields='__all__')

    user_id = request.user.id or 0
    colors = ['red', 'blue', 'green', 'orange', 'indigo', 'teal', 'pink', 'yellow', 'purple', 'rose']
    user_color = colors[user_id % len(colors)]

    if request.method == 'POST':
        form = Form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            msg = f"{'Updated' if pk else 'Created'} {model_name} successfully."
            messages.success(request, msg)
            return redirect('model_list', model_name=model_name)
    else:
        form = Form(instance=instance)

    return render(request, 'dashboard/model_form.html', {
        'user_color': user_color,
        'form': form,
        'model_name': model_name,
        'is_edit': pk is not None
    })

@login_required
def model_delete(request, model_name, pk):
    model = get_model_by_name(model_name)
    obj = get_object_or_404(model, pk=pk)

    user_id = request.user.id or 0
    colors = ['red', 'blue', 'green', 'orange', 'indigo', 'teal', 'pink', 'yellow', 'purple', 'rose']
    user_color = colors[user_id % len(colors)]

    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{model_name} deleted successfully.")
        return redirect('model_list', model_name=model_name)

    return render(request, 'dashboard/model_delete.html', {
        'object': obj,
        'model_name': model_name,
        'user_color': user_color
    })

@login_required
def some_view(request):
    pass
