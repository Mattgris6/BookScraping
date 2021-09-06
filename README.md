#BookScraping
Téléchargez les scripts présents sur le dépôt GitHub : https://github.com/Mattgris6/OC_DAPyhon_Projet2_BookScraping
Placez ces scripts dans un répertoire de travail sur votre ordinateur.

Pour créer un environnement virtuel, dans votre terminal, placez vous dans votre répertoire de travail via la commande cd (+ chemin du répertoire).
Ensuite, tapez la commande :

python -m venv env

Un nouveau répertoire env s'est créé dans votre répertoire de travail.
Pour l'activer, tapez la commande :

env/Scripts/activate.bat

Maintenant que vous êtes dans l'environnement virtuel, installez les paquets requis pour le code via la commande:

pip install -r requirements.txt

Ensuite, vous pouvez lancer le programme avec :

python book_scraping.py

Le programme met plusieurs minutes à tourner. Il génère les résultats dans un dossier "Résultats" placé dans votre répertoire de travail.
