# import csv

# # List of participants (assuming they are labeled as Player 1, Player 2, ..., Player 8)
# participants = ["sujan sapkota", "nischal pandey", "sajan oli", "genius shresth", "aman saraaf", "prashant yadav", "haridesh gupta", "david shah"]

# # Generate all possible match combinations
# match_combinations = [(p1, p2) for p1 in participants for p2 in participants if p1 != p2]

# # Create CSV file for match schedule and match results
# with open('chess_tournament_schedule.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Match', 'Player 1', 'Player 2', 'Result']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
#     # Write header
#     writer.writeheader()
    
#     # Write match schedule
#     for idx, match in enumerate(match_combinations, start=1):
#         writer.writerow({'Match': f'Match {idx}', 'Player 1': match[0], 'Player 2': match[1], 'Result': ''})

# # Create CSV file for points table
# with open('chess_points_table.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Player', 'Points']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
#     # Write header
#     writer.writeheader()
    
#     # Initialize points for each player to 0
#     points_table = {participant: 0 for participant in participants}
    
#     # Write initial points table
#     for player, points in points_table.items():
#         writer.writerow({'Player': player, 'Points': points})
import csv

# List of participants
participants = ["sujan sapkota", "nischal pandey", "sajan oli", "genius shresth", "aman saraaf", "prashant yadav", "haridesh gupta", "david shah"]

# Generate all possible match combinations
match_combinations = [(p1, p2) for p1 in participants for p2 in participants if p1 != p2]

# Initialize match schedule and match results dictionaries
match_schedule = {f'Match {idx}': {'Player 1': match[0], 'Player 2': match[1], 'Result': ''} for idx, match in enumerate(match_combinations, start=1)}
match_results = {}

# Initialize points table dictionary
points_table = {participant: 0 for participant in participants}

# Function to update points table based on match results
def update_points_table(match_result):
    winner = match_result['Result']
    if winner == 'Player 1':
        points_table[match_result['Player 1']] += 1
    elif winner == 'Player 2':
        points_table[match_result['Player 2']] += 1

# Function to display points table
def display_points_table():
    print("\nPoints Table:")
    for player, points in points_table.items():
        print(f"{player}: {points} points")

# Main loop
while True:
    print("\n1. View Match Schedule")
    print("2. Record Match Result")
    print("3. View Points Table")
    print("4. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        print("\nMatch Schedule:")
        for match, details in match_schedule.items():
            print(f"{match}: {details['Player 1']} vs {details['Player 2']}")
    
    elif choice == '2':
        match_to_update = input("Enter the match to update (e.g., Match 1): ")
        if match_to_update in match_schedule:
            result = input("Enter the winner (Player 1 or Player 2): ")
            match_schedule[match_to_update]['Result'] = result
            match_results[match_to_update] = match_schedule[match_to_update]
            update_points_table(match_schedule[match_to_update])
            print("Match result recorded successfully.")
        else:
            print("Invalid match number. Please try again.")
    
    elif choice == '3':
        display_points_table()
    
    elif choice == '4':
        # Save match results and points table to CSV files
        with open('chess_match_results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Match', 'Player 1', 'Player 2', 'Result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for match, details in match_results.items():
                writer.writerow({'Match': match, 'Player 1': details['Player 1'], 'Player 2': details['Player 2'], 'Result': details['Result']})
        
        with open('chess_points_table.csv', 'w', newline='') as csvfile:
            fieldnames = ['Player', 'Points']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for player, points in points_table.items():
                writer.writerow({'Player': player, 'Points': points})
        
        print("Exiting the program.")
        break
    
    else:
        print("Invalid choice. Please try again.")
