# Django Assessment

## Overview

Django Assessment is a Django web application designed to manage and display the results of games in a sports league. Users can upload a CSV file containing game results, view a ranking table based on the uploaded data, and perform actions like adding, editing, and deleting games through the web interface.

## Problem Statement

The goal of this project is to implement a Django web application that meets the following requirements:

- Allow users to upload a CSV file containing game results.
- Display a ranking table based on the uploaded data.
- Enable users to add, edit, and delete games from the list.
- Calculate points for each game (3 points for a win, 1 point for a draw, 0 points for a loss).
- Rank teams based on points and alphabetical order in case of ties.

## Requirements

- Python: 3.9
- Django: 3.2

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Django-Assessment.git
cd Django-Assessment
```

Create and activate a virtual environment:
```bash
python -m venv myenv
myenv\Scripts\activate  # For mac users, use source myenv/bin/activate
```

Run migrations:
Make sure that you run this, after defining the model.
```bash
python manage.py makemigrations
python manage.py migrate
```

## Usage

1. Start the development server:
```bash
python manage.py runserver
```
2. Open your browser and navigate to http://localhost:8000.
3. Use the web interface to upload CSV files, view the ranking table, and perform other actions.

