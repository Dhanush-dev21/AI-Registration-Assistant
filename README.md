# AI Registration Assistant

An AI-powered internship registration chatbot built with Python, Natural Language Processing (NLP), Machine Learning, and SQLite.

## Internship Task Details

- **Task ID:** AI-SS-001
- **Student Code:** DAS006342
- **Project:** AI Registration Assistant

## Features

- Natural-language internship registration
- Machine Learning-based intent classification
- Greeting and help responses
- Name extraction
- Email extraction and validation
- Duplicate email validation
- Field of study extraction
- Programming experience extraction
- Automatic registration ID generation
- SQLite database storage
- Search registration using Registration ID
- Handles invalid Registration IDs
- Handles unknown questions
- Cancel registration
- Restart registration
- Help command

## Technologies Used

- Python
- NLTK
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression
- SQLite
- Regular Expressions (Regex)

## Requirements

- Python 3.10 or above
- pip

## Project Structure

```text
AI_REG/
│
├── main.py
├── intent_model.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── registrations.db
```

## How It Works

The chatbot uses a Machine Learning intent classifier to understand user messages.

For example:

```text
User: I want to register

Assistant: Great! I'll help you register for the internship.
```

The assistant then collects:

1. Full Name
2. Email Address
3. Field of Study
4. Programming Experience

After collecting the information, the chatbot generates a unique Registration ID and stores the data in an SQLite database.

Example:

```text
Registration ID: REG0006

Name: Dhanush
Email: dhanush@gmail.com
Field: Computer Science
Experience: Beginner
```

## Natural Language Support

The chatbot understands natural sentences such as:

```text
My name is Dhanush

My email is dhanush@gmail.com

I study Computer Science

I am a beginner
```

## Check Registration

Users can search for their registration using the Registration ID.

Example:

```text
You: check REG0006
```

The assistant retrieves the registration information from the SQLite database.

If the Registration ID does not exist:

```text
You: check REG9999

Assistant: No registration found with ID REG9999.
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Download the required NLTK data:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"
```

## Run the Project

Start the chatbot:

```bash
python main.py
```

## Example

```text
You: I want to register

Assistant: Great! I'll help you register for the internship.
Assistant: Please provide your full name.

You: My name is Dhanush

Assistant: Please provide your email address.

You: dhanush@gmail.com

Assistant: Now, please tell me your field of study.

You: I study Computer Science

Assistant: Now, tell me about your programming experience.

You: I am a beginner

Assistant: Registration completed successfully.
```

The completed registration is saved in the SQLite database.

## Future Improvements

- Web-based User Interface
- REST API
- Better Intent Classification
- More Registration Fields
- Admin Dashboard
- Registration Update and Deletion
- Cloud Deployment

## Author

**Dhanush**

## GitHub Repository

https://github.com/Dhanush-dev21/AI-Registration-Assistant

## License

This project was created for educational and internship purposes.