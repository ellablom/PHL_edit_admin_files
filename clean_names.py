# Function to strip and clean admin names for joining
from unidecode import unidecode

# Input: Pandas column
def get_clean_names(origin_column):
    # Make names lowercase
    new_column = origin_column.str.casefold()
    # Specify list of elements to be removed from location name
    strings_to_remove = [
        # Any information in brackets
        r"\(.*\)",
        # All references to "City", "City of", etc.
        "city of", "city", "brgy.", "barangay", "region",
        # Special characters 
        "-", r"\*"
    ]
    # Remove elements
    for string in strings_to_remove:
        new_column = new_column.str.replace(string, "", regex = True)
    # Replace diacritics
    new_column = new_column.apply(unidecode)
    # Set dictionary of Roman numerals to transform
    numeral_dict = {
        r"\si($|\s)": " 1",
        r"\sii($|\s)": " 2",
        r"\siii($|\s)": " 3",
        r"\siv($|\s)": " 4",
        r"\sv($|\s)": " 5",
        r"\svi($|\s)": " 6",
        r"\svii($|\s)": " 7",
        r"\sviii($|\s)": " 8",
        r"\six($|\s)": " 9",
        r"\sx($|\s)": " 10",
        r"\sxi($|\s)": " 11",
        r"\sxii($|\s)": " 12",
        r"\sxiii($|\s)": " 13"
    }
    # Replace Roman numerals
    for roman, arabic in numeral_dict.items():
        new_column = new_column.str.replace(roman, arabic, regex = True)
    # Replace st. and sta.
    new_column = new_column.str.replace("st.", "san")
    new_column = new_column.str.replace("sta.", "santa")
    # Strip white space
    new_column = new_column.str.strip()
    return(new_column)