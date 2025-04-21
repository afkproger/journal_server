"""
URL configuration for journal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from server.views.reg_views import RegAPIView
from server.views.workspace_views import WorkspaceAPIView
from server.views.auth_views import LoginApiView
from server.views.friendship_views import FriendshipAPIView
from server.views.note_views import NoteAPIView
from server.views.chat_views import ChatAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/register/', RegAPIView.as_view()),
    path('api/v1/auth/',LoginApiView.as_view()),
    path('api/v1/workspace/' , WorkspaceAPIView.as_view()),
    path('api/v1/friendship/' , FriendshipAPIView.as_view()),
    path('api/v1/note/', NoteAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/chat/<str:other_username>/',ChatAPIView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)