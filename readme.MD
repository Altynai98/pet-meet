# Pet Meet

## Installing the app

1. Create virtual environment - `python -m venv .venv`
2. Activate virtual environment - `source .venv/bin/activate`
3. Install requirements - `pip install -r requirements.txt`
4. Go into the web app folder - `cd pet_meet`
5. Apply migrations - `python manage.py migrate`
6. Start the app - `python manage.py runserver`


## Testing the app

In order to test the web app, you need to use **Postman**. You can import the requests from the file `Pet Meet.postman_collection.json`. To test most endpoints, you need to create a user first (sign up), then sign in.