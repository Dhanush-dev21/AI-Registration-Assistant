\# AI Registration Assistant



An AI-powered internship registration chatbot built with Python, Natural Language Processing (NLP), Machine Learning, and SQLite.



\## Features



\* Natural-language internship registration

\* ML-based intent classification

\* Greeting and help responses

\* Name extraction

\* Email extraction and validation

\* Field of study extraction

\* Programming experience extraction

\* Automatic registration ID generation

\* SQLite database storage

\* Search registration using registration ID

\* Handles invalid registration IDs

\* Handles unknown questions



\## Technologies Used



\* Python

\* NLTK

\* Scikit-learn

\* TF-IDF Vectorization

\* Logistic Regression

\* SQLite

\* Regular Expressions



\## Project Structure



```text

AI\_REG/

│

├── main.py

├── intent\_model.py

├── database.py

├── requirements.txt

├── README.md

├── .gitignore

│

├── data/

│   └── registrations.db

│

└── venv/

```



\## How It Works



The chatbot uses a machine-learning intent classifier to understand user messages.



For example:



```text

User: I want to register

Assistant: Great! I'll help you register for the internship.

```



The assistant then collects:



1\. Full name

2\. Email address

3\. Field of study

4\. Programming experience



After collecting the information, the system generates a unique registration ID.



Example:



```text

Registration ID: REG0006

Name: Dhanush

Email: dhanush@gmail.com

Field: Computer Science

Experience: Beginner

```



\## Natural Language Support



The chatbot can understand natural sentences such as:



```text

My name is Dhanush

My email is dhanush@gmail.com

I study Computer Science

I am a beginner

```



\## Check Registration



Users can search for a registration using the registration ID.



Example:



```text

You: check REG0006

```



The assistant retrieves the registration information from the SQLite database.



If the ID does not exist:



```text

You: check REG9999

Assistant: No registration found with ID REG9999.

```



\## Installation



Create and activate a virtual environment:



```text

python -m venv venv

venv\\Scripts\\activate

```



Install the required packages:



```text

pip install -r requirements.txt

```



Download the required NLTK data:



```text

python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"

```



\## Run the Project



Start the chatbot with:



```text

python main.py

```



\## Example



```text

You: I want to register



Assistant: Great! I'll help you register for the internship.



You: My name is Dhanush



You: My email is dhanush@gmail.com



You: I study Computer Science



You: I am a beginner

```



The system saves the completed registration in SQLite.



\## Future Improvements



\* Web-based user interface

\* REST API

\* Better intent classification

\* More registration fields

\* Admin dashboard

\* Registration update and deletion

\* Deployment to a cloud platform



\## Author



Dhanush



\## License



This project is created for educational and internship purposes.



