from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# ==========================================
# TRAINING DATA
# ==========================================

training_data = [

    # Greeting
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("hi there", "greeting"),
    ("hello there", "greeting"),
    ("good morning", "greeting"),
    ("good afternoon", "greeting"),
    ("good evening", "greeting"),

    # Registration
    ("I want to register", "register"),
    ("I want to apply", "register"),
    ("I want to join the internship", "register"),
    ("help me register", "register"),
    ("I want to sign up", "register"),
    ("I want to enroll", "register"),
    ("I want to apply for internship", "register"),
    ("I want to register for internship", "register"),

    # Help
    ("I need help", "help"),
    ("can you help me", "help"),
    ("I need assistance", "help"),
    ("please guide me", "help"),
    ("I need support", "help"),
    ("help me", "help"),
    ("what can you help me with", "help"),
    ("I have a question", "help"),

    # Thank you
    ("thanks", "thank_you"),
    ("thank you", "thank_you"),
    ("thank you very much", "thank_you"),
    ("I appreciate your help", "thank_you"),
    ("thanks for helping me", "thank_you"),
    ("that's helpful", "thank_you"),

    # Check registration
    ("check my registration", "check_registration"),
    ("check registration", "check_registration"),
    ("check my application", "check_registration"),
    ("check my application status", "check_registration"),
    ("what is my registration status", "check_registration"),
    ("show my registration", "check_registration"),
    ("find my registration", "check_registration"),
    ("look up my registration", "check_registration"),
    ("check REG0001", "check_registration"),
    ("check REG0002", "check_registration"),
    ("check REG0003", "check_registration"),
    ("check REG0004", "check_registration"),

    # Unknown / unrelated
    ("what is the weather today", "unknown"),
    ("tell me a joke", "unknown"),
    ("what is the capital of India", "unknown"),
    ("who are you", "unknown"),
    ("what time is it", "unknown"),
    ("how are you", "unknown"),
    ("tell me about cricket", "unknown")
]


# ==========================================
# SEPARATE SENTENCES AND LABELS
# ==========================================

training_sentences = [
    item[0] for item in training_data
]

training_labels = [
    item[1] for item in training_data
]


# ==========================================
# TF-IDF
# ==========================================

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(
    training_sentences
)


# ==========================================
# LOGISTIC REGRESSION
# ==========================================

model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X,
    training_labels
)


# ==========================================
# PREDICT INTENT
# ==========================================

def predict_intent(user_input):

    user_vector = vectorizer.transform(
        [user_input]
    )

    probabilities = model.predict_proba(
        user_vector
    )

    confidence = probabilities.max()

    prediction = model.predict(
        user_vector
    )[0]

    # Low confidence means unknown
    if confidence < 0.30:

        return "unknown"

    return prediction


# ==========================================
# PREDICT INTENT + CONFIDENCE
# ==========================================

def predict_intent_with_confidence(user_input):

    user_vector = vectorizer.transform(
        [user_input]
    )

    probabilities = model.predict_proba(
        user_vector
    )

    confidence = probabilities.max()

    prediction = model.predict(
        user_vector
    )[0]

    # Low confidence means unknown
    if confidence < 0.30:

        prediction = "unknown"

    return prediction, round(
        float(confidence),
        2
    )


# ==========================================
# TEST MODEL
# ==========================================

if __name__ == "__main__":

    test_inputs = [

        "Hi there",

        "I want to apply for the internship",

        "Can you help me?",

        "Thank you very much",

        "check my registration",

        "check REG0004",

        "What is the weather today?",

        "I want to register"
    ]


    print("======================================")
    print("      INTENT CLASSIFICATION TEST")
    print("======================================")


    for text in test_inputs:

        intent, confidence = (
            predict_intent_with_confidence(text)
        )

        print(
            f"Input: {text}"
        )

        print(
            f"Intent: {intent}"
        )

        print(
            f"Confidence: {confidence:.2f}"
        )

        print()

