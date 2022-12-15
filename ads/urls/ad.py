from django.urls import path

from ads import views

urlpatterns = [
    path('', views.AdView.as_view()),
    path('<int:pk>/', views.AdDetailView.as_view()),
]

# path('<int:pk>/', views.VacancyDetailView.as_view()),
    # path('create/', views.VacancyCreateView.as_view()),
    # path('<int:pk>/update/', views.VacancyUpdateView.as_view()),
    # path('<int:pk>/delete/', views.VacancyDeleteView.as_view()),
    # path('by_user/', views.UserVacancyDetailView.as_view()),