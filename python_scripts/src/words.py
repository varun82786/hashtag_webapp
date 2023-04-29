import string

#function to that returs the string adding the lines one by one
def word_to_string(filename, num_lines):
    # Open the file and read its contents
    with open(filename, 'r') as f:
        # Read the first num_lines lines from the file
        lines = f.readlines()[:num_lines]
        
        # Concatenate the lines into a single string
        string = " ".join(lines)
        
        # Return the resulting string
        return string


def clean_string(raw_string):
    # Define characters to remove
    remove_chars = string.punctuation.replace("_", "") + "[]" + "\n"
    # The `string.punctuation` constant includes all punctuation marks except for the underscore character.
    # We remove the underscore character from the set of characters to remove so it is not deleted.
    # We also add square brackets and newline characters to the set of characters to remove.
    
    # Remove specified characters from the input string
    clean_string = "".join(char for char in raw_string if char not in remove_chars)
    # We iterate over each character in the input string, and only include it in the cleaned string
    # if it is not in the `remove_chars` set.
    
    return clean_string


def word_density(clean_string):
    # Split the input string into a list of words
    words = clean_string.split()
    
    # Count the total number of words in the input string
    num_words = len(words)
    
    # Count the number of occurrences of each word in the input string
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    # Calculate the density of each unique word in the input string
    word_density = {}
    for word, count in word_count.items():
        word_density[word] = count / num_words
    
    # Return a dictionary of word densities
    return word_density

def unique_words_string(raw_sentence):
    # Split the input string into a list of words
    words = raw_sentence.split()

    # Use a set to remove duplicate words
    unique_words = set(words)

    unique_words_list=list(unique_words)

    return unique_words_list

def hashtag_parametric_values(raw_sentence):
    hashtag_parametric_dict={}
    # Split the input string into a list of words
    words = raw_sentence.split()

    # Use a set to remove duplicate words
    unique_words = set(words)

    unique_words_list=list(unique_words)
    
    #count total words in both lists
    total_words=len(words)
    total_unq_words=len(unique_words)

    for hashtag in unique_words:

        num_of_occurances=words.count(hashtag)
        hashtag_density=num_of_occurances/total_words
        hashtag_parametric_dict[hashtag]=(num_of_occurances,hashtag_density)
    
    return hashtag_parametric_dict




    



#function to send data to where this file is imported
def send_data():
    filename = 'python_scripts\data\\all_top_200post.txt'
    num_lines = 4241
    text = word_to_string(filename, num_lines)
    clean_text = clean_string(text)
    unique_list_of_words=unique_words_string(clean_text)
    hashtag_parameters=hashtag_parametric_values(clean_text)

    return clean_text,unique_list_of_words,hashtag_parameters


print(send_data()[2])


    

#debug here for all the functions written in the file

# Example usage
#filename = 'S:\insta_project\projectinstagram\projectinstagram\instagram_scraping\hastags\data_req\data\\all_top_200post.txt'
#num_lines = 4241


#word_density = calculate_word_density(filename, num_lines)
#print(word_density)
#print("\n number of unique hastags in latest {} posts are {}\n".format(num_lines,len(word_density)))
#for tup in word_density:
#    print(tup)

"""
text = word_to_string(filename, num_lines)
#print(text)

clean_text = clean_string(text)
print(clean_text)
print("\n")
#print(word_density(clean_text))
"""