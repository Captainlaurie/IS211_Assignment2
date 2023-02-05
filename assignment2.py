import argparse
import urllib.request
import logging
import datetime

#set up logger
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='Error processing line #%(linenum)s for ID #%(personId)')
logger = logging.getLogger('assignment2')


def downloadData(url):
    """
    Reads data from a URL and returns the data as a string

    :param url:
    :return:
    """
    # read the URL
    # pip install requests
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    # return the data
    return response

def processData(fileContent):
    """
    Parses data and returns a dictionary with id: (name, birthday)

    :param data:
    :return:
    """
    personData = {}
    
    # processing data
    lines = fileContent.split("\n")
    
    #set a counter to keep track of lines
    lineNum = 0    
    header = True
    
    for line in lines:
        # process each line
        # Skip the header
        if header:
            header = False
            continue

        # Skip blank lines
        if len(line) == 0:
            continue

        # Split into dictionary

        elements = line.split(",")
        personId = int(elements[0])
        name = elements[1]
        date_str = elements[2]

        try:
            birthday = datetime.datetime.strptime(date_str,'%d/%m/%Y')
            personData[personId] = (name, birthday)
            
        except ValueError:
          # Log the error
          logger.error("Error processing line #{} for ID #{}".format(lineNum, personId))
                
        lineNum += 1
                
    return personData


def displayPerson(personId, personData):
    """ Searches for a person using the ID entered by the user
        If no such ID number exists, prints a message that no user was found """
    
    if personId in personData:
        name, birthday = personData[personId]
        print("Person #{} is {} with a birthday of {}".format(personId, name, birthday.strftime("%Y %m %d")))
        
    else:
        print("No user found with that ID")


def main(url):
    
    """ Asks user to input ID number to look up a person """
    
    print(f"Running main with URL = {url}...")

    fileContent = downloadData(url)
    personData = processData(fileContent)

    while True:
        user_input = int(input("Enter an ID to look up or type 0 to exit: "))
        
        if user_input <= 0:
            break
        
        displayPerson(user_input, personData)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

