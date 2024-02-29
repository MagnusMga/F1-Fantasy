from itertools import combinations
import csv

class Driver:
    def __init__(self, name, price, team):
        self.name = name
        self.price = price
        self.team = team
        self.points = 0

class Constructor:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.points = 0

# Example data
drivers = [
    Driver("Max Verstappen", 30.0, "Red Bull Racing"),
    Driver("Lando Norris", 23.0, "Mclaren"),
    Driver("Sergio Perez", 20.8, "Red Bull Racing"),
    Driver("Lewis Hamilton2", 19.3, "Mercedes"),
    Driver("Charles Leclerc", 19.1, "Ferrari"),
    Driver("Oscar Piastri", 19.0, "Mclaren"),
    Driver("George Russel", 18.8, "Mercedes"),
    Driver("Carlos Sainz", 18.5, "Ferrari"),
    Driver("Fernando Alonso", 15.8, "Aston Martin"),
    Driver("Lance Stroll", 10.7, "Aston Martin"),
    Driver("Daniel Ricciardo", 9.0, "RB"),
    Driver("Yuki Tsunoda", 8.0, "RB"),
    Driver("Pierre Gasly", 7.8, "Alpine"),
    Driver("Esteban Ocon", 7.8, "Alpine"),
    Driver("Alexander Albon", 7.0, "Williams"),
    Driver("Zhou Guanyu", 6.6, "Kick Sauber"),
    Driver("Valtteri Bottas", 6.4, "Kick Sauber"),
    Driver("Nico Hulkenberg", 6.4, "Haas F1 Team"),
    Driver("Kevin Magnussen", 6.2, "Haas F1 Team"),
    Driver("Logan Sargeant", 5.5, "Williams"),
]

constructors = [
    Constructor("Red Bull Racing", 27.9),
    Constructor("Mclaren", 23.2),
    Constructor("Mercedes", 20.1),
    Constructor("Ferrari", 19.3),
    Constructor("Aston Martin", 13.6),
    Constructor("RB", 8.5),
    Constructor("Alpine", 8.4),
    Constructor("Kick Sauber", 6.6),
    Constructor("Williams", 6.3),
    Constructor("Haas F1 Team", 6.3),
]

max_budget = 100.0  # Maximum budget for the fantasy team

# Generate all combinations of drivers and constructors
driver_combinations = combinations(drivers, 5)
constructor_combinations = combinations(constructors, 2)

# Filter valid teams based on budget constraint and calculate remaining budget
valid_teams = []
for driver_team in driver_combinations:
    constructor_combinations = combinations(constructors, 2)  # recreate the constructor combinations
    for constructor_team in constructor_combinations:
        total_price = sum(driver.price for driver in driver_team) + sum(constructor.price for constructor in constructor_team)
        if total_price <= max_budget:
            remaining_budget = max_budget - total_price
            valid_teams.append((driver_team, constructor_team, remaining_budget))

## Print valid teams
# for idx, team in enumerate(valid_teams, start=1):
#     print(f"Team {idx}:")
#     drivers, constructors, remaining_budget = team
#     print("Drivers:")
#     for driver in drivers:
#         print(f"Name: {driver.name}, Price: {driver.price}")
#     print("Constructors:")
#     for constructor in constructors:
#         print(f"Name: {constructor.name}, Price: {constructor.price}")
#     print(f"Remaining Budget: {remaining_budget}")
#     print()

print("Number of possible fantasy combinations")
print(len(valid_teams))

# # Sort valid teams based on remaining budget
# valid_teams.sort(key=lambda team: team[2])

# # Print the 10 teams with the least amount of budget remaining
# print("Top 10 teams with the least amount of budget remaining:")
# for idx, team in enumerate(valid_teams[:10], start=1):
#     print(f"Team {idx}:")
#     drivers, constructors, remaining_budget = team
#     print("Drivers:")
#     for driver in drivers:
#         print(f"Name: {driver.name}, Price: {driver.price}")
#     print("Constructors:")
#     for constructor in constructors:
#         print(f"Name: {constructor.name}, Price: {constructor.price}")
#     print(f"Remaining Budget: {remaining_budget}")
#     print()



# # Find all fantasy combinations with Red Bull Racing as constructor
# # and at least one of Max Verstappen or Sergio Perez as drivers
# found_combinations = []
# for team in valid_teams:
#     drivers, constructors, remaining_budget = team
#     if remaining_budget <= 0.5 and \
#        any(driver.name in ["Max Verstappen"] for driver in drivers) and \
#        any(constructor.name == "Red Bull Racing" for constructor in constructors):
#         found_combinations.append(team)

# # Print all found combinations
# if found_combinations:
#     print("Found fantasy combinations:")
#     for idx, combination in enumerate(found_combinations, start=1):
#         print(f"Combination {idx}:")
#         drivers, constructors, remaining_budget = combination
#         print("Drivers:")
#         for driver in drivers:
#             print(f"Name: {driver.name}, Price: {driver.price}")
#         print("Constructors:")
#         for constructor in constructors:
#             print(f"Name: {constructor.name}, Price: {constructor.price}")
#         print(f"Remaining Budget: {remaining_budget}")
#         print()
# else:
#     print("No fantasy combinations found with Red Bull Racing as constructor and at least one of Max Verstappen or Sergio Perez as drivers.")



######## LOADING CSV #######


# Define a function to load CSV data
def load_race_results(file_path):
    data = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            track_name = row['Track']
            if track_name not in data:
                data[track_name] = []
            data[track_name].append(row)
    return data


# List of file paths
file_paths = [
    "Formula1_2023season_raceResults.csv",
    "Formula1_2023season_qualifyingResults.csv",
    "Formula1_2023season_sprintResults.csv",
    "Formula1_2023season_sprintShootoutResults.csv"
]

all_data = {}
for file_path in file_paths:
    filename = file_path.split("_")[-1].split(".")[0]
    all_data[filename] = load_race_results(file_path)

# Separate the loaded data
race_results_data = all_data["raceResults"]
qualifying_results_data = all_data["qualifyingResults"]
sprint_results_data = all_data["sprintResults"]
sprint_shootout_results_data = all_data["sprintShootoutResults"]

### Process CSV Data
def calculate_position_change(race_results):
    for result in race_results:
        starting_grid = int(result['Starting Grid'])
        position = result['Position']
        if position.isdigit():
            position = int(position)
            position_change = starting_grid - position
        else:
            # Handle the case when position is "NC" (Not Classified)
            position_change = 0  # Or any other value you prefer
        result['Positions Changed'] = position_change
    return race_results

# Iterate over each race track name and its corresponding race results
for track_name, race_results in race_results_data.items():
    print(f"Race Results for {track_name}:")
    
    # Calculate position change for each race
    race_results_with_position_change = calculate_position_change(race_results)
    
    for result in race_results_with_position_change:
        print(result)
    
    print()  # Add a blank line between races for clarity

#### SCORING BASED ON 2023  ####

# Define the points system
points_system = {
    1: 25, 
    2: 18, 
    3: 15, 
    4: 12, 
    5: 10, 
    6: 8, 
    7: 6, 
    8: 4, 
    9: 2, 
    10: 1,
    # 11th - 20th place
    'DNF': -20, 
    'Disqualified': -25
}

points_system_quali = {
    1: 10,  # Pole position
    2: 9,
    3: 8,
    4: 7,
    5: 6,
    6: 5,
    7: 4,
    8: 3,
    9: 2,
    10: 1,
    # 11th - 20th place
    'NC': -5,  # No time set
    'Disqualified': -15
}


# Function to update driver points based on race results
def update_driver_points(race_results, drivers):
    for result in race_results:
        position = result['Position']
        for driver in drivers:
            if driver.name == result['Driver']:
                if position.isdigit():
                    position = int(position)
                    if 1 <= position <= 10:
                        driver.points += points_system[position]
                        # Add points for positions gained/lost
                        position_change = int(result['Positions Changed'])
                        if position_change > 0:
                            driver.points += position_change  # Points gained for positions gained
                        elif position_change < 0:
                            driver.points -= position_change  # Points lost for positions lost
                        # Add points for fastest lap
                        if result['Set Fastest Lap'] == 'Yes':
                            driver.points += 10
                        # Add points for Driver of the Day ### Not included atm #########################################
                        if result.get('Driver Of The Day', '').lower() == driver.name.lower():
                            driver.points += 10
                    elif position in ['DNF', 'Disqualified']:
                        driver.points += points_system[position]
                break

# Function to update driver points based on qualifying results
def update_driver_points_quali(qualifying_results, drivers):
    for result in qualifying_results:
        position = result['Position']
        for driver in drivers:
            if driver.name == result['Driver']:
                if position.isdigit():
                    position = int(position)
                    if 1 <= position <= 10:
                        driver.points += points_system_quali[position]
                elif position == 'NC':
                    driver.points += points_system_quali[position]
                elif position == 'Disqualified':
                    driver.points += points_system_quali[position]
                break



# Update driver points for each race
for race_results in race_results_data.values():
    update_driver_points(race_results, drivers)

# Update driver points for each race
for qualifying_results in qualifying_results_data.values():
    update_driver_points_quali(qualifying_results, drivers)

# Calculate constructor points based on drivers' points
for constructor in constructors:
    constructor.points = sum(driver.points for driver in drivers if driver.team == constructor.name)

# Print driver points
for driver in drivers:
    print(f"{driver.name}: {driver.points} points")
    
print("\n\n### Constructors ###\n\n")
# Print constructor points
for constructor in constructors:
    print(f"{constructor.name}: {constructor.points} points")



# Calculate team score based on driver and constructor points
team_scores = []
for driver_team, constructor_team, remaining_budget in valid_teams:
    team_score = 0
    # Calculate driver points for the team
    for driver in driver_team:
        team_score += driver.points
    # Calculate constructor points for the team
    for constructor in constructor_team:
        team_score += constructor.points
    team_scores.append((driver_team, constructor_team, team_score, remaining_budget))


# Sort team scores based on team score in descending order
team_scores.sort(key=lambda x: x[2], reverse=True)

print("\n\n\n")
# Print top 100 highest-scoring teams
print("Top 100 Highest-Scoring Teams:")
for idx, (driver_team, constructor_team, team_score, remaining_budget) in enumerate(team_scores[:100], start=1):
    print(f"Team {idx} Score: {team_score} points")

print("\n\n\n")

# Print highest scoring team and its drivers and constructors
highest_scoring_team = team_scores[0]
print("Highest Scoring Team:")
print(f"Team Score: {highest_scoring_team[2]} points")
print("Drivers:")
for driver in highest_scoring_team[0]:
    print(f"- {driver.name}")
print("Constructors:")
for constructor in highest_scoring_team[1]:
    print(f"- {constructor.name}")
