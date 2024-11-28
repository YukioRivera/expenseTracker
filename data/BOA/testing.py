import pandas as pd
import re

df_boa = pd.read_csv("BOA_2024_April_1371.csv")
df_chase = pd.read_csv("../processed/2023_Chase9197_Activity20230101_20231231_20241127.CSV")
# print(df_boa)
# print("------------------------------------------------------------------------------")
# print(df_chase)

# def categoryj

category_keywords = {
    'Automotive': ['car', 'repair', 'auto', 'mechanic', 'tire', 'oil change'],
    'Bills & Utilities': ['electric', 'water', 'gas bill', 'internet', 'cable', 'phone', 'utility'],
    'Entertainment': ['movie', 'cinema', 'concert', 'amusement', 'netflix', 'hulu', 'spotify'],
    'Fees & Adjustments': ['fee', 'service charge', 'adjustment', 'overdraft', 'penalty'],
    'Food & Drink': ['restaurant', 'cafe', 'starbucks', 'mcdonald', 'taco bell', 'burger king', 'dining'],
    'Gas': ['gas', 'chevron', 'shell', 'exxon', 'mobil', 'arco'],
    'Gifts & Donations': ['gift', 'donation', 'charity', 'present', 'fundraiser'],
    'Groceries': ['walmart', 'target', 'kroger', 'safeway', 'costco', 'family dollar', 'aldi'],
    'Health & Wellness': ['pharmacy', 'cvs', 'walgreens', 'rite aid', 'hospital', 'clinic'],
    'Home': ['home depot', 'lowes', 'furniture', 'ikea', 'maintenance', 'appliance'],
    'Personal': ['gym', 'hair', 'spa', 'salon', 'self-care', 'personal trainer'],
    'Professional Services': ['consulting', 'legal', 'accounting', 'services', 'freelance'],
    'Shopping': ['amazon', 'ebay', 'mall', 'boutique', 'clothing', 'apparel', 'shoes'],
    'Travel': ['flight', 'hotel', 'airbnb', 'rental car', 'train', 'expedia', 'trip'],
}


# Function to clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # Remove non-letter characters
    return text.strip()

def assign_category(description):
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in description:
                return category
    return 'Uncategorized'  # Default category if no match found


# Assuming df_chase is your Chase DataFrame
vendor_category_map = df_chase[['Description', 'Category']].drop_duplicates()
vendor_category_map.set_index('Description', inplace=True)
vendor_category_map = vendor_category_map['Category'].to_dict()

df_boa['Cleaned_Description'] = df_boa['Description'].apply(clean_text)
df_chase['Cleaned_Description'] = df_chase['Description'].apply(clean_text)

vendor_category_map = df_chase[['Cleaned_Description', 'Category']].drop_duplicates()
vendor_category_map.set_index('Cleaned_Description', inplace=True)
vendor_category_map = vendor_category_map['Category'].to_dict()

df_boa['Category'] = df_boa['Cleaned_Description'].map(vendor_category_map)

# Identify unmapped descriptions
unmapped = df_boa['Category'].isnull()
df_boa.loc[unmapped, 'Category'] = df_boa.loc[unmapped, 'Cleaned_Description'].apply(assign_category)

print(df_boa.to_string())