import re
import sqlite3

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from intent_model import predict_intent

from database import (
    initialize_database,
    save_to_database,
    find_registration
)


# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()


# ==========================================
# NLTK NLP PREPROCESSING
# ==========================================

lemmatizer = WordNetLemmatizer()


def preprocess_text(text):

    text = text.lower()

    tokens = word_tokenize(text)

    lemmas = [
        lemmatizer.lemmatize(token)
        for token in tokens
    ]

    return lemmas


# ==========================================
# STUDENT REGISTRATION DATA
# ==========================================

user_data = {
    "registration_id": "",
    "name": "",
    "email": "",
    "field": "",
    "experience": ""
}


# ==========================================
# GENERATE REGISTRATION ID
# ==========================================

def generate_registration_id():

    conn = sqlite3.connect(
        "data/registrations.db"
    )

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

        number = int(
            last_id.replace("REG", "")
        )

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

        r"(?:name is)\s+([a-zA-Z ]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            user_input,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return None


# ==========================================
# EXTRACT EMAIL
# ==========================================

def extract_email(user_input):

    pattern = (
        r"[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}"
    )

    match = re.search(
        pattern,
        user_input
    )

    if match:

        return match.group()

    return None


# ==========================================
# VALIDATE EMAIL
# ==========================================

def is_valid_email(email):

    pattern = (
        r"^[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}$"
    )

    return re.match(
        pattern,
        email
    ) is not None


# ==========================================
# EXTRACT FIELD OF STUDY
# ==========================================

def extract_field(user_input):

    patterns = [

        r"(?:i study|i'm studying|i am studying|"
        r"my field is|field is)\s+(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            user_input,
            re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return None


# ==========================================
# EXTRACT EXPERIENCE
# ==========================================

def extract_experience(user_input):

    patterns = [

        r"(?:i am a|i'm a|i am|i'm)\s+"
        r"(beginner|intermediate|advanced|expert)",

        r"(?:my experience is|experience level is)\s+(.+)",

        r"(?:i have)\s+(.+?)\s+(?:experience)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            user_input,
            re.IGNORECASE
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
        user_input.upper()
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

    print(
        f"Registration ID: "
        f"{user_data['registration_id']}"
    )

    print(
        f"Name:       {user_data['name']}"
    )

    print(
        f"Email:      {user_data['email']}"
    )

    print(
        f"Field:      {user_data['field']}"
    )

    print(
        f"Experience: {user_data['experience']}"
    )

    print("======================================")

    print(
        "Registration information collected successfully!"
    )


# ==========================================
# DISPLAY FOUND REGISTRATION
# ==========================================

def show_registration(registration):

    print("\n======================================")
    print("       REGISTRATION FOUND")
    print("======================================")

    print(
        f"Registration ID: "
        f"{registration['registration_id']}"
    )

    print(
        f"Name:       {registration['name']}"
    )

    print(
        f"Email:      {registration['email']}"
    )

    print(
        f"Field:      {registration['field']}"
    )

    print(
        f"Experience: {registration['experience']}"
    )

    print("======================================")


# ==========================================
# HANDLE CHECK REGISTRATION
# ==========================================

def handle_check_registration(user_input):

    registration_id = extract_registration_id(
        user_input
    )

    if not registration_id:

        print(
            "Assistant: Please provide your "
            "registration ID, for example REG0005."
        )

        return

    registration = find_registration(
        registration_id
    )

    if registration:

        show_registration(
            registration
        )

    else:

        print(
            f"Assistant: No registration found "
            f"with ID {registration_id}."
        )


# ==========================================
# START CHATBOT
# ==========================================

print("======================================")
print("     AI REGISTRATION ASSISTANT")
print("======================================")

print(
    "Type 'exit' to stop the chatbot.\n"
)


# ==========================================
# CONVERSATION STATE
# ==========================================

conversation_state = "start"


# ==========================================
# MAIN CHATBOT LOOP
# ==========================================

while True:

    user_input = input("You: ").strip()


    # ======================================
    # EXIT
    # ======================================

    if user_input.lower() == "exit":

        print(
            "Assistant: Thank you for using "
            "the AI Registration Assistant. Goodbye!"
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

            handle_check_registration(
                user_input
            )


        # ==================================
        # REGISTER
        # ==================================

        elif intent == "register":

            print(
                "Assistant: Great! I'll help you "
                "register for the internship."
            )

            print(
                "Assistant: Please provide "
                "your full name."
            )

            conversation_state = "name"


        # ==================================
        # GREETING
        # ==================================

        elif intent == "greeting":

            print(
                "Assistant: Hello! Welcome to "
                "the AI Registration Assistant. "
                "How can I help you?"
            )


        # ==================================
        # HELP
        # ==================================

        elif intent == "help":

            print(
                "Assistant: I can help you with "
                "internship registration and "
                "registration status."
            )


        # ==================================
        # THANK YOU
        # ==================================

        elif intent == "thank_you":

            print(
                "Assistant: You're welcome!"
            )


        # ==================================
        # UNKNOWN
        # ==================================

        else:

            print(
                "Assistant: I'm not sure I "
                "understood. Could you please "
                "rephrase your question?"
            )


    # ======================================
    # NAME STATE
    # ======================================

    elif conversation_state == "name":

        name = extract_name(
            user_input
        )


        if name:

            user_data["name"] = name


        elif re.fullmatch(
            r"[a-zA-Z ]+",
            user_input
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
                "thank you"
            ]


            if user_input.lower() in invalid_phrases:

                print(
                    "Assistant: Please enter "
                    "your actual full name."
                )

                continue


            if len(words) > 4:

                print(
                    "Assistant: Please enter "
                    "a valid name."
                )

                continue


            user_data["name"] = (
                user_input.strip()
            )


        else:

            print(
                "Assistant: Please enter "
                "a valid name."
            )

            continue


        print(
            f"Assistant: Nice to meet you, "
            f"{user_data['name']}!"
        )

        print(
            "Assistant: Please provide "
            "your email address."
        )

        conversation_state = "email"


    # ======================================
    # EMAIL STATE
    # ======================================

    elif conversation_state == "email":

        email = extract_email(
            user_input
        )


        if email and is_valid_email(email):

            user_data["email"] = email

            print(
                f"Assistant: Thank you! Your email "
                f"{email} has been recorded."
            )

            print(
                "Assistant: Now, please tell me "
                "your field of study."
            )

            conversation_state = "field"


        else:

            print(
                "Assistant: That email address "
                "is not valid."
            )

            print(
                "Assistant: Please enter a valid "
                "email address."
            )


    # ======================================
    # FIELD STATE
    # ======================================

    elif conversation_state == "field":

        field = extract_field(
            user_input
        )


        if not field:

            field = user_input.strip()


        if len(field) < 2:

            print(
                "Assistant: Please enter your "
                "field of study."
            )

            continue


        user_data["field"] = field


        print(
            f"Assistant: Great! You're studying "
            f"{field}."
        )

        print(
            "Assistant: Now, tell me about "
            "your programming experience."
        )

        conversation_state = "experience"


    # ======================================
    # EXPERIENCE STATE
    # ======================================

    elif conversation_state == "experience":

        experience = extract_experience(
            user_input
        )


        if not experience:

            experience = user_input.strip()


        if len(experience) < 2:

            print(
                "Assistant: Please describe "
                "your programming experience."
            )

            continue


        user_data["experience"] = (
            experience
        )


        # Generate registration ID

        user_data["registration_id"] = (
            generate_registration_id()
        )


        print(
            f"Assistant: Great! Your experience "
            f"level is {experience}."
        )


        # Display summary

        show_summary()


        # Save to SQLite

        try:

            save_to_database(
                user_data
            )

            print(
                "Assistant: Registration saved "
                "successfully!"
            )

        except Exception as error:

            print(
                "Assistant: Error saving "
                "registration."
            )

            print(
                f"Database error: {error}"
            )

            conversation_state = "start"

            continue


        print(
            "\nAssistant: Your registration "
            "information has been collected."
        )

        print(
            "Assistant: Thank you for registering!"
        )


        conversation_state = "completed"


    # ======================================
    # COMPLETED STATE
    # ======================================

    elif conversation_state == "completed":

        intent = predict_intent(
            user_input
        )


        # ==================================
        # CHECK REGISTRATION AFTER COMPLETION
        # ==================================

        if intent == "check_registration":

            handle_check_registration(
                user_input
            )


        # ==================================
        # OTHER INPUT
        # ==================================

        else:

            print(
                "Assistant: Your registration is "
                "already complete."
            )

            print(
                "Assistant: You can check your "
                "registration using your ID."
            )

            print(
                "Assistant: Type something like "
                "'check REG0005' or type 'exit'."
            )

