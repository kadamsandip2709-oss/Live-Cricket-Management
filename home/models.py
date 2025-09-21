# home/models.py
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ✅ must be unique
    total_players = models.IntegerField()
    overs = models.IntegerField()
    wickets = models.IntegerField(editable=False)  # ✅ auto-calculated
    disqualified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # ✅ wickets = total players - 1
        if self.total_players >= 2:
            self.wickets = self.total_players - 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Player(models.Model):
    PLAYER_TYPES = (
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('allrounder', 'All Rounder'),
    )

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    player_type = models.CharField(max_length=20, choices=PLAYER_TYPES)

    def __str__(self):
        return f"{self.number} - {self.name} ({self.player_type})"


#Matches 
class Match(models.Model):
    team1 = models.ForeignKey("Team", related_name="team1_matches", on_delete=models.CASCADE)
    team2 = models.ForeignKey("Team", related_name="team2_matches", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    # Score fields
    team1_runs = models.PositiveIntegerField(default=0)
    team1_overs = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)  # Example: 10.2 overs
    team1_wickets = models.PositiveIntegerField(default=0)

    team2_runs = models.PositiveIntegerField(default=0)
    team2_overs = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
    team2_wickets = models.PositiveIntegerField(default=0)

    winner = models.ForeignKey("Team", related_name="won_matches", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name}"

    def decide_winner(self):
        """Automatically decide winner based on runs"""
        if self.team1_runs > self.team2_runs:
            self.winner = self.team1
        elif self.team2_runs > self.team1_runs:
            self.winner = self.team2
        else:
            self.winner = None  # Draw
        self.save()