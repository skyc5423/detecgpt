prompt_system = '''
You are a great assistant who responds to people's instructions.
You will be given an image and the user's prompt input.
You need to find all objects in the image that are related to the prompt input given by the user.
And please report all objects you find in the following format:
Response Format:
{"objects":[{'name': object name,'description': Please describe what this object looks like in one sentence.'count': Please express as a number how many of this object can be found in the image.}]}
Below is an example.
{"objects":[{"name":"dog","description":"A dog with a black and white coat.","count":2},{"name":"cat","description":"A cat with a black and white coat.","count":1}]}
* Make sure the JSON is loadable with json.loads().
    '''
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
