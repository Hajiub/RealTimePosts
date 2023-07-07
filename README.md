## Real Time Posts

A web application that allows users to view and interact with real-time posts using AJAX polling.

## Technologies Used
HTML

CSS

JavaScript

AJAX

SQLite

## Getting Started
1. Clone the repository
```bash
git clone https://github.com/Hajiub/RealTimePosts.git
```
2. change the directory
``` bash
cd RealTimePosts
```
2. Follow this steps
```bash
# 1. Create a Python virtual environment
python3 -m venv .venv

# 2. Activate the virtual environment (for Linux and macOS)
source .venv/bin/activate

# 3. Install the project requirements
pip3 install -r requirements.txt
```
3. Create The sqlite database
```bash
# 1. Create the migration repository
python3 manage.py db init
# 2. Generate an initial migration
python3 manage.py db migrate -m 'Initial migration.'
# 3. Apply the changes to the database
python3 manage.py db upgrade
```
4. Start The app
```bash
python3 manage.py run
```
5. You can view all the commands
```
python3 manage.py
```



