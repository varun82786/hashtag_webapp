import requests

# All the complex operations will be performed here

def get_top_keys(dictionary, top_n=1):

    # Set default top_n to 1 if it is None or less than 2
    if top_n is None or top_n < 2:
        top_n = 1

    # Sort the dictionary items by values in descending order
    sorted_items = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    # Get the top n items
    top_items = sorted_items[:top_n]

    # Extract keys from the top items
    top_keys = [item[0] for item in top_items]

    return top_keys

def get_indices_of_elements(raw_data, desired_elements):

    indices = []
    indexer = 0
    for ele in raw_data:
        if ele in desired_elements:
            indices.append(indexer)
        indexer += 1
            
    return indices

#this function gets the hastags based on gener of the hashtags and those hastags will be injected into the generated hashtags 
def gener_hashtags(hashtags_gen, parameter_data, hashtags_data, gener_data):
    gener_list = []
    #consolidated data for gener
    consolidated_data = {}
    hashtags_req = []
    
    for tags in hashtags_gen:
        
        idx = hashtags_data.index(tags)
        gener_list.append(gener_data[idx])
        
    unique_gener = set(gener_list)
    #print("\nunique_gener- ",unique_gener)
    
    for gener in unique_gener:
        consolidated_data[gener] = gener_list.count(gener)
    #print("\nconsolidated_data- ",consolidated_data)
        
    geners = get_top_keys(consolidated_data)
    #print("\ngeners- ",geners)
    
    idxs = set(get_indices_of_elements(gener_data, geners))
    #print("\nidxs -",idxs)
    
    for idx in idxs:
        hashtag = hashtags_data[idx]
        if hashtag not in hashtags_gen:
            if parameter_data[idx][0] >10:
               hashtags_req.append(hashtag)
               
    #print("\nhashtags_req- ",hashtags_req)
            
    # print(gener_list)
    # print(geners)
    # print(hashtags_req)
       
    return hashtags_req


def get_related_words(word):
    base_url = "https://api.datamuse.com/words"
    params = {"ml": word}  # 'ml' stands for means like (related words)

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check if the request was successful

        data = response.json()
        #print(data)
        # Sort the related words based on their scores (relevance)
        related_words = sorted(data, key=lambda x: x.get("score",0), reverse=True)
        related_words = [entry["word"] for entry in related_words]

        return related_words
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    
def get_synonyms(word):
    base_url = "https://api.datamuse.com/words"
    params = {"rel_syn": word}  # 'rel_syn' stands for related synonym

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check if the request was successful

        data = response.json()
        #print(data)
        synonyms = [entry["word"] for entry in data]

        return synonyms
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []