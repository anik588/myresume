from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic import CreateView
from .models import ProfileCategory, Project, Category  # Import ProfileCategory model
import datetime  # Ensure datetime is imported

# Home view (index page)
from django.shortcuts import render
from .forms import ContactForm

# views.py
from django.contrib.auth.models import User

MODEL_MAP = {
    'user': User,
    'project': Project,
    'category': Category,
    # add others...
}


def home(request):
    form = ContactForm()

    # Fetch all categories and prefetch related projects
    categories = Category.objects.prefetch_related('projects').all()
    profile_categories = ProfileCategory.objects.all()
    # Group projects by category (only include if they have at least 1 project)
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
        'title': 'Welcome to My Resume',
        'content': 'This is the home page of my resume website.',
        'profile_categories': profile_categories
    }

    return render(request, 'index.html', context)


# Portfolio views (ecommerce and newspaper)
def portfolio_ecommerce(request):
    return render(request, 'portfolio-ecommerce.html')


def portfolio_newspaper_site(request):
    return render(request, 'portfolio-newspaper-site.html')


# Contact form handling and email sending
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Prepare the email context
            context = {
                'name': name,
                'email': email,
                'message': message,
                'year': datetime.datetime.now().year
            }
            html_content = render_to_string('email.html', context)

            # Set up the email
            subject = 'New Message Request'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.DEFAULT_FROM_EMAIL]  # Replace with actual recipient if needed
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


# Project detail view
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Calculate the filled and empty stars
    filled_stars = range(project.rating)  # Creates a range of filled stars
    empty_stars = range(5 - project.rating)  # Creates a range of empty stars

    return render(request, 'project.html', {
        'project': project,
        'filled_stars': filled_stars,
        'empty_stars': empty_stars,
    })


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Project, Category, ProfileCategory, ProfileContent
#
# @login_required
# def dashboard_view(request):
#     return render(request, 'dashboard/dashboard.html', {
#         'projects': Project.objects.all(),
#         'categories': Category.objects.all(),
#         'profile_categories': ProfileCategory.objects.all(),
#         'profile_contents': ProfileContent.objects.all(),
#     })

from django.apps import apps
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# 🧠 Helper to get any model from any app
def get_model_by_name(model_name):
    for app in apps.get_app_configs():
        try:
            return apps.get_model(app.label, model_name)
        except LookupError:
            continue
    raise LookupError(f"Model '{model_name}' not found in any app.")


# ✅ Home admin page: show all models from all apps
@login_required
def dashboard_home(request):
    all_models = []
    for app in apps.get_app_configs():
        for model in app.get_models():
            try:
                # Add models to the admin section
                if model.__name__ in ['User', 'Group', 'Permission', 'LogEntry', 'ContentType', 'Session']:
                    all_models.append({
                        'name': model.__name__,
                        'verbose_name': model._meta.verbose_name_plural,
                    })
                else:
                    # Add other models to the main section
                    all_models.append({
                        'name': model.__name__,
                        'verbose_name': model._meta.verbose_name_plural,
                    })
            except:
                continue

    user_id = request.user.id or 0
    colors = ['red', 'blue', 'green', 'orange', 'indigo', 'teal', 'pink', 'yellow', 'purple', 'rose']
    user_color = colors[user_id % len(colors)]

    return render(request, 'dashboard/dashboard.html', {
        'models': all_models,
        'user_color': user_color
    })



# ✅ List all objects of a model
@login_required
def model_list(request, model_name):
    # Dynamically get model from string
    model = get_model_by_name(model_name)

    # Fetch all objects for this model
    objects = model.objects.all()

    # Pagination (optional: for large datasets)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, 10)
    paginated_objects = paginator.get_page(page)

    # Get model fields
    fields = model._meta.fields

    # Build object-value list
    objects_with_values = []
    for obj in paginated_objects:
        values = [field.value_from_object(obj) for field in fields]
        objects_with_values.append({'object': obj, 'values': values})

    # Color assignment (optional)
    user_id = request.user.id or 0
    colors = ['red', 'blue', 'green', 'orange', 'indigo', 'teal', 'pink', 'yellow', 'purple', 'rose']
    user_color = colors[user_id % len(colors)]

    # Render the template
    return render(request, 'dashboard/model_list.html', {
        'fields': fields,
        'objects_with_values': objects_with_values,
        'model_name': model_name,
        'user_color': user_color,
    })



# ✅ Add or edit a model object
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


# ✅ Delete a model object (from modal or direct)
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

    # fallback (in case delete modal not used)
    return render(request, 'dashboard/model_delete.html', {
        'object': obj,
        'model_name': model_name,
        'user_color': user_color
    })


from django.contrib.auth.decorators import login_required

@login_required
def some_view(request):
    # Your view logic
    pass
