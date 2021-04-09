from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authViews
from django.conf import settings
from SNS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', authViews.LoginView.as_view(), name='login'),
    path('accounts/logout/', authViews.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('', include('SNS.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
