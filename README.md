# Todo-list
A todo-list application for my submission to placexp

## How to run
This application is built in flask, a python web framework. I will assume you have python3 installed and added to the path variable. If this is not the case, do so now.

#### Step 1
Fork this repository and clone it into your local machine.

#### Step 2 (optional)
At this stage, you may prefer to start a python virtual environment before installing dependencies. If so, now is the time to do so. If you don't want to create a virtual environment, you can skip this step

To create and start a virtual environment with the 'venv' module, first, open a terminal and navigate to the root folder of this repository.

To create a virtual environment with name 'your-env', type:
`python -m venv your-env`
To start this env, type:

###### (cmd)
`your-env\scripts\activate.bat`

###### (UNIX/macOS)
`source your-env/bin/activate`

To deactivate your env, simply type `deactivate`

#### Step 3
Now we will install dependencies. Start your virtual environment if you have one, then, at the root folder, type

`python -m pip install -r requirements.txt`

#### Step 4
And finally, to run the application, type:

`flask run`

Visit (localhost:5000) to see the application run

Don't hesitate to contact me in case of any difficulties :)

20BCE1896