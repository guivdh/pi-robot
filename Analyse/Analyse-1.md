#Table des matières :

##Commun à tous les thèmes
* Analyse / Cahier des charges : Formalisation de la demande du client
o Contexte dans lequel le TFE s’articule
o Présentation des besoins du client (fonctionnalités et non solutions)
* Eventuellement sous forme de User Stories
o Sujet pertinent, projet avec des spécificités, validé par le rapporteur (Intérêt technique? Intérêt pour un client? Pas de logiciels identiques génériques déjà existants? Etude de marché? Sondages?)
o Charge de travail suffisante, validée également par le rapporteur (300h environ, comprenant notamment une analyse suffisante)
o Contraintes dont l’étudiant doit tenir compte (matériel, temporel, …)
o Documents/schémas selon la thématique (UML, DB, etc. pour le développement, schémas réseaux/électroniques de l’existant, …)
* Présentation de la méthodologie utilisée
* Présentation de la solution avec justification des choix effectués
o Documents/schémas selon la thématique (Diagrammes de classe, schémas réseaux, …)
* Historique du projet : Planning de la réalisation + bilan des rencontres avec le client (+ éventuellement rapporteur) et explication de l’évolution des choix dans le temps
* Utilisation d’un outil de versionning type GitHub dès le début du projet (commit unique la veille de la remise non accepté)
* Tout code doit être facilement testable par l’équipe pédagogique. Par ex., pour TFE applicatif : l’application doit être déployable instantanément par les professeurs, via la mise à disposition d’une procédure d’installation courte (par ex. image docker). L’étudiant doit se concerter avec son rapporteur pour valider cette procédure
* Quelle que soit la thématique, réflexion sur la sécurité : Identification des risques, proposition de contre-mesures
* Démonstration du cas pratique : Dès le début du TFE, l’étudiant doit réfléchir à la manière dont il montrera sa réalisation. Si cela ne s’avère pas possible, il doit en discuter avec son rapporteur qui pourra, le cas échéant, faire une visite sur site pour pouvoir se porter garant de la réalisation effectuée. Dans ce cas, une vidéo ou une démo simplifiée sera également préparée pour que le jury puisse se faire une idée de ce qui a été fait. Idéalement le projet doit être testé et validé par le client et déployé en production.
* Analyse critique du projet, points forts et points faibles, améliorations envisageables, plan pour le futur

##Sécurité
* Analyse de sécurité pour tout projet :
o Identification des biens à protéger (assets)
o quels sont les risques
o quelles sont les contre-mesures mises en place
o quels sont les risques résiduels
* Site en https
* Prise en compte des données personnelles et du GDPR

##Physique appliquée (électricité & électronique, signal, télécoms)
Le travail devrait comporter une partie matérielle (p.e. carte hardware assemblée et/ou développée par l’étudiant avec des entrées/sorties analogiques et/ou numériques, robot, systèmes d’acquisition de signaux, ...). 
Dans la mesure du possible, une simulation préalable de la solution sera développée par l’étudiant. La partie matérielle doit communiquer avec une interface utilisateur (application pc, mobile, ...) via des interfaces et des protocoles de communication adaptés à l’environnement dans lequel l’application tourne. 
Il faut conditionner les signaux reçus (calibration du système pour un environnement donné, nettoyage des bruits, filtrage, amplification, …) et puis les traiter pour répondre aux objectifs de l’application finale.
En plus des attentes communes à tous les projets (voir plus haut), le doit TFE doit expliciter :
* Le besoin recherché sous forme de cahier de charges (préciser notamment les contraintes temporelles, les contraintes énergétiques, les contraintes d’espace mémoire, les contraintes environnementales, les contraintes des temps de latence dans les transferts de données, etc),
* L'étude succincte des possibilités existantes et la justification des choix faits (pq tel ou tel composant, protocole, etc),
* L’implémentation de la solution retenue,
* Des tests pour vérifier la conformité avec le cahier des charges,
* Les manquements et les améliorations possibles

##Développement 
###WEB
* Ce n’est pas le fait de faire des pages web (HTML5-CSS3) qui compte mais la taille de la DB et les services proposés sur celle-ci.
* Programmation côté client ET côté serveur.
###Mobile
* Justifier le choix d’une application mobile
* Justifier le choix de la plateforme et des technologies choisies
* Habituellement la synchronisation de données avec un serveur est exigée
* Application concrètement installée et installable (pas simulateur)
###Applicatif
Pour tous ceux qui ont une BD
* Schéma entités-associations et schéma relationnel
* Justification des choix DB : SQL, noSQL, ORM, logiciels

##Ressources
* Indiquer clairement les sources de toute ressource intellectuelle ou d’exploitation (site web, code source, schémas, livres, ..) utilisées dans le cadre du projet.

Autre Thème
