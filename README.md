# nerevuChallenge

## How to run the API

If you do not have experience with virtual environments and/or Flask: you should first make a python3 virtual environment after cloning the git repo and cd-ing into the repo. The command to do so is

python3 -m venv name_of_your_virtualenvironment
source name_of_your_virtualenvironment/bin/activate

That second command activates your virtual environment in the terminal you use the command. After that, you should install all of the packages in the requirements.txt file using pip:

pip install -r requirements.txt

Now, you can type in "flask run" into the terminal. Header over to a browser and type in http://localhost:5000/holidays_2?holidayType=Federal%20Holiday

## Why are there two CSVs?

The CSV with "copypaste" in its name was created by copy and pasting the holiday data from timeanddate.com into a google spreadsheet. I think downloaded this as a CSV file. I copied-and-pasted the data because my attempts at using their API and my attempts at web-scraping were failing. I wanted to at least complete the other portions of the coding challenge before coming back. I came back and fixed/created a function that generates a clean CSV.
