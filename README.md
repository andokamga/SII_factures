- pip install -r requirements.txt, pour installer toutes les dépendances qu'il contient, utilisez.
- Pour exécuter le projet, rendez-vous dans le dossier principal du projet et exécutez la commande suivante : python main.py
- Allez dans le dossier database et exécutez la commande python db_connection.py pour initialiser la base de données avec les données de test.
- Après l'exécution, les informations de connexion sont les suivantes : nom d'utilisateur : user1, mot de passe : password1.
- Après l'exécution, les informations de connexion sont les suivantes : nom d'utilisateur : user2, mot de passe : password2.

- Après la création ou l'impression de la facture, le fichier PDF est enregistré dans le dossier /documents/facture du répertoire de l'utilisateur.
- Après la sauvegarde, le fichier de la base de données est enregistré dans le dossier /data/facture du répertoire de l'utilisateur.
- Après la création de la facture, le fichier PDF de celle-ci s'ouvre pour permettre à l'utilisateur de l'imprimer

- Le code UI (front-end) permettant de créer la facture et d'exporter le fichier au format PDF se trouve dans le fichier invoice_window, avec les mots-clés generate_pdf() et create_invoice().

- Commande pour générer le fichier exécutable : python -m PyInstaller --onefile --noconsole --icon=facture.ico --add-data 'database/database.db;database' main.py