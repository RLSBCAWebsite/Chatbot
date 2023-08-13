from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from app.models import Register
from app.models import Messages
from app.models import Contact
import random
import json
import re
from django.contrib.staticfiles.finders import find

response_data = {}
# import random_responses

# Create your views here.


def openHome(request):
    return render(request, "web/index.html")


def openAboutus(request):
    return render(request, "web/aboutus.html")


def openContactus(request):
    return render(request, "web/contact.html")


def openFacilities(request):
    return render(request, "web/facilities.html")


def addRegister(request):
    if Register.objects.filter(rg_email=request.POST["txtEmail"]).count() == 0:
        Register.objects.create(
            rg_name=request.POST["txtName"],
            rg_mobile=request.POST["txtMobileNo"],
            rg_email=request.POST["txtEmail"],
            rg_password=request.POST["txtPassword"],
        )
        return HttpResponse(0)
    else:
        return HttpResponse(10)


def checkWebLogin(request):
    if (
        Register.objects.filter(
            rg_email=request.POST["txtEmail"], rg_password=request.POST["txtPassword"]
        ).count()
        == 0
    ):
        return HttpResponse(10)

    else:
        request.session["web_email"] = request.POST["txtEmail"]
        return HttpResponse(0)


def random_string():
    random_list = [
        "Please try writing something more descriptive.",
        "Oh! It appears you wrote something I don't understand yet",
        "Do you mind trying to rephrase that?",
        "I'm terribly sorry, I didn't quite catch that.",
        "I can't answer that yet, please try asking something else.",
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]


# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print("Heyy!How can I help you?\n")
        return json.load(bot_responses)


# Store JSON data
# file_path = find("bot.json")
# response_data = load_json(file_path)


def startChat(request):
    file_path = find("bot.json")
    if file_path:
        response_data = load_json(file_path)
        # print(response_data)
        get_response(request.POST["txtMsg"])
    else:
        response_data = {}

    return JsonResponse(response_data, safe=False)


# def get_response(request):
#     # print(input_string)
#     input_string = request.POST["txtMsg"]
#     file_path = find("bot.json")
#     response_data = load_json(file_path)
#     # print(response_data)
#     split_message = re.split(r"\s+|[,;?!.-]\s*", input_string.lower())
#     score_list = []

#     # Check all the responses
#     # print(response_data)
#     for response in response_data:
#         response_score = 0
#         required_score = 0
#         required_words = response["required_words"]

#         # Check if there are any required words
#         if required_words:
#             for word in split_message:
#                 if word in required_words:
#                     required_score += 1

#         # Amount of required words should match the required score
#         if required_score == len(required_words):
#             # print(required_score == len(required_words))
#             # Check each word the user has typed
#             # print(split_message)
#             for word in split_message:
#                 # If the word is in the response, add to the score

#                 if word in response["user_input"]:
#                     response_score += 1

#         # Add score to list
#         score_list.append(response_score)
#         # Debugging: Find the best phrase
#         # print(response_score, response["user_input"])

#     # Find the best response and return it if they're not all 0
#     best_response = max(score_list)
#     response_index = score_list.index(best_response)
#     # print(best_response);

#     # Check if input is empty
#     if input_string == "":
#         return "Please type something so we can chat and interact... :("

#     # If there is no good response, return a random one.
#     if best_response != 0:
#         print(response_data[response_index]["bot_response"])
#         return HttpResponse(response_data[response_index]["bot_response"])
#         # return response_data[response_index]["bot_response"]
#     else:
#         data = random_string()
#         return HttpResponse(data)


import re
from django.http import HttpResponse

# def get_response(request):
#     input_string = request.POST["txtMsg"]
#     file_path = find("bot.json")
#     response_data = load_json(file_path)
#     split_message = re.split(r"\s+|[,;?!.-]\s*", input_string.lower())
#     score_list = []

#     for response in response_data:
#         response_score = 0
#         required_score = 0
#         required_words = response["required_words"]

#         if required_words:
#             for word in split_message:
#                 if word in required_words:
#                     required_score += 1

#         if required_score == len(required_words):
#             for word in split_message:
#                 print(word);
#                 if word in response["user_input"]:
#                     response_score += 1

#         score_list.append(response_score)
#         print("Response:", response["bot_response"], "Score:", response_score)

#     best_response = max(score_list)
#     response_index = score_list.index(best_response)

#     if input_string == "":
#         return HttpResponse("Please type something so we can chat and interact... :(")

#     if best_response != 0:
#         # print("Selected Response:", response_data[response_index]["bot_response"])
#         return HttpResponse(response_data[response_index]["bot_response"])
#     else:
#         data = random_string()  # Make sure random_string() returns a valid response
#         # print("Random Response:", data)
#         return HttpResponse(data)

def get_response(request):
    input_string = request.POST.get("txtMsg", "")  # Using .get() to handle missing input

    if not input_string:  # Check if the input string is empty
        return HttpResponse("Please type something so we can chat and interact... :(")

    # Load JSON data
    file_path = find("bot.json")
    response_data = load_json(file_path)

    split_message = re.split(r"\s+|[,;?!.-]\s*", input_string.lower())
    max_response_score = 0  # Initialize max response score to find the best response
    best_bot_response = None  # Initialize the best bot response

    for response in response_data:
        response_score = 0
        required_words = response["required_words"]

        # Calculate required score based on required words
        required_score = sum(1 for word in split_message if word in required_words)

        if required_score == len(required_words):
            # Calculate response score based on user input words
            response_score = sum(1 for word in split_message if word in response["user_input"])

            if response_score > max_response_score:
                max_response_score = response_score
                best_bot_response = response["bot_response"]
    print(best_bot_response);
    if best_bot_response == None:
        best_bot_response = "";
    Messages.objects.create(
        ms_email=request.POST["userEmail"],
        ms_msg_user=input_string,
        ms_msg_bot=best_bot_response
    )
    if best_bot_response:
        return HttpResponse(best_bot_response)
    else:
        data = random_string()  # Make sure random_string() returns a valid response
        return HttpResponse(data)


def saveContact(request):
    Contact.objects.create(
        ct_name=request.POST["name"],
        ct_email=request.POST["email"],
        ct_subject=request.POST["subject"],
        ct_message=request.POST["message"]
    )

    return HttpResponse()


# while True:
#     user_input = input("You:")

#     print("Bot:", get_response(user_input))
