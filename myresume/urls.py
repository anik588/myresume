from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from home import views
from django.contrib.auth import views as auth_views


urlpatterns = [
#    path("admin/", custom_admin_site.urls),  # ✅ your custom admin site here
    path('admin/', views.dashboard_home, name='dashboard_home'),
    path('accounts/', include('django.contrib.auth.urls')),  # this gives you login/logout
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('admin/<str:model_name>/', views.model_list, name='model_list'),
    path('admin/<str:model_name>/add/', views.model_add_edit, name='model_add'),
    path('admin/<str:model_name>/<int:pk>/edit/', views.model_add_edit, name='model_edit'),
    path('admin/<str:model_name>/<int:pk>/delete/', views.model_delete, name='model_delete'),


    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('portfolio-ecommerce/', views.portfolio_ecommerce, name='portfolio_ecommerce'),
    path('portfolio-newspaper-site/', views.portfolio_newspaper_site, name='portfolio_newspaper_site'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),

]

# Static/media settings (OK)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
