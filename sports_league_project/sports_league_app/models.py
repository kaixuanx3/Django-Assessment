from django.db import models

class Game(models.Model):
    team1_name = models.CharField(max_length=255)
    team1_score = models.IntegerField()
    team2_name = models.CharField(max_length=255)
    team2_score = models.IntegerField()

    @property
    def points(self):
        # Calculate and return points based on the game result
        if self.team1_score > self.team2_score:
            return 3
        elif self.team1_score == self.team2_score:
            return 1
        else:
            return 0