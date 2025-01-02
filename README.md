# agentic-customer-support
A multi agent system to provide customer support.

### Set up 

1. Create a file named `.env` with the following content:

    ```env
    OPENAI_API_KEY=<your_api_key_here
    ```
2. Create a virtual environment and install dependencies in requirements.txt

    ```
    $python -m venv .venv
    $source .venv/bin/activate
    $pip install -r requirements.txt
    ```
3. [Optional] If you need to reset the database, delete the mattress.db file and run create_db.py to create and insert the initial dataset. 

    ```$python create_db.py```

4. Run frodo by executing `python frodo.py`