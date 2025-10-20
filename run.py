import os
from dotenv import load_dotenv
load_dotenv()
from my_app import create_app

app=create_app()

if __name__=="__main__":
    app.run(debug=True)
