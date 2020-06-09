from django import forms
from .models import AstrologyInfo


class AstrologyInfoForm(forms.ModelForm):
    class Meta:
        model = AstrologyInfo
        fields = ("user", "latitude", "longitude", "date", "time")


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = AstrologyInfo
        fields = ("user", "latitude", "longitude", "date", "time", "accuracy", "feedback")


