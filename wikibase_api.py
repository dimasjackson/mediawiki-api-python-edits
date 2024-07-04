import requests
import json

class WikibaseAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.csrf_token = None
        self.login()

    def _get_token(self, token_type):
        params = {
            "action": "query",
            "meta": "tokens",
            "type": token_type,
            "format": "json"
        }
        response = self.session.get(url=self.base_url, params=params)
        response.raise_for_status()
        return response.json()['query']['tokens'][f'{token_type}token']

    def login(self):
        login_token = self._get_token("login")
        login_params = {
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.password,
            "lgtoken": login_token,
            "format": "json"
        }
        response = self.session.post(self.base_url, data=login_params)
        response.raise_for_status()
        if response.json().get('login', {}).get('result') != 'Success':
            raise Exception("Login failed: ",response.json())
        self.csrf_token = self._get_token("csrf")

    def _edit_entity(self, entity_data, entity_type="item"):
        data = {
            "action": "wbeditentity",
            "format": "json",
            "token": self.csrf_token,
            **entity_data
        }
        response = self.session.post(self.base_url, data=data)
        response.raise_for_status()
        return response.json()

    def create_item(self, label, description, language="en"):
        entity_data = {
            "new": "item",
            "data": f'{{"labels": {{"{language}": {{"language": "{language}", "value": "{label}"}}}}, "descriptions": {{"{language}": {{"language": "{language}", "value": "{description}"}}}}}}'
        }
        return self._edit_entity(entity_data)

    def edit_item(self, item_id, label=None, description=None, language="en"):
        entity_data = {
            "id": item_id,
            "data": f'{{"labels": {{"{language}": {{"language": "{language}", "value": "{label}"}}}}, "descriptions": {{"{language}": {{"language": "{language}", "value": "{description}"}}}}}}'
        }
        return self._edit_entity(entity_data)

    def create_property(self, label, property_type, description, language="en"):
        entity_data = {
            "new": "property",
            "data": f'{{"labels": {{"{language}": {{"language": "{language}", "value": "{label}"}}}}, "datatype": "{property_type}", "descriptions": {{"{language}": {{"language": "{language}", "value": "{description}"}}}}}}'
        }
        return self._edit_entity(entity_data)

    def edit_property(self, property_id, label=None, property_type=None, language="en"):
        entity_data = {
            "id": property_id,
            "data": f'{{"labels": {{"{language}": {{"language": "{language}", "value": "{label}"}}}}, "datatype": "{property_type}"}}'
        }
        return self._edit_entity(entity_data)

    def add_statement(self, item_id, property_id, value, value_type):
        if value_type == "item":
            formatted_value = f'{{"entity-type":"item","numeric-id":{int(value)}}}'
        elif value_type == "string":
            formatted_value = f'"{value}"'
        elif value_type == "quantity":
            formatted_value = f'{{"amount":"+{value}","unit":"1"}}'
        elif value_type == "datetime":
            dict={"time": value, "timezone": 0, "before": 0, "after": 0, "precision": 11, "calendarmodel": "http://www.wikidata.org/entity/Q1985727"}
            formatted_value = json.dumps(dict)
        elif value_type == "coordinate":
            # Remove parentheses and split by comma
            coordinates_list = value.strip('()').split(',')
            # Convert strings to float and create a tuple
            coordinates_tuple = tuple(map(float, coordinates_list))
            dict={"latitude": coordinates_tuple[0], "longitude": coordinates_tuple[1], "precision": 0.000001, "globe": "http://www.wikidata.org/entity/Q2"}
            formatted_value = json.dumps(dict)
        else:
            raise ValueError("Unsupported value type")

        data = {
            "action": "wbcreateclaim",
            "format": "json",
            "entity": item_id,
            "snaktype": "value",
            "property": property_id,
            "value": formatted_value,
            "token": self.csrf_token
        }
        response = self.session.post(self.base_url, data=data)
        response.raise_for_status()
        return response.json()

    def search_entities(self, search, search_type="item"):
        params = {
            "action": "query",
            "list": "search",
            "srsearch": search,
            "format": "json",
            "srnamespace": "122" if search_type == "property" else "120",
        }
        response = self.session.get(url=self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    def opensearch(self, search):
        params = {
            "action": "opensearch",
            "search": search,
            "format": "json"
        }
        r = self.session.get(url=self.base_url, params=params)
        return r.json()