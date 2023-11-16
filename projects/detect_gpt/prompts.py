prompt_object = '''
Respond in a loadable JSON format.
Task:
Look at the given image and fill the JSON value with given instruction. 
JSON object has two keys named "description", "objects". 
Please fill the "description" value with the one sentence expression as detail as you can.
Then, please fill the "objects" value with the list of objects you can find in the given image.
Response Format:
{
"description": str,
"objects": list
}
* Make sure the JSON is loadable with json.loads().
    '''

prompt_dish = '''
Respond in a loadable JSON format.
Task:
Look at the given image and fill the JSON value with given instruction. 
JSON object has two keys named "description", "foods". 
Please fill the "description" value with the one sentence expression as detail as you can.
Then, please fill the "foods" value with the list of dishes you can find in the given image.
Response Format:
{
"description": str,
"foods": list
}
* Make sure the JSON is loadable with json.loads().
    '''

prompt_dish_multiple = '''
Respond in a loadable JSON format.
Task:
Look at the given image and fill the JSON value with given instruction. 
JSON object has two keys named "description", "foods". 
Please fill the "description" value with the one sentence expression as detail as you can.
Then, please fill the "foods" value with the list of "dish" object you can find in the given image.
Each "dish" object is a dictionary with two keys: "name", "count".
If you find same category of multiple dishes, please fill "count" value as a number of objects.
For example, if you find two hamburgers in the given image, "dish" object should be {"name":"hamburger", "count":2}.
Response Format:
{
"description": str,
"foods": list
}
* Make sure the JSON is loadable with json.loads().
    '''
