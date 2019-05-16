from django import forms
from .models import Movie, Score

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'vote_average', 'popularity',]
        
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['review', 'score', 'spoiler',]