import json

def read_schema():
    new_schema = {}
    with open('command_schema1.json', 'r') as f:
        data = json.load(f)

        for i in data:
            print(i['tool_name'])
            new_schema[i['tool_name']] = i

    with open('new_tools_schema.json', 'w') as f:
        json.dump(new_schema, f, indent=4)

read_schema()