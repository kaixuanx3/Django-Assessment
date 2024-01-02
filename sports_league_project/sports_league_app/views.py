from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Game
from .forms import GameUploadForm, GameForm
from io import TextIOWrapper
from django.db.models import F, Sum
from django.db.models import Case, When, Value, IntegerField
import csv

def upload_csv(request):
    if request.method == 'POST':
        form = GameUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Process the CSV file
            handle_uploaded_file(csv_file)

            return redirect('game_list')
    else:
        form = GameUploadForm()
    return render(request, 'upload_csv.html', {'form': form})

def handle_uploaded_file(csv_file):
    try:
        # Remove existing games
        Game.objects.all().delete()

        decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8-sig', errors='replace')
        reader = csv.reader(decoded_file)

        # Read the first line
        first_line = next(reader, None)

        # Check if the first character is the BOM
        #if first_line and first_line[0].startswith('\ufeff'):
        #    print(f"Ignoring BOM line: {first_line}")
        #    first_line[0] = first_line[0][1:]

        for line in [first_line] + list(reader):
            # Check for null bytes in the line
            if '\x00' in line:
                print(f"Ignoring line with null byte: {line}")
                continue

            if len(line) == 1:
                # Remove surrounding double quotes from the entire line
                line[0] = line[0].strip('"')

                # Split the line by commas
                parts = line[0].split(',')
                if len(parts) == 4:
                    team1_name, team1_score, team2_name, team2_score = map(str.strip, parts)

                    # Remove non-numeric characters from scores
                    team1_score = ''.join(c for c in team1_score if c.isdigit())
                    team2_score = ''.join(c for c in team2_score if c.isdigit())

                    team1_score = int(team1_score) if team1_score.isdigit() else 0
                    team2_score = int(team2_score) if team2_score.isdigit() else 0

                    process_game(team1_name, team1_score, team2_name, team2_score)
                else:
                    # Ignore invalid lines in the CSV
                    print(f"Ignoring invalid line: {line}")
            else:
                # Ignore invalid lines in the CSV
                print(f"Ignoring invalid line: {line}")
    except Exception as e:
        # Log and print any exceptions during CSV processing
        print(f"Error processing CSV file: {e}")

def process_game(team1_name, team1_score, team2_name, team2_score):
    # Check if the game already exists
    existing_game = Game.objects.filter(
        team1_name=team1_name, team1_score=team1_score,
        team2_name=team2_name, team2_score=team2_score
    ).first()

    if existing_game:
        print(f"Game already exists: {existing_game}")
    else:
        game = Game(team1_name=team1_name, team1_score=team1_score, team2_name=team2_name, team2_score=team2_score)
        game.save()

def game_list(request):
    # Calculate cumulative points and ranking for each team
    teams_ranking = (
        Game.objects.values('team1_name')
        .annotate(points=Sum(Case(
            When(team1_score__gt=F('team2_score'), then=Value(3)),
            When(team1_score=F('team2_score'), then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )))
        .annotate(team_name=F('team1_name'))
        .union(
            Game.objects.values('team2_name')
            .annotate(points=Sum(Case(
                When(team2_score__gt=F('team1_score'), then=Value(3)),
                When(team2_score=F('team1_score'), then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )))
            .annotate(team_name=F('team2_name'))
        )
        .order_by('-points', 'team_name')
    )

    return render(request, 'game_list.html', {'teams_ranking': teams_ranking})

def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_game')
    else:
        form = GameForm()
    return render(request, 'add_game.html', {'form': form})

def edit_game(request, team_name):
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('edit_game')
    else:
        form = GameForm(instance=game)
    return render(request, 'edit_game.html', {'form': form})

def delete_game(request, team_name):
    if request.method == 'POST':
        form = GameForm(request.POST)
        game.delete()
        return redirect('delete_game')
    return render(request, 'delete_game.html', {'form': form})

