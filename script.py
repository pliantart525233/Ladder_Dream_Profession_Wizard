#imports
import anthropic
import sys
import io

# Ensure stdout is using UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize an Anthropic client
client = anthropic.Anthropic()

#decide major

def major_suggestion(country, grades, prompt, word_count):
    #Defining a prompt
    prompt = "What major should I do?"
    #Create the message
    message = client.messages.create(
        #Model
        model="claude-3-haiku-20240307",
        #Maximum amount of tokens
        max_tokens=1000,
        temperature=0,
        #Message sent to the system
        system="You are trying to help students to get into university at " + country + " and decide which major they will do." 
        +" Help them depending on the prompt. Use less than "+ str(word_count * 2) +" words. Don't tell them you are using less than "+ str(word_count * 2) +" words. The classes that they "
         + "took and their grader are: " 
        + str(grades) + ". Also consider the impact of EVERY grade, including the average and bad ones.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        #Pre-built message or message chosen/written by the user
                        "text": prompt
                    }
                ]
            }
        ]
    )
    #print(message.content)
    return message.content

#subject = "Political Science"
#country = "US"

#get_tip(country, subject)

#tips

def get_tip(country, subject, prompt, word_count):
    #Defining a prompt
    prompt = "What do I need to get into a good university for " +subject+"?"
    #Create the message
    message = client.messages.create(
        #Create the message
        model="claude-3-haiku-20240307",
        #Maximum amount of tokens
        max_tokens=1000,
        temperature=0,
        #Message sent to the system
        system="You are trying to help students to get into university at " + country + " in " + subject + ". Help them depending on the prompt. Use less than "+ str(word_count) +" words. Don't tell them you are using less than "+ word_count +" words",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        #Pre-built message or message chosen/written by the user
                        "text": prompt
                    }
                ]
            }
        ]
    )
    #print(message.content)
    return message.content

#subject = "Political Science"
#country = "US"

#get_tip(country, subject)

#check universities based on grades

def uni_based_grades(country, GPA, subject, prompt, word_count):
    #Defining the prompt
    prompt = "answer please"
    # Create the message
    message = client.messages.create(
        #Choosing the model
        model="claude-3-haiku-20240307",
        #Limit of tokens to use
        max_tokens=1000,
        temperature=0,
        #Message sent to the system
        system="You are trying to help students to get into university. Which " + country+ " universities they can get into with their GPA ("+str(GPA)+") for " + subject + "? Use less than "+ str(word_count) +" words",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        #Pre-built message or message chosen/written by the user
                        "text": prompt
                    }
                ]
            }
        ]
    )
    #print(message.content)
    return message.content
#GPA = 3.5
#subject = "Computer Science"
#country = "United States"

#uni_based_grades(country, GPA, subject)

#extra curricular stuff
def uni_extra(country, subject, prompt, word_count):
    #Defining the prompt
    prompt = "answer please"
    # Create the message
    message = client.messages.create(
        #Choosing the model
        model="claude-3-haiku-20240307",
        #Limit of tokens to use
        max_tokens=1000,
        temperature=0,
        #Message sent to the system
        system="You are trying to help students to get into university. Which extra-curricular activities they should do to get into " + subject + " at " + country + ". Use less than "+ str(word_count) +" words",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        #Pre-built message or message chosen/written by the user
                        "text": prompt
                    }
                ]
            }
        ]
    )
    #print(message.content)
    return message.content

#country = "Switzerland"
#text = "I have a GPA of 3.5 and I am interested in studying Computer Science"
#subject = "Business"
#uni_based_grades(country, subject)

#Custom Question
def custom_as_example(country, grades, recalculated_GPA, subject, prompt, system_message, word_count):
    #Defining the prompt
    system_message = "You are trying to help a student to choose their university and major. Only name the major, possible minor and university. Don't give any other information. ONLY name two/three major, two/three possible minor and two/three university. Don't give any other information. Mention the countries the universities are from"
    prompt = "I am interested in Arts and humanities, and have no interest in STEM. I want to go to "+ country + "."
    # Create the message
    message = client.messages.create(
        #Choosing the model
        model="claude-3-haiku-20240307",
        #Limit of tokens to use
        max_tokens=100,
        temperature=0,
        #Message sent to the system
        system= system_message,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        #Pre-built message or message chosen/written by the user
                        "text": prompt
                    }
                ]
            }
        ]
    )
    #print(message.content)
    return message.content

#country = "Switzerland"
#text = "I have a GPA of 3.5 and I am interested in studying Computer Science"
#subject = "Business"
#uni_based_grades(country, subject)

GPA = 0.0
subject = ""
country = ""
prompt = ""
system_message = ""
word_count = 50

#Pre built grades for example
grades = {"Biology":[98], "Math":[95], "Computer Science":[97], "English":[99], "Physics":[78], "Chemistry":[80], "Music":[100], "History":[68], "Arts":[98]}
#print(grades)

#calculate GPA
for i in range(len(grades)):
    GPA += grades[list(grades.keys())[i]][0]

GPA /= len(grades)
GPA = round(GPA, 2)

grade_reference = {
  94: 4.0,
  90: 3.7,
  87: 3.3,
  83: 3.0,
  80: 2.7,
  77: 2.3,
  73: 2.0,
  70: 1.7,
  67: 1.3,
  65: 1.0,
  0: 0.0
  #Source for grade reference: https://bigfuture.collegeboard.org/plan-for-college/get-started/how-to-convert-gpa-4.0-scale
}

#Get the GPA in 4.0 scale format
for item in grade_reference:
  if GPA >= item:
    recalculated_GPA = grade_reference[item]
    break
#print(recalculated_GPA)

#print("Your current GPA is: ", recalculated_GPA)

# Ask user for input to select the correct information needed and to choose the type of help they want (major, tip, possible, extra)
#country = input("What country do you want to do college?")

#subject = input("What subject do you want to study?")

#question = input("What do you need help with?")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            question = sys.argv[1]
            country = sys.argv[2]
            subject = sys.argv[3]

            # Call the appropriate function based on the user's input to get the suggested information
            if question == "major":
                result = major_suggestion(country, grades, prompt, word_count)
            elif question == "tip":
                result = get_tip(country, subject, prompt, word_count)
            elif question =="possible":
                result = uni_based_grades(country, recalculated_GPA, subject, prompt, word_count)
            elif question =="custom":
                result = custom_as_example(country, grades, recalculated_GPA, subject, prompt, system_message, word_count)
            else:
                result = uni_extra(country, subject, prompt, word_count)

            print(str(result))  

        else:
            print("No input string provided.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)



