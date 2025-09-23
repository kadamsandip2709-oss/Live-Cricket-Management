# home/forms.py
from django import forms
from .models import Team, Player
from .models import Match

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "total_players", "overs"]

    def clean_total_players(self):
        total_players = self.cleaned_data.get("total_players")
        if total_players < 2:
            raise forms.ValidationError("A team must have at least 2 players.")
        return total_players

    def clean_overs(self):
        overs = self.cleaned_data.get("overs")
        if overs < 1:
            raise forms.ValidationError("Overs must be at least 1.")
        return overs

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Team.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("A team with this name already exists.")
        return name


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["number", "name", "player_type"]


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["team1", "team2"]

    def clean(self):
        cleaned_data = super().clean()
        team1 = cleaned_data.get("team1")
        team2 = cleaned_data.get("team2")

        if team1 == team2:
            raise forms.ValidationError("A team cannot play against itself.")
        return cleaned_data


class MatchScoreForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            "team1_runs", "team1_overs", "team1_wickets",
            "team2_runs", "team2_overs", "team2_wickets"
        ]