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
                print(f"Found item {item_title}.")
                print()
            else:
                print(f"FAILED: Item not found. Create item {item_label}, then import the JSON again.")
                break

            opensearch_result = wikibase.opensearch(item_title)
            item_label_found = opensearch_result[2][0].split(" (Q")[0]
            print(f"Label found: {item_label_found}")

            if item_label_found.lower() == item_label.lower():
                print(f"Item found: {item_title} {item_label_found}.")
                print()
            else:
                print(f"FAILED: Item {item_label} not equal to {item_label_found}. Create item {item_label}, then import the JSON again.")

            print("-----------------\n") 
            
            # Process properties
            for property in item['properties']:
                print()
                print(f"Searching for property [{property['label']}]...")

                property_search_results = wikibase.search_entities(property['label'], "property")
                print("Search results:")
                print(property_search_results)
                print()

                if property_search_results['query']['searchinfo']['totalhits'] != 0:
                    # Assuming the first result is the correct match
                    property_resultset = property_search_results['query']['search'][0]
                    property_title = property_resultset['title']
                    print(f"Found property: {property_title}.")
                    opensearch_result = wikibase.opensearch(property_title)
                    print("Label search results:")
                    print(opensearch_result)
                    property_label = opensearch_result[2][0].split(" (P")[0]
                    print(f"Label found: {property_label}")
                    print()

                    if property_label.lower() == property['label'].lower():
                        found_property_id = property_resultset['title']
                        datatype = property['datatype']

                        if datatype == 'item':
                            print(f"Searching for property value item {property['value']} ...")
                            search_results = wikibase.search_entities(property['value'])
                            property_item_resultset = search_results['query']['search'][0]
                            property_item_title = property_item_resultset['title']
                            print(f"Found item {property_item_title}.")
                            print()
                            print(f"Adding object property [{property['label']}] ({found_property_id}) with value [{property_item_title} {property['value']}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property_item_title[6:], 'item')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property['label']}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property['label']}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "string":
                            print(f"Adding string property [{property['label']}] ({found_property_id}) with value [{property['value']}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property['value'], 'string')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property['label']}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property['label']}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "datetime":
                            print(f"Adding datetime property [{property['label']}] ({found_property_id}) with value [{property['value']}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], str(property['value']), 'datetime')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property['label']}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property['label']}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "coordinates":
                            print(f"Adding global coordinates property [{property['label']}] ({found_property_id}) with value [{property['value']}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property['value'], 'coordinate')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property['label']}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property['label']}] ({found_property_id}) FAILED!")
                            print()

                        elif datatype == "quantity":
                            print(f"Adding quantity property [{property['label']}] ({found_property_id}) with value [{property['value']}] to item [{item_label_found}] ({item_title}).")
                            add_statement = wikibase.add_statement(item_title[5:], found_property_id[9:], property['value'], 'quantity')
                            print()
                            print(json.dumps(add_statement, indent=4))
                            if add_statement['success'] == 1:
                                print(f"STATEMENT [{property['label']}] ({found_property_id}) SUCCESFULLY ADDED!")
                            else:
                                print(f"ADD STATEMENT [{property['label']}] ({found_property_id}) FAILED!")
                            print()

                        else:
                            print(f"ADD STATEMENT [{property['label']}] ({found_property_id}) FAILED: Unknow datatype {datatype}. Datatype must be item, string, datetime, coordinates or quantity.")
                            print()

                        if 'qualifiers' in property:

                            for qualifier in property['qualifiers']:

                                print(f"Adding qualifier with property [{qualifier['property']}] and value [{qualifier['value']}] to statement [{property['label']}] ({found_property_id}) of item [{item_label_found}] ({item_title}).")
                                
                                item_qid = item_title.split(":")[1]
                                property_pid = found_property_id.split(":")[1]
                                statement = wikibase.get_statement_id(item_qid=item_qid, property_pid=property_pid)
                                claims = statement.get("claims", {}).get(property_pid, [])

                                if not claims:
                                    raise ValueError(f"No claims found for property {found_property_id} in item {item_title}: {statement}")
                                
                                qualifier_property_search = wikibase.search_entities(qualifier['property'], "property")
                                statement_id = statement['claims'][property_pid][0]['id']
                                # Assuming the first result is the correct match
                                qualifier_property_resultset = qualifier_property_search['query']['search'][0]
                                qualifier_property_title = qualifier_property_resultset['title']
                                qualifier_property_pid = qualifier_property_title.split(':')[1]

                                valuetype = qualifier['valueType']
                                if valuetype == 'item':

                                    print(f"Searching for qualifier property value item {qualifier['value']} ...")

                                    search_results = wikibase.search_entities(qualifier['value'])
                                    property_item_resultset = search_results['query']['search'][0]
                                    property_item_title = property_item_resultset['title']
                                    print(f"Found item {property_item_title}.")
                                    print()

                                    print(f"Adding object property [{qualifier['property']}] ({qualifier_property_pid}) with value [{property_item_title} {qualifier['value']}] to item [{item_label_found}] ({item_title}).")
                                    add_qualifier = wikibase.add_qualifier(statement_id, qualifier_property_pid, property_item_title[6:], 'item')
                                    print()
                                    print(json.dumps(add_qualifier, indent=4))
                                    if add_qualifier['success'] == 1:
                                        print(f"qualifier [{qualifier['property']}] ({qualifier_property_pid}) SUCCESFULLY ADDED!")
                                    else:
                                        print(f"ADD qualifier [{qualifier['property']}] ({qualifier_property_pid}) FAILED!")
                                    print()

                                elif valuetype == "string":
                                    print(f"Adding qualifier string property [{qualifier['property']}] ({qualifier_property_pid}) with value [{qualifier['value']}] to item [{item_label_found}] ({item_title}).")
                                    add_qualifier = wikibase.add_qualifier(statement_id, qualifier_property_pid, qualifier['value'], 'string')
                                    print()
                                    print(json.dumps(add_qualifier, indent=4))
                                    if add_qualifier['success'] == 1:
                                        print(f"qualifier [{qualifier['property']}] ({qualifier_property_pid}) SUCCESFULLY ADDED!")
                                    else:
                                        print(f"ADD qualifier [{qualifier['property']}] ({qualifier_property_pid}) FAILED!")
                                    print()

                                elif valuetype == "datetime":
                                    print(f"Adding qualifier datetime property [{qualifier['property']}] ({qualifier_property_pid}) with value [{qualifier['value']}] to item [{item_label_found}] ({item_title}).")
                                    add_qualifier = wikibase.add_qualifier(statement_id, qualifier_property_pid, str(qualifier['value']), 'datetime')
                                    print()
                                    print(json.dumps(add_qualifier, indent=4))
                                    if add_qualifier['success'] == 1:
                                        print(f"qualifier [{qualifier['property']}] ({qualifier_property_pid}) SUCCESFULLY ADDED!")
                                    else:
                                        print(f"ADD qualifier [{qualifier['property']}] ({qualifier_property_pid}) FAILED!")
                                    print()

                                elif valuetype == "coordinates":
                                    print(f"Adding qualifier global coordinates property [{qualifier['property']}] ({qualifier_property_pid}) with value [{qualifier['value']}] to item [{item_label_found}] ({item_title}).")
                                    add_qualifier = wikibase.add_qualifier(statement_id, qualifier_property_pid, qualifier['value'], 'coordinate')
                                    print()
                                    print(json.dumps(add_qualifier, indent=4))
                                    if add_qualifier['success'] == 1:
                                        print(f"qualifier [{qualifier['property']}] ({qualifier_property_pid}) SUCCESFULLY ADDED!")
                                    else:
                                        print(f"ADD qualifier [{qualifier['property']}] ({qualifier_property_pid}) FAILED!")
                                    print()

                                elif valuetype == "quantity":
                                    print(f"Adding qualifier quantity property [{qualifier['property']}] ({qualifier_property_pid}) with value [{qualifier['value']}] to item [{item_label_found}] ({item_title}).")
                                    add_qualifier = wikibase.add_qualifier(statement_id, qualifier_property_pid, qualifier['value'], 'quantity')
                                    print()
                                    print(json.dumps(add_qualifier, indent=4))
                                    if add_qualifier['success'] == 1:
                                        print(f"qualifier [{qualifier['property']}] ({qualifier_property_pid}) SUCCESFULLY ADDED!")
                                    else:
                                        print(f"ADD qualifier [{qualifier['property']}] ({qualifier_property_pid}) FAILED!")
                                    print()

                                else:
                                    print(f"ADD qualifier [{qualifier['property']}] ({qualifier_property_pid}) FAILED: Unknow datatype {datatype}. Datatype must be item, string, datetime, coordinates or quantity.")
                                    print()

                                print()
                                print(json.dumps(add_qualifier, indent=4))

                                if add_qualifier['success'] == 1:
                                    print(f"QUALIFIER [{qualifier['property']}] ({found_property_id}) SUCCESFULLY ADDED!")
                                else:
                                    print(f"ADD QUALIFIER [{qualifier['property']}] ({found_property_id}) FAILED!")
                                print()

                    else:
                        print(f"ADD STATEMENT FAILED: Property {property['label']} not equal to {property_label}.")
                        print()
                else:
                    print(f"ADD STATEMENT FAILED: Property {property['label']} not found in Wikibase.")
                    print() 
                print("*********************\n") 

    print("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON and add statements to Wikibase.")
    parser.add_argument("--url", required=True, help="Wikibase API URL e.g. http://mywiki/w/api.php")
    parser.add_argument("--bot_user", required=True, help="Wikibase bot user e. g. Admin@MyBot")
    parser.add_argument("--bot_password", required=True, help="Wikibase bot password")
    parser.add_argument("--json_file", required=True, help="JSON file path")

    args = parser.parse_args()

    main(args.url, args.bot_user, args.bot_password, args.json_file)
