from django.contrib import admin
from django.urls import path, include  # Import the include function

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the app's URLs by specifying its namespace (if any)
    path('app/', include('todolist_app.urls', namespace='todolist_app')),
]
