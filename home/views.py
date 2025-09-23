from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Team, Player, Match
from .forms import TeamForm, PlayerForm, MatchForm, MatchScoreForm


# ===================== AUTH VIEWS =====================
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# ===================== TEAM & PLAYER VIEWS =====================
@login_required(login_url="login")
def home(request):
    if request.method == "POST":
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            team = team_form.save()
            messages.success(request, f"Team '{team.name}' created successfully!")
            return redirect("home")  # refresh after saving
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        team_form = TeamForm()

    teams = Team.objects.all()
    return render(request, "home.html", {"team_form": team_form, "teams": teams})


@login_required(login_url="login")
def add_player(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if team.players.count() >= team.total_players:
        messages.error(request, f"Team {team.name} already has the maximum number of players.")
        return redirect("home")

    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.save()
            messages.success(request, f"Player '{player.name}' added to {team.name}!")
            return redirect("home")
    else:
        form = PlayerForm()

    return render(request, "add_player.html", {"form": form, "team": team})


@login_required(login_url="login")
def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.wickets = team.total_players - 1
            team.save()
            messages.success(request, f"Team '{team.name}' updated successfully!")
            return redirect("home")
    else:
        form = TeamForm(instance=team)
    return render(request, "edit_team.html", {"form": form, "team": team})


@login_required(login_url="login")
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == "POST":
        team.delete()
        messages.success(request, "Team deleted successfully!")
        return redirect("home")
    return render(request, "confirm_delete.html", {"object": team, "type": "Team"})


@login_required(login_url="login")
def edit_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, "Player updated successfully!")
            return redirect("home")
    else:
        form = PlayerForm(instance=player)
    return render(request, "edit_player.html", {"form": form, "player": player})


@login_required(login_url="login")
def delete_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == "POST":
        player.delete()
        messages.success(request, "Player deleted successfully!")
        return redirect("home")
    return render(request, "confirm_delete.html", {"object": player, "type": "Player"})


# ===================== MATCHES =====================
@login_required(login_url="login")
def matches(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Match scheduled successfully!")
            return redirect("matches")
    else:
        form = MatchForm()

    matches = Match.objects.all().order_by("-date")
    return render(request, "matches.html", {"form": form, "matches": matches})


@login_required(login_url="login")
def update_score(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if request.method == "POST":
        form = MatchScoreForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            match.decide_winner()
            messages.success(request, "Match score updated successfully!")
            return redirect("matches")
    else:
        form = MatchScoreForm(instance=match)

    return render(request, "update_score.html", {"form": form, "match": match})


# ===================== EXTRA PAGES =====================
@login_required(login_url="login")
def teams(request):
    teams = Team.objects.all()
    return render(request, "teams.html", {"teams": teams})


@login_required(login_url="login")
def players(request):
    players = Player.objects.select_related("team").all()
    return render(request, "players.html", {"players": players})
