# Capstone_Project

**Project Name**
Capstone Project (Security Software Development) - IAM using facial recognition

**Development Environment**
1. Windows 10, PyCharm Community Edition, MariaDB
2. Machine Learning Module: OpenCV
3. MySQL, Python, Python Flask, HTML, CSS, HeidiSQL
4. Password Encryption: Salt hashing
5. Exception Handling

**Project Objectives**
1. Build a web login & registration interface
2. Build a user authentication module
3. Integrate a facial recognition module
4. Add a security logging module
5. Store password using salt and hashing concept

**How to set-up & How to run**
1. Please download the codes from the repostory.
2. Install the PyCharm Community Edition and create the venv (virtual environment) in it.
3. After setting up the PyCharm environment, please install the required packages (Please take a look at the "Packages to be installed" list)
4. The three html files (index,login,signup) must be in the folder named "templates".
5. Create the folder named "knowns". This is the folder where you save the facial images of people (must be .jpeg files).
6. Run the login.py in the terminal (python login.py).
7. Open the browser and go to your localhost (http://127.0.0.1:5000/).
8. Click "Sign Up" and finish the registration.
9. After logging in successfully, you will be able to see the task page.
10. At the task page, you will be able to see the word "Face Recognition". That is the link which will connect you to the facial recognition.
11. After clicking on the link, run facial recognition and a webcam will launch on your computer screen to scan you. 
12. If there is a facial image about you stored in the "Templates" folder, it will show the user name and face recognition will be passed but otherwise it will display the word "unknown". (Please see to the project result images.)
13. Finally, you can check the security log (activity related to security issues and please see the project result images)
