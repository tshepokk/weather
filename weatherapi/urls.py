from django.urls import path

from . import views
# import views

urlpatterns = [
	path("", views.home),

]