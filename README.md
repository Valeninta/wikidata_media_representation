Script for getting the female/male ratio of the crew of a given film. Inspired by the approach used here: https://projects.fivethirtyeight.com/next-bechdel/#footnote-anchor-5

# Procedure
1. Get all crew members from imdb's full credits (excluding transportation department, miscellaneous and stunt department)
2. Using the imdb Id: check for each crew member if there is an entry in wikidata with a gender attribution. If yes, take this.
3. (Optional) Using imdb's name.basics. tsv: check for each remaining crew member if they are mentioned as actor or actress. If as actor, assign gender "male", if as actress, assign gender "female". You can download the file here: https://datasets.imdbws.com/
4. Using genderize.io: get for each remaining crew member's given name the gender attribution in genderize.io, including the probabilty that the assignment is correct. The information is stored in a file names_to_gender.csv that may be reused in later runs.
5. Print a Breakdown of the results (number/share of crew members with male/female/unsure gender attribution). When the gender was derived from the given name only gender attributions with a probabily >= 90% are accepted. All other crew members are counted towards the "unsure" category.

The results are written into a file crew_gender_```film_title```.csv and can be scrutinized there, if necessary.

# Prerequisites
This script is written in python3. It uses the BeautifulSoup (https://pypi.org/project/beautifulsoup4) and Genderize (https://github.com/SteelPangolin/genderize) library.
1. Install python3 if you don't have it installed. Installation instructions: https://wiki.python.org/moin/BeginnersGuide/Download
 - If you are new to Python you can just install Anaconda instead: https://anaconda.org/
 - After installation open an Anaconda prompt (in Windows from start menu)
 - Install pip as a package installer: ```conda install pip```
 - Install git to get packages from github: ```conda install git```
2. Install BeautifulSoup: ```pip install beautifulsoup4```
3. Install Genderize: ```pip install git+https://github.com/SteelPangolin/genderize```

## Optional data files to use
To get gender information from imdb's name.basics.tsv download it here: https://datasets.imdbws.com/. You should place it into the same directory as this script.

# Using this script
* In a terminal (e.g an Anaconda prompt) navigate into the directory where the python script is placed. (e.g., for Windows users, if your directory is C:\Users\Me\python_scripts, enter ```cd C:\Users\Me\python_scripts```)
* Enter ```python3 genderize_film.py```
* You will be prompted to add a film title and the imdb id. As a film title you can use anything you like. It will be only used to generate the filename of the results file.
