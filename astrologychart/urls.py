from django.urls import path, re_path
from . import views

app_name = 'astrologychart'

urlpatterns = [
    path('astrologychart/', views.astrologychart, name='astrologychart'),
    path('calclateastrology/', views.calculate_astrology, name='calculateastrology'),
    path('feedbackastrology/', views.feedback_astrology, name='feedbackastrology'),
]
