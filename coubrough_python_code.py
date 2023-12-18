# Import tabulate library 
from tabulate import tabulate

# Define function to get the tree names from the file
def read_names_from_file(file_path):
    names = []
    with open(file_path, 'r') as file:
        for line in file:
            names.append(line.strip())
    return names

# Define letter values
letter_values = {'Q': 1, 'Z': 1, 'J': 3, 'X': 3, 'K': 6, 'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7,
                 'B': 8, 'C': 8, 'M': 8, 'P': 8, 'D': 9, 'G': 9, 'L': 15, 'N': 15, 'R': 15, 'S': 15, 'T': 15,
                 'O': 20, 'U': 20, 'A': 25, 'I': 25, 'E': 35}

# Define function to calculate the letter score
def calculate_letter_score(letter, word):
    letter = letter.upper()  # Convert the letter to uppercase

    # Set default values
    first_letter_score = 0
    last_letter_score = 0
    letter_score = 0

    # Find the position of the letter in the word
    position = word.find(letter) + 1  

    if position == 1:
        first_letter_score = 0  # When a letter is the first letter in a word, it scores zero

    if position == len(word):
        last_letter_score = 20 if letter == 'E' else 5 # When a letter is the last letter in a word, it scores 5, unless the letter is an E, which scores 20

    if position != 1 and position != len(word):
        letter_score = letter_values.get(letter, 0)  # If a letter is neither the first nor last letter in a word, get the relevant letter score from the letter_values dictionary

    total_score = first_letter_score + last_letter_score + letter_score # Sum scores to calculate the overall score for that letter

    return total_score

    
# Define function to generate the abbreviations, and calculate the score for each abbreviation
def generate_abbreviations(name):
    abbreviations = set()  # Use a set to store unique abbreviations for each name
    
    first_letter = name[0] # The first letter in the abbreviation is always the first letter in the name

    # For names with multiple words, split into each word
    words = [word.strip("'") for word in name.split()]

    for word in words:
        for i in range(len(word) - 2):
            second_letter = word[i]
            for j in range(i + 1, len(word) - 1):
                third_letter = word[j]

                # Ensure the second letter is not the same as the first letter in the abbreviation
                if second_letter != first_letter:
                    # Ensure that only letters are used to form abbreviations
                    if all(c.isalpha() for c in [first_letter, second_letter, third_letter]):

                        abbreviation = first_letter + second_letter + third_letter

                        # Calculate scores for each letter of the abbreviation (except the first letter since it is always 0)
                        scores2 = calculate_letter_score(second_letter, word)
                        scores3 = calculate_letter_score(third_letter, word)

                        # Calculate position value for the second letter of the abbreviation
                        position = word.find(second_letter) + 1
                        position_score_l2 = 0 #set default value
                        if position == 2:
                            position_score_l2 = 1
                        elif position == 3:
                            position_score_l2 = 2
                        elif position >= 4:
                            position_score_l2 = 3

                        # Calculate position value for the third letter of the abbreviation
                        position = word.find(third_letter) + 1
                        position_score_l3 = 0 #set default value
                        if position == 2:
                            position_score_l3 = 1
                        elif position == 3:
                            position_score_l3 = 2
                        elif position >= 4:
                            position_score_l3 = 3

                        # Calculate the total position score for the abbreviation:
                        position_score = position_score_l2 + position_score_l3

                        # Accumulate scores for each position
                        total_score = scores2 + scores3 + position_score

                        # Add the abbreviation and score to the set
                        abbreviations.add((abbreviation, total_score, name))

    return list(abbreviations)


def main():
    try:
        # Prompt user for input file name
        #input_file = input("Enter the name of the input file (e.g., input.txt): ")
        input_file = ("/Users/elisecoubrough/AC50002 Python/") + input("Enter the name of the input file (e.g., input.txt): ") # takes the file name from user input and combines with the longer file path to give the full file path


        # Read names from the input file
        names = read_names_from_file(input_file)

        # List to store formatted results
        table_data = []

        # List to store all abbreviations with names and scores
        all_abbreviations = []

        # Set to store used abbreviations
        used_abbreviations = set() 

        # Generate abbreviations and calculate scores for each name
        for name in names:
            abbreviations_for_name = generate_abbreviations(name) 
        
            # Filtering to remove abbreviations that can be formed from more than one name on the list
            unique_abbreviations = [(abbr, score, name) for abbr, score, name in abbreviations_for_name if abbr not in used_abbreviations]
            
            all_abbreviations.extend(unique_abbreviations)
            used_abbreviations.update(abbr for abbr, _, _ in unique_abbreviations) # Update the set of used abbreviations

        # Sort the table_data based on the names
        table_data_sorted = sorted(table_data, key=lambda x: x[0])
        
        # Output the final results to the output file, display as a table
        table_headings = ["Name", "Abbreviation", "Score"] # specifies table column headings
        output_file_abbrevs = "coubrough_trees_abbrevs.txt" # specifies output file name
        with open(output_file_abbrevs, 'w') as file:
            file.write(tabulate(table_data_sorted, headers=["Name", "Abbreviation", "Score"], tablefmt="rounded_grid")) # writes the full results to the output file, formatted as a table

        print(f"Full results table written to: {output_file_abbrevs}")

        
        # Finding the best abbreviation for each name:
        best_abbreviations = {} # Create a dictionary to store the best abbreviation for each name

        # Append the results to table_data and find the best abbreviations
        for entry in sorted(all_abbreviations, key=lambda x: x[1]):
            abbr, score, current_name = entry
            table_data.append([current_name, abbr.upper(), score])

            # Update the best abbreviation for the current name
            if current_name not in best_abbreviations or score < best_abbreviations[current_name][1]:
                best_abbreviations[current_name] = (abbr.upper(), score)

        
        # For outputting the best abbreviations table:
        table_data_best_abbreviations = [[name, abbr, score] for name, (abbr, score) in best_abbreviations.items()] # Formats data for the table by creating a list of lists (ensures 3 columns in table)
        table_data_best_abbreviations_sorted = sorted(table_data_best_abbreviations, key=lambda x: x[0]) # Sort the best abbreviations table alphabetically by name

        # Output the best abbreviations table to a file
        output_file_best_abbrevs = "coubrough_trees_best_abbrevs.txt" # specifies the output file name
        with open(output_file_best_abbrevs, 'w') as file:
            file.write(tabulate(table_data_best_abbreviations_sorted, headers=["Name", "Best Abbreviation", "Best Score"], tablefmt="rounded_grid")) # writes the best abbreviation for each name to the output file, formatted as a table

        print(f"The best abbreviations for each name table can be viewed at: {output_file_best_abbrevs}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.") # If input file is incorrect, display error


# Call and run the main() function 
if __name__ == "__main__":
    main()