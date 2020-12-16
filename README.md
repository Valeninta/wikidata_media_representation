Script for getting the female/male ratio of the crew of a given film. Inspired by the approach used here: https://projects.fivethirtyeight.com/next-bechdel/#footnote-anchor-5

# Procedure
1. Get all crew members from imdb's full credits (excluding transportation department, miscellaneous and stunt department)
2. Using the imdb Id: check for each crew member if there is an entry in wikidata with a gender attribution. If yes, take this.
3. (Optional) Using imdb's name.basics. tsv: check for each remaining crew member if they are mentioned as actor or actress. If as actor, assign gender "male", if as actress, assign gender "female". You can download the file here: https://datasets.imdbws.com/
4. Using genderize.io: get for each remaining crew member's given name the gender attribution in genderize.io, including the probabilty that the assignment is correct. The information is stored in a file names_to_gender.csv that may be reused in late runs.
5. Print a Breakdown of the results (number/share of crew members with male/female/unsure gender attribution). When the gender was derived from the given name only gender attributions with a probabily >= 90% were accepted. All other crew members were counted towards the "unsure" category.

The results are written into a file crew_gender_ + film_title

# Prerequisites
This script is written in python3. It uses the BeautifulSoup (https://pypi.org/project/beautifulsoup4) and Genderize (https://github.com/SteelPangolin/genderize) library.
1. You need to install python3. Installation instructions: https://wiki.python.org/moin/BeginnersGuide/Download
2. You need to install BeautifulSoup: ```pip install beautifulsoup4```
3. You need to install Genderize: ```pip install git+https://github.com/SteelPangolin/genderize```

To get gender information from imdb's name.basics.tsv you need to download it here: https://datasets.imdbws.com/. You should place it into the same directory as this script.

# Using this script
After downloading this script, open a terminal in the same directory as the script. Start it using ```python3 genderize_film.py```. You will be prompted to add a film title and the imdb id.
