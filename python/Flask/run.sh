#!/bin/bash

# Activate the virtual environment
source FlaskApp/bin/activate

# Set the FLASK_APP environment variable
# Modify this line if your Flask app instance or factory is named differently
export FLASK_APP=./app/app.py

# Optionally, set the FLASK_ENV to development for debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the Flask application
# flask run --reload
python app/app.py