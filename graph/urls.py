
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main.views import index, signup, login_user, logout_user, home
from main.views import pdf_registry, pdf_extract

app_name = 'graph'

urlpatterns = [
    path('', index, name='land'),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('home/', home, name="home"),
    path('user_profile/', pdf_registry, name='pdf_registry'),
    path('admin/', admin.site.urls),
    path('extract/', pdf_extract, name='pdf_extract')
]

#Configure Django to serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







"""
URL configuration for graph project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""