import re
import sqlite3

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from database import (
    email_exists,
    find_registration,
    initialize_database,
    save_to_database,
)
from intent_model import predict_intent

# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()


# ==========================================
# NLTK
# ==========================================

lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    """Convert text to lowercase, tokenize, and lemmatize."""
    text = text.lower()
    tokens = word_tokenize(text)

    return [lemmatizer.lemmatize(token) for token in tokens]


# ==========================================
# USER DATA
# ==========================================

userdata = {
    "registration_id": "",
    "name": "",
    "email": "",
    "field": "",
    "experience": "",
}


# ==========================================
# RESET USER DATA
# ==========================================


def reset_userdata():
    global userdata

    userdata = {
        "registration_id": "",
        "name": "",
        "email": "",
        "field": "",
        "experience": "",
    }


# ==========================================
# GENERATE REGISTRATION ID
# ==========================================


def generate_registration_id():
    conn = sqlite3.connect("data/registrations.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT registration_id
        FROM registrations
        WHERE registration_id LIKE 'REG%'
        ORDER BY CAST(
            SUBSTR(registration_id, 4) AS INTEGER
        ) DESC
        LIMIT 1
        """)

    result = cursor.fetchone()
    conn.close()

    if result:
        last_id = result[0]
        number = int(last_id.replace("REG", ""))
        next_number = number + 1
    else:
        next_number = 1

    return f"REG{next_number:04d}"


# ==========================================
# EXTRACT NAME
# ==========================================


def extract_name(user_input):
    patterns = [
        r"(?:my name is|i am|i'm)\s+([a-zA-Z ]+)",
        r"(?:name is)\s+([a-zA-Z ]+)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            user_input,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

    return None


# ==========================================
# EXTRACT EMAIL
# ==========================================


def extract_email(user_input):
    pattern = r"[a-zA-Z0-9.%+-]+" r"@[a-zA-Z0-9.-]+" r"\.[a-zA-Z]{2,}"

    match = re.search(pattern, user_input)

    if match:
        return match.group()

    return None


# ==========================================
# VALIDATE EMAIL
# ==========================================


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9.%+-]+" r"@[a-zA-Z0-9.-]+" r"\.[a-zA-Z]{2,}$"

    return re.match(pattern, email) is not None


# ==========================================
# EXTRACT FIELD
# ==========================================


def extract_field(user_input):
    patterns = [
        r"(?:i study|i'm studying|i am studying|" r"my field is|field is)\s+(.+)"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            user_input,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

    return None


# ==========================================
# EXTRACT EXPERIENCE
# ==========================================


def extract_experience(user_input):
    patterns = [
        r"(?:i am a|i'm a|i am|i'm)\s+" r"(beginner|intermediate|advanced|expert)",
        r"(?:my experience is|experience level is)\s+(.+)",
        r"(?:i have)\s+(.+?)\s+(?:experience)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            user_input,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

    return None


# ==========================================
# EXTRACT REGISTRATION ID
# ==========================================


def extract_registration_id(user_input):
    pattern = r"\bREG\d{4}\b"

    match = re.search(
        pattern,
        user_input.upper(),
    )

    if match:
        return match.group()

    return None


# ==========================================
# DISPLAY REGISTRATION SUMMARY
# ==========================================


def show_summary():
    print("\n======================================")
    print("       REGISTRATION SUMMARY")
    print("======================================")

    print(f"Registration ID: " f"{userdata['registration_id']}")

    print(f"Name:       " f"{userdata['name']}")

    print(f"Email:      " f"{userdata['email']}")

    print(f"Field:      " f"{userdata['field']}")

    print(f"Experience: " f"{userdata['experience']}")

    print("======================================")

    print("Registration information collected successfully!")


# ==========================================
# DISPLAY FOUND REGISTRATION
# ==========================================


def show_registration(registration):
    print("\n======================================")
    print("       REGISTRATION FOUND")
    print("======================================")

    print(f"Registration ID: " f"{registration['registration_id']}")

    print(f"Name:       " f"{registration['name']}")

    print(f"Email:      " f"{registration['email']}")

    print(f"Field:      " f"{registration['field']}")

    print(f"Experience: " f"{registration['experience']}")

    print("======================================")


# ==========================================
# HANDLE CHECK REGISTRATION
# ==========================================


def handle_check_registration(user_input):
    registration_id = extract_registration_id(user_input)

    if not registration_id:
        print("Assistant: Please provide your " "registration ID, for example REG0005.")
        return False

    registration = find_registration(registration_id)

    if registration:
        show_registration(registration)
    else:
        print(f"Assistant: No registration found " f"with ID {registration_id}.")

    return True


# ==========================================
# HELP
# ==========================================


def show_help():
    print("Assistant: I can help you with the following:\n")

    print("1. Register for an internship")
    print("2. Check your registration details")
    print("3. Cancel registration")
    print("4. Restart registration\n")

    print("Available commands:")
    print("• I want to register")
    print("• Show my registration details")
    print("• Cancel")
    print("• Restart")
    print("• Exit")


# ==========================================
# MAIN CHATBOT
# ==========================================

print("======================================")
print("     AI REGISTRATION ASSISTANT")
print("======================================")

print("Type 'help' for available commands.")

print("Type 'exit' to stop the chatbot.\n")


conversation_state = "start"


# ==========================================
# CHATBOT LOOP
# ==========================================

while True:

    user_input = input("You: ").strip()

    # ======================================
    # EMPTY INPUT
    # ======================================

    if not user_input:
        print("Assistant: Please enter something.")
        continue

    # ======================================
    # GLOBAL HELP COMMAND
    # ======================================

    if user_input.lower() == "help":
        show_help()
        continue

    # ======================================
    # GLOBAL CANCEL COMMAND
    # ======================================

    if user_input.lower() == "cancel":

        reset_userdata()

        conversation_state = "start"

        print("Assistant: Registration cancelled.")

        print(
            "Assistant: You can type " "'I want to register' anytime " "to start again."
        )

        continue

    # ======================================
    # GLOBAL RESTART COMMAND
    # ======================================

    if user_input.lower() == "restart":

        reset_userdata()

        conversation_state = "name"

        print("Assistant: Registration restarted.")

        print("Assistant: Please provide " "your full name.")

        continue

    # ======================================
    # EXIT
    # ======================================

    if user_input.lower() == "exit":

        print(
            "Assistant: Thank you for using "
            "the AI Registration Assistant. "
            "Goodbye!"
        )

        break

    # ======================================
    # START STATE
    # ======================================

    if conversation_state == "start":

        intent = predict_intent(user_input)

        # ==================================
        # CHECK REGISTRATION
        # ==================================

        if intent == "check_registration":

            registration_id = extract_registration_id(user_input)

            if registration_id:

                handle_check_registration(user_input)

            else:

                print(
                    "Assistant: Please provide "
                    "your registration ID, "
                    "for example REG0005."
                )

                conversation_state = "registration_id"

        # ==================================
        # REGISTER
        # ==================================

        elif intent == "register":

            reset_userdata()

            print("Assistant: Great! I'll help you " "register for the internship.")

            print("Assistant: Please provide " "your full name.")

            conversation_state = "name"

        # ==================================
        # GREETING
        # ==================================

        elif intent == "greeting":

            print("Assistant: Hello! Welcome to " "the AI Registration Assistant.")

            print("Assistant: How can I help you?")

        # ==================================
        # THANK YOU
        # ==================================

        elif intent == "thank_you":

            print("Assistant: You're welcome!")

        # ==================================
        # HELP INTENT
        # ==================================

        elif intent == "help":

            show_help()

        # ==================================
        # UNKNOWN
        # ==================================

        else:

            print("Assistant: I'm not sure I " "understood.")

            print("Assistant: Could you please " "rephrase your question?")

    # ======================================
    # REGISTRATION ID STATE
    # ======================================

    elif conversation_state == "registration_id":

        registration_id = extract_registration_id(user_input)

        if registration_id:

            registration = find_registration(registration_id)

            if registration:

                show_registration(registration)

            else:

                print(
                    f"Assistant: No registration "
                    f"found with ID "
                    f"{registration_id}."
                )

            conversation_state = "start"

        else:

            print("Assistant: Please enter a valid " "registration ID such as REG0005.")

    # ======================================
    # NAME STATE
    # ======================================

    elif conversation_state == "name":

        name = extract_name(user_input)

        if name:

            userdata["name"] = name

        elif re.fullmatch(
            r"[a-zA-Z ]+",
            user_input,
        ):

            words = user_input.split()

            invalid_phrases = [
                "i need help",
                "i need support",
                "i want to register",
                "hello",
                "hi",
                "hey",
                "thanks",
                "thank you",
            ]

            if user_input.lower() in invalid_phrases:

                print("Assistant: Please enter " "your actual full name.")

                continue

            if len(words) > 4:

                print("Assistant: Please enter " "a valid name.")

                continue

            userdata["name"] = user_input.strip()

        else:

            print("Assistant: Please enter " "a valid name.")

            continue

        print(f"Assistant: Nice to meet you, " f"{userdata['name']}!")

        print("Assistant: Please provide " "your email address.")

        conversation_state = "email"

    # ======================================
    # EMAIL STATE
    # ======================================

    elif conversation_state == "email":

        email = extract_email(user_input)

        if email and is_valid_email(email):

            if email_exists(email):

                print("Assistant: This email is " "already registered.")

                print("Assistant: Please use a " "different email address.")

                continue

            userdata["email"] = email

            print(f"Assistant: Thank you! Your " f"email {email} has been recorded.")

            print("Assistant: Now, please tell me " "your field of study.")

            conversation_state = "field"

        else:

            print("Assistant: That email address " "is not valid.")

            print("Assistant: Please enter a valid " "email address.")

    # ======================================
    # FIELD STATE
    # ======================================

    elif conversation_state == "field":

        field = extract_field(user_input)

        if not field:
            field = user_input.strip()

        if len(field) < 2:

            print("Assistant: Please enter your " "field of study.")

            continue

        userdata["field"] = field

        print(f"Assistant: Great! You're studying " f"{field}.")

        print("Assistant: Now, tell me about " "your programming experience.")

        conversation_state = "experience"

    # ======================================
    # EXPERIENCE STATE
    # ======================================

    elif conversation_state == "experience":

        experience = extract_experience(user_input)

        if not experience:
            experience = user_input.strip()

        if len(experience) < 2:

            print("Assistant: Please describe " "your programming experience.")

            continue

        userdata["experience"] = experience

        # ==================================
        # GENERATE REGISTRATION ID
        # ==================================

        userdata["registration_id"] = generate_registration_id()

        print(f"Assistant: Great! Your experience " f"level is {experience}.")

        # ==================================
        # SHOW SUMMARY
        # ==================================

        show_summary()

        # ==================================
        # SAVE TO DATABASE
        # ==================================

        try:

            save_to_database(userdata)

            print("Assistant: Registration saved " "successfully!")

        except Exception as error:

            print("Assistant: Error saving " "registration.")

            print(f"Database error: {error}")

            conversation_state = "start"

            continue

        print("\nAssistant: Your registration " "information has been collected.")

        print("Assistant: Thank you for registering!")

        print(f"Assistant: Your registration ID is " f"{userdata['registration_id']}.")

        conversation_state = "completed"

    # ======================================
    # COMPLETED STATE
    # ======================================

    elif conversation_state == "completed":

        intent = predict_intent(user_input)

        # ==================================
        # REGISTER AGAIN
        # ==================================

        if intent == "register":

            reset_userdata()

            conversation_state = "name"

            print(
                "Assistant: Sure! I'll help you " "register for the internship again."
            )

            print("Assistant: Please provide " "your full name.")

        # ==================================
        # CHECK REGISTRATION
        # ==================================

        elif intent == "check_registration":

            registration_id = extract_registration_id(user_input)

            if registration_id:

                handle_check_registration(user_input)

            else:

                print(
                    "Assistant: Please provide "
                    "your registration ID, "
                    "for example REG0005."
                )

                conversation_state = "registration_id"

        # ==================================
        # GREETING AFTER COMPLETION
        # ==================================

        elif intent == "greeting":

            print("Assistant: Hello again!")

            print("Assistant: Your registration " "is already complete.")

        # ==================================
        # THANK YOU AFTER COMPLETION
        # ==================================

        elif intent == "thank_you":

            print("Assistant: You're welcome!")

        # ==================================
        # HELP AFTER COMPLETION
        # ==================================

        elif intent == "help":

            show_help()

        # ==================================
        # OTHER INPUT
        # ==================================

        else:

            print("Assistant: Your registration " "is already complete.")

            print("Assistant: You can check your " "registration using your ID.")

            print("Assistant: Type something like " "'check REG0008' or type 'exit'.")
