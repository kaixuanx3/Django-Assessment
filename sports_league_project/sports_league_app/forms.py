from django import forms
from .models import Game

class GameUploadForm(forms.Form):
    csv_file = forms.FileField()

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['team1_name', 'team1_score', 'team2_name', 'team2_score']