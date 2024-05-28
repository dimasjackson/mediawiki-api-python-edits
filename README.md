# mediawiki-api-python-edits
Create, edit and modify entities and properties in your wiki using MediaWiki API and python. Automate the process of adding claims to your local wiki/wikibase instance itens using CSV files.

## Importing CSV statements

Run the following script to import a CSV file with properties. The first row must be called 'label' and contain the item's labels. It is necessary to create all items in column 'label' before running the script. The other column names must be the properties that you want to add to each item.

The supported datatypes are:

* string (e. g. "Krzyżacy")
* item (e. g. "Universe")
* datetime (e. g. "+2000-01-03T00:00:00Z" warning: hour, minutes and secconds must be zero) 
* quantity (e. g. 1.75)
* coordinates (e. g. "(40.748433,-73.985656)")

```
py import_csv.py --url http://mywiki/w/api.php --bot_user user@botname --bot_password abcd123456 --csv_file data.csv --datatypes "name:string;email address:string;date of birth:datetime;instance of:item;coordenadinates location:coordinates;weight:quantity"
```

See `usage_example.ipynb` for more usecases.

This is a preliminary version, contributions are welcome!
