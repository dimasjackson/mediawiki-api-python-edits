import csv
import argparse
import json
from wikibase_api import WikibaseAPI

def main(url, bot_user, bot_password, csv_file, datatypes):
    # Initialize the WikibaseAPI
    wikibase = WikibaseAPI(url, bot_user, bot_password)

    # Read the CSV file
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            item_label = row.pop('label')
       
            # Search for an item by label
            print()
            print(f"Searching for item {item_label} ...")
            search_results = wikibase.search_entities(item_label)

            if search_results['query']['searchinfo']['totalhits'] != 0:
                item_resultset = search_results['query']['search'][0]
                item_title = item_resultset['title']
                print(f"Found item {item_title}.")
                print()
            else:
                print(f"FAILED: Item not found. Create item {item_label}, then import the CSV again.")
                break

            opensearch_result = wikibase.opensearch(item_title)
            item_label_found = opensearch_result[2][0].split(" (Q")[0]
            print(f"Label found: {item_label_found}")

            if item_label_found.lower() == item_label.lower():
                print(f"Item found: {item_title} {item_label_found}.")
                print()
            else:
                print(f"FAILED: ITEM {item_label} NOT FOUND AND CANNOT BE CREATED")

            print("-----------------\n") 
            
            # Process properties
            for property_name, property_value in row.items():
                print()
                print(f"Searching for property [{property_name}]...")

                property_search_results = wikibase.search_entities(property_name, "property")
                print("Search results:")
                print(property_search_results)
                print()

                if property_search_results['query']['searchinfo']['totalhits'] != 0:
                    property_resultset = property_search_results['query']['search'][0]
                    property_title = property_resultset['title']
                    print(f"Found property: {property_title}.")
                    opensearch_result = wikibase.opensearch(property_title)
                    print("Label search results:")
                    print(opensearch_result)
                    property_label = opensearch_result[2][0].split(" (P")[0]
                    print(f"Label found: {property_label}")
                    print()

                    if property_label.lower() == property_name.lower():
                        found_property_id = property_resultset['title']
                        datatype = datatypes.get(property_name)

                        if datatype == 'item':
                            print(f"Searching for property value item {property_value} ...")
                            search_results = wikibase.search_entities(property_value)
                            property_item_resultset = search_results['query']['search'][0]
                            property_item_title = property_item_resultset['title']
                            print(f"Found item {property_item_title}.")
                            print()
                            print(f"Adding object property [{property_name}] ({found_property_id}) with value [{property_item_title} {property_value}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property_item_title[6:], 'item')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property_name}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property_name}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "string":
                            print(f"Adding string property [{property_name}] ({found_property_id}) with value [{property_value}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property_value, 'string')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property_name}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property_name}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "datetime":
                            print(f"Adding datetime property [{property_name}] ({found_property_id}) with value [{property_value}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], str(property_value), 'datetime')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property_name}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property_name}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "coordinates":
                            print(f"Adding global coordinates property [{property_name}] ({found_property_id}) with value [{property_value}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property_value, 'coordinate')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property_name}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property_name}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "quantity":
                            print(f"Adding quantity property [{property_name}] ({found_property_id}) with value [{property_value}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property_value, 'quantity')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property_name}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property_name}] ({found_property_id}) FAILED!")
                            print()

                        else:
                            print(f"ADD STATEMENT [{property_name}] ({found_property_id}) FAILED: Unknow datatype. Datatype must be item, string, datetime, coordinates or quantity.")
                            print()
                    else:
                        print(f"ADD STATEMENT FAILED: Property {property_name} not equal to {property_label}.")
                        print()
                else:
                    print(f"ADD STATEMENT FAILED: Property {property_name} not found in Wikibase.")
                    print() 
                print("*********************\n") 

    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV and add statements to Wikibase.")
    parser.add_argument("--url", required=True, help="Wikibase API URL e. g. http://mywiki/w/api.php")
    parser.add_argument("--bot_user", required=True, help="Wikibase bot user")
    parser.add_argument("--bot_password", required=True, help="Wikibase bot password")
    parser.add_argument("--csv_file", required=True, help="CSV file path")
    parser.add_argument("--datatypes", required=True, type=str, help="semicolon separated list of datatypes for CSV columns e.g. \"instance of:item;coordinate location:coordinate;date of birth:datetime\"")

    args = parser.parse_args()
    
    # Convert datatypes string to dictionary
    datatypes = {}
    for dtype in args.datatypes.split(";"):
        prop, dtype = dtype.split(":")
        datatypes[prop] = dtype

    main(args.url, args.bot_user, args.bot_password, args.csv_file, datatypes)
