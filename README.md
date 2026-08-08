# AI Registration Assistant

An AI-powered internship registration chatbot built with Python, Natural Language Processing (NLP), Machine Learning, and SQLite.

## Internship Task Details

- **Task ID:** AI-SS-001
- **Project:** AI Registration Assistant

## Features

- Natural-language internship registration
- Machine Learning-based intent classification
- Greeting and help responses
- Name extraction and validation
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
- Exit command

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

> The SQLite database contains registration data and is excluded from the GitHub repository using `.gitignore`.

## How It Works

The chatbot uses a Machine Learning intent classifier to understand user messages.

For example:

```text
You: I want to register

Assistant: Great! I'll help you register for the internship.
Assistant: Please provide your full name.
```

The assistant then collects:

1. Full Name
2. Email Address
3. Field of Study
4. Programming Experience

After collecting the information, the chatbot generates a unique Registration ID and stores the data in an SQLite database.

Example:

```text
Registration ID: REG0001

Name: Student
Email: student@example.com
Field: Computer Science
Experience: Beginner
```

## Natural Language Support

The chatbot understands natural sentences such as:

```text
My name is Student

My email is student@example.com

I study Computer Science

I am a beginner
```

## Check Registration

Users can search for their registration using the Registration ID.

Example:

```text
You: check REG0001
```

The assistant retrieves the registration information from the SQLite database.

If the Registration ID does not exist:

```text
You: check REG9999

Assistant: No registration found with ID REG9999.
```

## Cancel Registration

Users can cancel the registration process using:

```text
You: cancel

Assistant: Registration cancelled.
Assistant: You can type 'I want to register' anytime to start again.
```

## Restart Registration

Users can restart the registration process using:

```text
You: restart

Assistant: Registration restarted.
Assistant: Please provide your full name.
```

## Help Command

Users can view the available commands using:

```text
You: help
```

The assistant displays the available registration and chatbot commands.

## Exit Command

Users can safely close the chatbot using:

```text
You: exit

Assistant: Thank you for using the AI Registration Assistant. Goodbye!
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

### Windows

```bat
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
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

You should see:

```text
AI REGISTRATION ASSISTANT

======================================
Type 'help' for available commands.
Type 'exit' to stop the chatbot.

You:
```

## Example

```text
You: I want to register

Assistant: Great! I'll help you register for the internship.
Assistant: Please provide your full name.

You: Student

Assistant: Nice to meet you, Student!
Assistant: Please provide your email address.

You: student@example.com

Assistant: Thank you! Your email student@example.com has been recorded.
Assistant: Now, please tell me your field of study.

You: Computer Science

Assistant: Great! You're studying Computer Science.
Assistant: Now, tell me about your programming experience.

You: Intermediate

Assistant: Great! Your experience level is Intermediate.

Registration information collected successfully!
Assistant: Registration saved successfully!
Assistant: Your registration information has been collected.
Assistant: Thank you for registering!
Assistant: Your registration ID is REG0001.
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