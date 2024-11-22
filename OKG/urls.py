"""
URL configuration for OKG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from Accounts.views import user_login
from Courses.views import course_list, course_detail, delete_note, update_note, create_note
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login, name='login'),
    path('courses/', course_list, name='course_list'),
    path('courses/<int:id>/', course_detail, name='course_detail'),
    path('create_note/', create_note, name='create_note'),  # Add this
    path('delete_note/', delete_note, name='delete_note'),  # Ensure this exists
    path('update_note/', update_note, name='update_note'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
