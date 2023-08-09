# Бот прачка для Штиглица

## Prerequisites

1. [Python](https://python.org/) version 3.8 or later
2. pip or pip3

## Installation requirements

1. Create virtual environment 
    
    - For Windows:

        ```Powershell
        python -m venv .venv
        ```

    - For Linux, MacOS:
    
        ```shell
        python3 -m venv .venv
        ```

2. Activate virtual environment

    - For Windows:
    
        ```Powershell
        .\.venv\Scripts\activate
        ```

    - For Linux, MacOS:

        ```shell
        source ./.venv/bin/activate
        ```

3. Install requirements

    - For Windows:

        ```shell
        pip install -r requirements.txt
        ```

    - For Linux, MacOS:
    
        ```shell
        pip3 install -r requirements.txt
        ```


4. Create SQL tables

    - For Windows:

        ```powershell
        sqlite3 database.db
        ```
        ---
        ```sql
        CREATE TABLE records(time TEXT, date TEXT, id TEXT)
        CREATE TABLE users( id TEXT, name TEXT, number INTEGER)
        ```

    - For Linux, MacOS:

        ```bash
        sqlite3 database.db
        ```
        ---
        ```sql    
        CREATE TABLE records(time TEXT, date TEXT, id TEXT);
        CREATE TABLE users( id TEXT, name TEXT, number INTEGER);
        ```

## Running the bot

1. Activate virtual environment

    - For Windows:
    
        ```powershell
        .\.venv\Scripts\activate
        ```

    - For Linux, MacOS:

        ```bash
        source ./.venv/bin/activate
        ```

2. Setting environment variables

    - For Windows:

        ```Powershell
        $env:TOKEN = "TOKEN_TO_YOUR_BOT";
        ```
        

    - For Linux, MacOS:

        ```shell
        export TOKEN="TOKEN_TO_YOUR_BOT"
        ```

3. Run bot

    - For Windows:

        ```shell
        python .\src\main.py
        ```

    - For Linux, MacOS:

        ```shell
        python3 ./src/main.py
        ```