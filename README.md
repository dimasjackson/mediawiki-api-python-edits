# mediawiki-api-python-edits
Create, edit and modify entities and properties in your wiki using MediaWiki API and python. Automate the process of adding claims to your local wiki/wikibase instance itens using CSV files.

## Create Items and Properties

Use the script `create_item_json.py` to create items from a JSON file like the example in `create_item.json`. To run the script, execute the following line in Terminal/CMD:
```
python create_item_json.py --url http://mywiki/w/api.php --bot_user user@botname --bot_password abcd123456 --json_file create_item.json
```

Supported datatypes for properties are
* string: Represents simple text.
* monolingual-text: Text with an associated language tag.
* external-identifier: Identifiers that link to external databases.
* URL: Links to web resources.
* quantity: Numerical values, optionally with units.
* time: Points in time, dates, or timespans.
* globe-coordinate: Geographic coordinates.
* wkibase-item: Links to other Wikibase items.
* property: Links to Wikibase properties.
* commons-media: Links to media files on Wikimedia Commons.
* geoshape: Geospatial shapes.
* tabular-data: Links to tabular datasets.
* math: Mathematical expressions in LaTeX format.

## Importing JSON file statements
The script `import_json.py` add properties to existing items in your Wikibase instance. The JSON must follow the schema in `data.json` example. To run the script, execute the following line in Terminal/CMD:
```
python import_json.py --url http://mywiki/w/api.php --bot_user user@botname --bot_password abcd123456 --json_file data.json
```

## Importing CSV statements

Run the following script to import a CSV file with properties. The first column must be called 'label' and contain the item's labels. It is necessary to create all items in column 'label' before running the script. The other column names must be the properties that you want to add to each item.

The supported datatypes are:

* string (e. g. "Krzyżacy")
* item (e. g. "Universe")
* datetime (e. g. "+2000-01-31T00:00:00Z")
    
    **Warning**: the '+' sign is required and hour, minutes and secconds must be zero, the Wikibase property type must be 'Point in time'

* quantity (e. g. 1.75)
* coordinates (e. g. "(40.748433,-73.985656)")

```
python import_csv.py --url http://mywiki/w/api.php --bot_user user@botname --bot_password abcd123456 --csv_file data.csv --datatypes "name:string;email address:string;date of birth:datetime;instance of:item;coordinates location:coordinates;weight:quantity"
```

See `usage_example.ipynb` for more usecases.

This is a preliminary version, contributions are welcome!
