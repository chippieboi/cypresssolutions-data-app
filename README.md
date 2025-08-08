# cypresssolutions-data-app

## Install Instructions
IMPORTANT NOTE: Make sure you have Python version 3.9 or later installed on your computer. To test this, open Command Prompt and type 'python --version'.

### File Creation
Download the 'data app' folder and all of its contents. Extract the folder and open the folder where you see app.py, the data folder, requirements.txt, and verify_setup.py. At this level, create a folder and call it '.streamlit'. Inside the '.streamlit' folder, create a text file and call it 'secrets.toml'. Open this text tile and put the following into it and save:

[connections.da_mvp_db]
url = "sqlite:///./data/database.db"


All the files are now created (for some reason, GitHub didn't let me upload this folder, sorry about that).

### Command Line Setup
Open the 'data app' folder. In the blank space, right-click and select the 'Open in Terminal' option. Inside the terminal, type the following commands:

python -m venv venv
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

You should now see a green (venv) in front of your file directory on the left. Assuming you have that, do the following commands:

pip install --upgrade pip
pip install -r requirements.txt

You should now have the virtual environment set up and the dependencies downloaded.

### Verification and Running the App
Make sure you are still in the (venv) setup. Type the following to test you have everything correctly set up.

python verify_setup.py

If anything isn't working properly, check the file structure and the text in the secrets.toml file.
Once you have verified everything is installed correctly, run the following command to run the application:

streamlit run app.py

This should put some text into the command prompt and then open a new tab automatically in your browser. You can now use the application!

For future reference, when you go to run this application after setup, open the data app folder and open the command prompt like you did before. Then type the following to open the virtual environment and run the app:

.\venv\Scripts\Activate.ps1
streamlit run app.py
