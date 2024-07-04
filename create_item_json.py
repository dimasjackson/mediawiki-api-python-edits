import json
import argparse
from wikibase_api import WikibaseAPI

def main(url, bot_user, bot_password, json_file):
    # Initialize the WikibaseAPI
    wikibase = WikibaseAPI(url, bot_user, bot_password)

    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        for item in data:
            item_label = item['label']
       
            # Search for an item by label
            print()
            print(f"Searching for item {item_label} ...")
            search_results = wikibase.search_entities(item_label)

            if search_results['query']['searchinfo']['totalhits'] != 0:
                item_resultset = search_results['query']['search'][0]
                item_title = item_resultset['title']
                print(f"Found item {item_title}. The item/property {item_label} already exists.")
                break
            else:
                print(f"Item not found. Creating item {item_label}:")

            if item['type'] == 'item':
                create_item = wikibase.create_item(item_label, item['description'], item['language'])
                if create_item['success'] == 1:
                    print(f"Item {item_label} ({create_item['entity']['id']}) successfully created!")
                print()
            elif item['type'] == 'property':
                create_property = wikibase.create_property(item_label, item['propertyType'], item['description'], item['language'])
                if create_property['success'] == 1:
                    print(f"Property {item_label} ({create_property['entity']['id']}) successfully created!")
                print()
            else:
                print(f"FAILED: item/property {item_label} can't be created. Type must be \'item\' or \'property\'.")

            print("-----------------\n") 
            
    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON and add statements to Wikibase.")
    parser.add_argument("--url", required=True, help="Wikibase API URL e.g. http://mywiki/w/api.php")
    parser.add_argument("--bot_user", required=True, help="Wikibase bot user e. g. Admin@MyBot")
    parser.add_argument("--bot_password", required=True, help="Wikibase bot password")
    parser.add_argument("--json_file", required=True, help="JSON file path")

    args = parser.parse_args()

    main(args.url, args.bot_user, args.bot_password, args.json_file)
