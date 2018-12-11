# Mes rubriques favorites #
# Version 2.0-dev #

*	 Auteurs : Abderrahim, Abdellah, Abdelkrim.
*	 télécharger [version stable](https://github.com/abdel792/myFavoriteTopics/releases/download/v2.0/myFavoriteTopics-2.0.nvda-addon)
*	 télécharger [version de développement](https://github.com/abdel792/myFavoriteTopics/releases/download/v2.0-dev/myFavoriteTopics-2.0-dev.nvda-addon)

Cet addon devrait vous permettre d'afficher et de consulter vos rubriques favorites.

Il devrait ajouter un item dans le menu "Outils" de NVDA intitulé "Mes rubriques favorites", qui devrait vous ouvrir une boîte de dialogue composée de 5 boutons :

* Un bouton "Afficher mes sites web favoris", pour afficher la liste de vos sites web favoris.
* Un bouton "Afficher mes applications favorites", pour afficher la liste de vos applications et répertoires favoris présents sur votre PC.
* Un bouton "Afficher mes contacts favoris", pour afficher la liste de vos contacts favoris.
* Un bouton "Afficher mes journaux favoris", pour afficher la liste de vos journaux favoris.
* Un bouton "Fermer", pour refermer la boîte de dialogue.

## Notes ##

* Vous pourrez refermer cette boîte de dialogue juste en pressant sur la touche d'échappement.
* Vous pourrez assigner un raccourci clavier pour ouvrir cette boîte de dialogue dans le menu "Gestes de commandes" et plus précisément, dans la catégorie "Outils".

## Pour naviguer parmi les éléments de la liste ##

Lorsque vous presser sur l'un des boutons correspondant à une rubrique, vous devriez avoir une boîte de dialogue composée des éléments suivants :

* Une liste d'items, parmi lesquels vous pourrez circuler avec vos flèches verticales.
* Un bouton "Ouvrir", qui devrait vous permettre d'accéder au contenu de l'item sélectionné dans la liste.
* Un bouton "Ajouter un nouveau groupe", qui devrait vous permettre d'ajouter un nouveau groupe dans la liste.
* Un bouton "Ajouter une nouvelle clé", qui devrait vous permettre d'ajouter une nouvelle clé dans la liste.
* Un bouton "Renommer le groupe", qui devrait vous permettre de renommer le groupe sélectionné dans la liste. (Cet item ne s'affiche que si l'élément sélectionné est un groupe)
* Un bouton "Renommer la clé", qui devrait vous permettre de renommer la clé sélectionnée dans la liste. (Cet item ne s'affiche que si l'élément sélectionné est une clé)
* Un bouton "Modifier la valeur", qui devrait vous permettre de modifier la valeur de la clé correspondant à l'item sélectionné dans la listge. (Cet item ne s'affiche que si l'élément sélectionné est une clé)
* Un bouton "Déplacer vers un groupe", qui devrait vous permettre de déplacer la clé sélectionnée dans la liste vers un groupe. (Cet item ne s'affiche que si l'élément sélectionné est une clé)
* Un bouton "Supprimer", qui devrait vous permettre de supprimer l'élément sélectionné dans la liste. Si l'élément est un groupe, tout le contenu de ce groupe sera supprimé.
* Un bouton "Fermer", pour refermer la boîte de dialogue.

## Notes ##

* Vous pourrez presser la touche d'échappement pour refermer chacune de ces boîtes de dialogue, et revenir ainsi à la boîte de dialogue présentant les boutons d'accès aux rubriques.
* Lorsque vous circulez dans la liste des items, si vous êtes sur un groupe, son nom devrait être suffixé par le terme (Groupe).
* Si vous ouvrez un groupe, vous devriez atterrir dans la liste des clés que contient ce groupe.
* Vous pourrez assigner un raccourci clavier pour ouvrir chacune des  boîtes de dialogue citées dans les chapitres précédents, dans le menu "Gestes de commandes" et plus précisément, dans la catégorie "Outils".
* Lorsqu'aucun item n'est présent dans la liste, seuls les bouton "Ajouter un groupe"", ""Ajouter une clé"" et "Fermer" sont proposés."

## Changements pour la version 2.0 ##

*	 Correction d'un bug qui survenait après la fermeture de la boîte de dialogue des rubriques favorites et qui empêchait sa réouverture sans relancer NVDA.

## Changements pour la version 1.2. ##

* Cette version apporte la compatibilité de l'extension avec wxPython version 4, notamment pour les boîtes de dialogue de modification et renommage des clés pour chaque rubrique;

## Changements pour la version 1.1. ##

* Cette version ajoute la possibilité de créer et de gérer des groupes de sous-rubriques.
* Dans la rubrique "Afficher mes contacts favoris", les informations du contact sont affichées dans une fenêtre de type texte, pour faciliter la copie.
* Désormais, dans la rubrique "Mes contacts favoris", les valeurs entrées pour chaque contact sont multilignes.

## Changements pour la version 1.0. ##

* version initiale.
