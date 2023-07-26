# ZET-Compass

Calculates the best moment to invest in zero emission transport and charging infrastructure for your company.
The application is written in Python and uses the Flask framework to run a web application.
Anaconda is used to manage the Python environment and dependencies.

For detailed information about the project, please visit the [project wiki](https://github.com/Jakolien/ZET-compass/wiki).
The wiki is written in Dutch.

## Installation

In order to run the app, Anaconda needs to be installed.
Download the most recent version from [Anaconda's website](https://www.anaconda.com/download). 
After the installation file finished downloading, run it. 
Assistance for installing the application can be found in [the installation guide of Anaconda](https://docs.anaconda.com/free/navigator/install/). 
It is assumed that Anaconda Navigator is installed. 

The next step is to import the environment. 
This can be done under the tab "Environments". 
A file is included that contains the enviroment settings. 
This file is ```kompas.yml```. 
This file needs to be imported into Anaconda.
At the bottom of the "Environments"-page is a button "Import". 
Navigate to the ```kompas.yml``` file and import it. 
Anaconda will now prepare the environment.

![Zet-Kompass Enviroment in Anaconda](https://github.com/Jakolien/ZET-compass/assets/104203258/f2d5f807-e7bc-4186-8035-34967572ce71)

## Running the application

In order to run the application, a ```anaconda powershell prompt``` is used. 
This is installed together with Anaconda. 
The Prompt is available through the start menu in Windows. 
De following steps are required to run the application:

1. Activate "kompas" enviroment: ```conda activate kompas```.
2. Navigate to the project: ```cd [locatie]```. Right clicking the folder in explorer allows the path to be copied, this options is called "copy as path".
3. Execute the file: ```python app.py```

<img width="867" alt="Zet-Kompass Draaien" src="https://github.com/Jakolien/ZET-compass/assets/104203258/5d65824b-c53d-45f1-9dd6-699bad50a5d7">

## Credits

Originally written as a Jupyter notebook by Jakolien van der Meer.
Lecturer at the research group Supply Chain Innovation at the HZ University of Applied Sciences.
Email: [jakolien.meer@gmail.com](mailto:jakolien.meer@gmail.com?subject=TransportTransport%20Kompas)

Rewritten to a Flask application by Julien Kenneth Pleijte.
IT Bachelor Student at the HZ University of Applied Sciences.
Email: [julienmaster21@gmail.com](mailto:julienmaster21@gmail.com?subject=Transport%20Kompas)

External Routes optimized and extended by Wesley van Schaijk.
IT Bachelor Student at the HZ University of Applied Sciences.
GitHub: [Jimmaphy](https://github.com/jimmaphy)

## The Results Example

![Results of ZET-Kompass](documentation/transport_kompas_results.jpeg)


