# load data from student json
with open('./students.json') as user_file:
    file_contents = user_file.read()

parsed_json = json.loads(json.loads(file_contents))

print(parsed_json)