# Import required modules
import sys
sys.path.append('python_scripts\libraries')
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#nltk.download('tagsets')
# Import words file
import words as w
import nltk_tags 

# Load  data, data will be loaded from words.py file which has many kind of data
data = w.send_data()
raw_hashtag_string=data[0]
uniq_hashtag_list=data[1]


# Unique hashtag lits to string conversion
hashtag_string=""
for ele in uniq_hashtag_list:
    hashtag_string += " "+ele

# Tokenize the hashtag text
tokens = word_tokenize(hashtag_string)

# Remove stop words
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if not word in stop_words]

# Categorize the words
tagged_tokens = nltk.pos_tag(filtered_tokens)


def search_words(keywords, data, num_results=None):
    """
    Searches for keywords in the given data and returns the words
    that contain any of the keywords along with their category.
    If num_results is specified, only returns the top num_results
    matching words.
    """
    # Tokenize the data
    tokens = word_tokenize(data)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if not word in stop_words]

    # Categorize the words
    tagged_tokens = nltk.pos_tag(filtered_tokens)
    #tag_dict = nltk.help.upenn_tagset()
    tag_dict=nltk_tags.nltk_tags()

    # Map the NLTK tags to their category names
    tag_map = {}
    for tag in tag_dict:
        if tag.isalpha():
            tag_map[tag] = tag_dict[tag]

    # Search for keywords in the tagged tokens
    matching_words = []
    for word, tag in tagged_tokens:
        if any(keyword.lower() in word.lower() for keyword in keywords):
            category = tag_map.get(tag, tag)
            matching_words.append((word, category))

    # Group matching words by category
    grouped_words = {}
    for word, category in matching_words:
        if category not in grouped_words:
            grouped_words[category] = []
        if word not in grouped_words[category]:
            grouped_words[category].append(word)

    # Sort the groups by number of matching words
    sorted_groups = sorted(grouped_words.items(), key=lambda x: len(x[1]), reverse=True)

    # If num_results is specified, only return the top num_results
    if num_results is not None:
        sorted_groups = sorted_groups[:num_results]

    return sorted_groups

# Example usage of search_words function
keywords = ['street','story']
num_results = None
matching_words = search_words(keywords, hashtag_string, num_results)
# print(f"Top {num_results} words matching {keywords}:")
# for category, words in matching_words:
#     print(f"{category}: {words}")

report=open("wordsreport.txt","w")
report.writelines(f"Top {num_results} words matching {keywords}:\n")
for category, words in matching_words:
    report.writelines(f"{category}: {words}\n")

report.close()

print(len(matching_words),"\n")
#print(matching_words[9])