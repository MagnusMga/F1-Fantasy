from itertools import combinations
import csv

class Driver:
    def __init__(self, name, price, team):
        self.name = name
        self.price = price
        self.team = team

class Constructor:
    def __init__(self, name, price):
        self.name = name
        self.price = price

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


#### SCORING BASED ON 2023  ####
    
# Define a function to score the teams
def score_teams(valid_teams, race_results_data, qualifying_results_data, sprint_results_data):
    scored_teams = []
    for team in valid_teams:
        drivers, constructors, remaining_budget = team
        team_score = 0

        # Score for each race
        for race_name, race_results in race_results_data.items():
            # Filter race results for the current race
            race_results_for_race = [result for result in race_results if result['Track'] == race_name]
            
            # Score qualifying, sprint, and race for each driver
            for driver in drivers:
                qualifying_score = 0
                sprint_score = 0
                race_score = 0
                
                for result in race_results_for_race:
                    if result['Driver'] == driver.name:
                        # Score qualifying
                        for row in qualifying_results_data[race_name]:
                            if row['Driver'] == driver.name:
                                try:
                                    position = int(row['Position'])
                                    if position == 1:
                                        qualifying_score += 10
                                    elif position <= 10:
                                        qualifying_score += 11 - position
                                    elif position <= 20:
                                        qualifying_score += 0
                                    else:
                                        qualifying_score -= 5
                                except ValueError:
                                    # Handle the case where Position is not a valid integer
                                    pass
                            
                        # Score race
                        try:
                            position = int(result['Position'])
                            if position == 1:
                                race_score += 25
                            elif position <= 10:
                                race_score += 11 - position
                            elif position <= 20:
                                race_score += 0
                            else:
                                race_score -= 20
                        except ValueError:
                            # Handle the case where Position is not a valid integer
                            pass

                # Add scores for each race to the team score
                team_score += qualifying_score + sprint_score + race_score

            # Score constructors for each race
            constructor_score = 0
            for result in race_results_for_race:
                for constructor in constructors:
                    if result['Team'] == constructor.name:
                        # Score constructors
                        try:
                            position = int(result['Position'])
                            if position == 1:
                                constructor_score += 25
                            elif position <= 10:
                                constructor_score += 11 - position
                            elif position <= 20:
                                constructor_score += 0
                            else:
                                constructor_score -= 20
                        except ValueError:
                            # Handle the case where Position is not a valid integer
                            pass

            # Add constructor score to the team score
            team_score += constructor_score

            # Score sprint if available
            if race_name in sprint_results_data:
                sprint_results_for_race = [result for result in sprint_results_data[race_name] if result['Driver'] == driver.name]
                for result in sprint_results_for_race:
                    try:
                        position = int(result['Position'])
                        if position <= 8:
                            sprint_score += 9 - position
                        elif position <= 20:
                            sprint_score += 0
                        else:
                            sprint_score -= 20
                    except ValueError:
                        # Handle the case where Position is not a valid integer
                        pass

                # Add sprint score to the team score
                team_score += sprint_score

        scored_teams.append((team, team_score))
        
        
    
    return scored_teams

print("scored")



scored_teams = score_teams(valid_teams, race_results_data, qualifying_results_data, sprint_results_data)

# Sort scored teams by score in descending order
scored_teams.sort(key=lambda x: x[1], reverse=True)

# Print top 10 scored teams
print("Top 10 scored teams:")
for idx, (team, score) in enumerate(scored_teams[:10], start=1):
    drivers, constructors, remaining_budget = team
    print(f"Team {idx} - Score: {score}")
    print("Drivers:")
    for driver in drivers:
        print(f"Name: {driver.name}")
    print("Constructors:")
    for constructor in constructors:
        print(f"Name: {constructor.name}")
    print(f"Remaining Budget: {remaining_budget}")
    print()


print("Teams Printed")
print("Number of scored teams:", len(scored_teams))
