# BadgesCGR
Gestionnaire de badges pour la Rotonde


Python 3.8.5 - Tkinter 8.6 - tkcalendar  1.5.0

## Présentation

Cette application permet de gérer les badges de la Rotonde.

Toutes les actions effectuées sont inscrites dans un fichier de log `logbadges.csv`

Ce fichier peut être ouvert dans Calc/Excel en spécifiant l'encodage `UTF-8` et le séparateur `;`.

L'application fonctionne en utilisant le fichier `badges.ini` comme base de données de l'état de l'ensemble du parc de badges.  Ce fichier ne doit JAMAIS être modifié manuellement. 
Pour réinitialiser l'application, il suffit de le supprimer.  

## Distribuer l'application

Pour freezer l'application avec pyinstaller 

Windows : 
``pyinstaller --add-data cgr.ico;. --noconsole BadgesCGR.py`` 

Linux : 
``pyinstaller --add-data cgr.xbm:. --noconsole BadgesCGR.py`` 



 

