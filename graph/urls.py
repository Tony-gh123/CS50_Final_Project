
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main.views.log import index, home
from main.views.log import signup, login_user, logout_user
from main.views.log import pdf_registry
from main.views.chat import admin_chat, chat, send, conversation

app_name = 'graph'

urlpatterns = [
    # landing page & admin
    path('admin/', admin.site.urls),
    path('home/', home, name="home"),
    path('', index, name='land'),
    # authentication and login
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    # file uploads
    path('user_profile/', pdf_registry, name='pdf_registry'),
    # user communication
    path('admin_chat/', admin_chat, name='admin_chat'),
    path('admin_chat/<int:recipient_id>/', admin_chat, name='admin_chat_user'),
    path('chat/', chat, name='chat'),
    path('send/<int:recipient_id>/', send, name='send'),
    path('conversation/<int:recipient_id>/', conversation, name='conversation' ),
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