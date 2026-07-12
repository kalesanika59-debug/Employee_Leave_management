from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from employees.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('employees/', include('employees.urls')),
    path('leaves/', include('leaves.urls')),
]