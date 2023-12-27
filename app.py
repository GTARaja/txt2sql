import pathlib
import textwrap
import cx_Oracle

import google.generativeai as genai

# Used to securely store your API key
#from google.colab import userdata
import csv
from IPython.display import display
from IPython.display import Markdown

# Function to read the CSV file and create a dictionary
def read_csv(file_path):
    data_dict = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                data_dict[row[0]] = row[1]
    return data_dict
# Function to get user input and fetch the corresponding value
def fetch_dml(data_dict, user_input):

  for user_item in user_input:
    # Split each substring and match with the dictionary keys
    user_items = user_item.split()
    for item in user_items:
      dml_value = data_dict.get(item)
      if dml_value:
        dml_statements=dml_value

  return dml_statements
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
#GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')

genai.configure(api_key='Enter your API Key')

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
model = genai.GenerativeModel('gemini-pro')
csv_file_path = "venv/dml.csv"
#inp = input('Enter Statement for which SQL Query needs to be generated and executed')
data_dictionary = read_csv(csv_file_path)
# Get user input and fetch the corresponding value
user_input1 = input("Enter Statement for which SQL Query needs to be generated and executed").strip()
user_input=user_input1.split()
# Fetch the corresponding values for each substring
result = fetch_dml(data_dictionary, user_input)
print(result)
response = model.generate_content("consider the DML "+result+ "provide only the oracle sql query without newline character to" + user_input1 +"?")
#response = model.generate_content('{"menu": {  "id": "file",  "value": "File",  "popup": {  "menuitem": [  {"value": "New", "onclick": "CreateDoc()"},  {"value": "Open", "onclick": "OpenDoc()"},  {"value": "Save", "onclick": "SaveDoc()"}  ]  }  }} based on this json create some sample json for testing')
print(response.text)
to_markdown(response.text)
#print(response.candidates)
my_new_string = response.text.replace("```", "")
my_new_string1 = my_new_string.replace("```sql", "")
#print(my_new_string1)
try:
  con = cx_Oracle.connect('SYSTEM/pic16f84@localhost:1521/xe')

except cx_Oracle.DatabaseError as er:
  print('There is an error in the Oracle database:', er)

else:
  try:
    cur = con.cursor()

    # fetchall() is used to fetch all records from result set
    cur.execute(my_new_string1)
    rows = cur.fetchall()
    print(rows)

    # fetchmany(int) is used to fetch limited number of records from result set based on integer argument passed in it
    #cur.execute('select * from TransferDetails')
    #rows = cur.fetchmany(3)
    #print(rows)

    # fetchone() is used fetch one record from top of the result set
    #cur.execute('select * from TransferDetails')
    #rows = cur.fetchone()
    #print(rows)

  except cx_Oracle.DatabaseError as er:
    print('There is an error in the Oracle database:', er)

  except Exception as er:
    print('Error:' + str(er))

  finally:
    if cur:
      cur.close()

finally:
  if con:
    con.close()
