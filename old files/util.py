import re
import pandas as pd
from thefuzz import fuzz
from thefuzz import process

# Function to clean up text, remove spaces, special characters, and numbers
def clean_text(text):
    
    # Convert text to uppercase for standardization
    text = text.upper()
    
    # Remove leading numbers or special characters
    text = re.sub(r'^[^a-zA-Z]+', '', text)
    
    # Remove 'WWW.' and '.COM' (case-insensitive)
    text = re.sub(r'WWW\.|\.COM', '', text, flags=re.IGNORECASE) 
    
    # Split into words and process each word to remove unwanted characters
    words = text.split()
    cleaned_words = [re.sub(r'[^a-zA-Z]+', '', word) for word in words if word]  # Clean each word

    return " ".join(cleaned_words)


###### ML Functions, may want to move to a different file 
# This Cleans up the data and changes descriptions to common vendors, using the common vendors text file in the directory
# if new vendors are added, add them to the text file
def StandardizeDescriptions(dataFrame):
    
    df = dataFrame

    # using the function in util to clean up the data and remove special characters, numbers, and standarizing with .upper 
    df['Cleaned_Text'] = df['Description'].apply(clean_text)
    
    # file in curr dir that has the list of common vendors 
    # uipdate this file with new vendors
    file_name = "common_vendors.txt"
    
    # open the file lf vendors
    with open(file_name, 'r') as file:
        contents = [line.split(',') for line in file.readlines()]
        contents = [[item.strip() for item in line] for line in contents]

    vendors = pd.DataFrame(contents)
    vendors.columns = ['Vendors']
    
    # converting dataframe column to  
    # list of elements 
    # to do fuzzy matching 
    list1 = df['Cleaned_Text'].tolist() 
    # print(vendors)
    list2 = vendors['Vendors'].tolist() 
    
    # empty lists for storing the matches 
    # later 
    mat1 = [] 
    mat2 = [] 
    p = [] 

    threshold = 70
    
    # iterating through list1 to extract 
    # it's closest match from list2 
    for i in list1: 
        mat1.append(process.extractOne( 
        i, list2, scorer=fuzz.partial_ratio)) 
    df['Matches'] = mat1 
    
    # iterating through the closest matches 
    # to filter out the maximum closest match 
    for j in df['Matches']: 
        # print('Check:' , j)
        if j[1] >= threshold: 
            p.append(j[0]) 
        mat2.append(",".join(p)) 
        p = [] 
        
    # print(mat2)
    # storing the resultant matches back  
    # to dframe1 

    # print(mat2.to_string())
    df['Matches'] = mat2 
    # print(df.to_string())
    
    # print("checking if we missed any entries")
    fls = df["Matches"] == ''
    
    # print(fls.to_string())
    
    result = df[fls == True]
    
    # print(result.to_string())
    # print(df.to_string())
    
    return df