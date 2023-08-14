from django.db import models
import random
from django.contrib.auth.models import User
from event.models import Event
from django.dispatch import receiver
from django.db.models.signals import post_save


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    events = models.ManyToManyField(Event, related_name="participants", blank=True)
    
    def __str__(self):
        return self.user.username


class StudentEventApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    artifacts = models.URLField(blank=True, null=True)
    custom_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.student.handle + ' - ' + str(self.event)


class StudentTeam(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Student, related_name="teams", blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="teams")

    def __str__(self):
        return self.name + ' - ' + str(self.event)


class StudentTeamEventApplictaion(models.Model):
    team = models.ForeignKey(StudentTeam, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    artifacts = models.URLField(blank=True, null=True)
    custom_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.team.name + ' - ' + str(self.event)


class Winner(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="winners")
    winner = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="wins")
    position = models.IntegerField()

    def __str__(self):
        return self.winner.handle + ' - ' + str(self.event) + ' - ' + str(self.position)


class WinningTeam(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="winning_teams")
    winner = models.ForeignKey(StudentTeam, on_delete=models.CASCADE, related_name="wins")
    position = models.IntegerField()

    def __str__(self):
        return self.winner.name + ' - ' + str(self.event) + ' - ' + str(self.position)


qualities = ["Hope", "Love", "Courage", "Curiosity", "Wisdom", "Empathy", "Patience", "Resilience", "Creativity", "Ambition", "Gratitude", "Determination", "Compassion", "Integrity", "Contentment", "Trust", "Forgiveness", "Generosity", "Humility", "Acceptance", "Serenity", "Joy", "Optimism", "Enthusiasm", "Harmony", "Kindness", "Sincerity", "Understanding", "Sympathy", "Empowerment", "Authenticity", "Perseverance", "Respect", "Open-mindedness", "Self-discipline", "Flexibility", "Equanimity", "Adaptability", "Tolerance", "Hopefulness", "Motivation", "Insight", "Imagination", "Peacefulness", "Clarity", "Tranquility", "Graciousness", "Altruism", "Consideration", "Resoluteness", "Resourcefulness", "Encouragement", "Positivity", "Harmony", "Gentleness", "Consistency", "Sacrifice", "Compromise", "Reverence", "Harmony", "Contentment", "Ambivalence", "Rationality", "Enlightenment", "Contentment", "Adaptation", "Equilibrium", "Maturity", "Perception", "Reflectiveness", "Remorse", "Nostalgia", "Dissonance", "Apprehension", "Fulfillment", "Acceptance", "Appreciation", "Longing", "Yearning", "Melancholy", "Anticipation", "Vulnerability", "Hesitation", "Certainty", "Ambiguity", "Ambivalence", "Discomfort", "Bittersweetness", "Perplexity", "Solitude", "Elation", "Confusion", "Satisfaction", "Guilt", "Euphoria", "Restlessness", "Melancholy", "Desolation", "Satisfaction", "Reflection"]

names = ["Einstein", "Newton", "Hawking", "Curie", "Bohr", "Feynman", "Schrödinger", "Hertz", "Planck", "Heisenberg", "Maxwell", "Tesla", "Dirac", "Galilei", "Coulomb", "Kepler", "Rutherford", "Fermi", "Oppenheimer", "Lorentz", "Schwarzschild", "Witten", "Gell-Mann", "Bethe", "Pauli", "Landau", "Hooke", "Hubble", "Euler", "Bose", "Chandrasekhar", "Mach", "Raman", "Dyson", "Mendeleev", "Schwinger", "Thomson", "Klein", "Ramanujan", "Hubble", "Ohm", "Franklin", "Kaku", "Gamow", "Fizeau", "Boltzmann", "Hawking", "Wheeler", "Schwartz", "Yang", "Lee", "Gödel", "Higgs", "Anderson", "Gauss", "Galvani", "Gibbs", "Bell", "Hertz", "Cavendish", "Fermi", "Fermi", "Laplace", "Langevin", "Laue", "Lenz", "Lorentz", "Mandelbrot", "Minkowski", "Millikan", "Möbius", "Nernst", "Noether", "Ohm", "Pauli", "Plank", "Poincaré", "Raman", "Rankine", "Ramanujan", "Riemann", "Rutherford", "Schrodinger", "Schrödinger", "Stark", "Teller", "Thomson", "Turing", "Volta", "Wegener", "Weierstrass", "Weisskopf", "Wigner", "Wilson", "Xuan", "Young", "Zwicky", "Feynman", "Witten", "Bohr", "Einstein"]


@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created:
        handle = f"{random.choice(names)}'s_{random.choice(qualities)}"
        Student.objects.create(user=instance, handle=handle)
