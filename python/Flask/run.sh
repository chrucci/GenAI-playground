#!/bin/bash

# Activate the virtual environment
source FlaskApp/bin/activate

# Ensure app.py exists in the current directory
# if [ ! -f "app.py" ]; then
#     echo "Error: app.py not found in the current directory."
#     exit 1
# fi

# Set the FLASK_APP environment variable
# Modify this line if your Flask app instance or factory is named differently
export FLASK_APP=./app/app.py

# Optionally, set the FLASK_ENV to development for debug mode
export FLASK_ENV=development

# Run the Flask application
flask run