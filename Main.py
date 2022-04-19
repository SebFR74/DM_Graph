
############################## Import des modules
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import sys
import os

############################## Fct Select_Fic - Sélectionne le fichier de config
def Select_Fic(Fen_Main):
    try:
        Fen_Main.Txt_Fic.delete(0, "end")
        Fen_Sel = tk.Tk()
        Fen_Sel.withdraw() # pour ne pas afficher la fenêtre Tk
        Nomfichier_Sel = askopenfilename() # lance la fenêtre de sélection
        print (Nomfichier_Sel)
        Fen_Main.Txt_Fic.insert(0,Nomfichier_Sel)
        Fen_Sel.destroy()

    except IndexError as e:
        print('Erreur Select_Fic : ', e)

############################## Fct Verif_SAT - Vérification du fichier de config
def Verif_SAT(Nomfichier_Sel,Fen_Main):
    global b_Est_SAT
    try:
        # Etape 1 : Lecture Fichier config + remplissage matrice
        if not (os.path.isfile(Nomfichier_Sel) & (os.path.exists(Nomfichier_Sel))):
            print ("Le fichier n'existe pas : " + Nomfichier_Sel)
            return True
        if Lecture_Fichier_Config(Nomfichier_Sel,Fen_Main):
            # Etape 2 : Affichage Tableau Principal avec les clauses
            print("Tableau_Principal ================================= ")
            print (Tableau_Principal)
            print ("================================================== ")
            # Etape 3 : Transposition matrice
            if Transpose_Tableau(int(Nb_Variable)*2+1): 
                # Etape 4 : Affichage Matrice Trasposée
                print("Tableau_Transpose ================================== ")
                print (Tableau_Transpose)
                print ("=================================================== ")
                # Etape 5 : Parcours Profondeur
                if Parcours_Profondeur(int(Nb_Variable)*2+1): 
                    # Etape 6 : Affichage du tableau des composantes
                    print("Tableau_Composante ================================= ")
                    print(Tableau_Composante)
                    print ("=================================================== ")
                    # Etape 7 : Parcours Profondeur Inversé
                    if Parcours_Profondeur_Inv(): 
                        # Etape 8 : Affichage du tableau des composantes Inv
                        print("Tableau_Composante_Transpose ======================= ")
                        print(Tableau_Composante_Transpose)
                        print ("=================================================== ")
                        # Etape 9 : Parcours Profondeur Inversé
                        b_Est_SAT = True
                        if Reponse_SAT(): 
                            # Etape 10 : Parcours pour trouver des littéraux opposés
                            print ("===================================================")
                            if b_Est_SAT : print("Resultat Final : Le fichier est SATisfiable !")
                            else : print("Resultat Final : Le fichier est IN-SATisfiable !")
                            return True
                        else:
                            print("Parcours_Profondeur_Inv a échouée")
                            return False
                    else:
                        print("Parcours_Profondeur_Inv a échouée")
                        return False
                else:
                    print("Parcours_Profondeur a échouée")
                    return False
            else:
                print("Transpose_Tableau a échouée")
                return False
        else:
            print("Le fichier config est incorrect")
            return False
    except IndexError as e:
        print('Erreur Verif_SAT  : ', e)
        return False

############################## Fct Lecture_Fichier_Config
############################## Vérification du fichier de config
############################## MAJ de la Matrice
def Lecture_Fichier_Config(Nomfichier_Sel,Fen_Main):
    global Tableau_Principal, Tableau_Transpose, Nb_Variable
    try:
        print("Nomfichier_Sel : " + str(Nomfichier_Sel))
        #Ouverture du fichier
        with open(Nomfichier_Sel, "r") as File_In:
            # Lecture Ligne 1
            Lignes_Lue = File_In.readline()
            while (Lignes_Lue != ""):
                # Test de toutes les lignes commentaire
                if (Lignes_Lue[0] == "c"): #Commentaire
                    Fen_Main.Txt_L1.delete(0, "end")
                    Fen_Main.Txt_L1.insert(0,Lignes_Lue)
                # Test de la ligne config
                elif (Lignes_Lue[0] == "p"): #Config
                    Fen_Main.Txt_L2.delete(0, "end")
                    Fen_Main.Txt_L2.insert(0,Lignes_Lue)
                    # Test si config OK
                    if (Lignes_Lue[0:6] == "p cnf "): # Config OK
                        Config_partie_2 = Lignes_Lue[6:-1] # -1 on en profite pour virer le CRLF
                        print("Config OK : " + Config_partie_2)
                        # Config OK - On charge les param - Nb de variables - Nb de clauses
                        Espace_Config_partie_2 = Config_partie_2.find(" ")
                        print("Espace_Config_partie_2 : " + str(Espace_Config_partie_2))
                        Nb_Variable = Config_partie_2[0:Espace_Config_partie_2]
                        Nb_Clause = Config_partie_2[Espace_Config_partie_2+1:len(Config_partie_2)]
                        print("Nb_Variable : " + Nb_Variable)
                        print("Nb_Clause : " + Nb_Clause)

                        ## A ce niveau on a toutes les infos, la suite est la iste des clauses.
                        ## On va donc créer a matrice sous forme d'un tableau
                        ## Les lignes / colonnes sont les Variables (Sommet)
                        ## Les valeurs de la matrice correspondent aux clauses (Arrêtes)
                        ## On va essayer de mettre l'origine au centre (ligne et colonne)
                        ## Et donc les valeurs positives seront à droite et les négatives à gauche
                        ## Pas de Pb pour la colonne/ligne 0 qui sera au centre

                        # On commence par tout mettre à zéro (Init tableau)
                        # Création des tableaux vides
                        Tableau_Principal = np.zeros((int(Nb_Variable)*2+1,int(Nb_Variable)*2+1), int)
                        Tableau_Transpose = np.zeros((int(Nb_Variable)*2+1,int(Nb_Variable)*2+1), int)

                        # Pour chaque Clause, on va mettre 1 dans la matrice
                        return Remplit_Tableau(Nb_Clause, File_In)
                    else:
                        return False
                else:
                    print ("Erreur fichier config : Lignes_Lue = " + Lignes_Lue)
                    return False

                ## Lecture ligne suivante
                # #print(Lignes_Lue)
                Lignes_Lue = File_In.readline()
        return False

    except IndexError as e:
        print('Erreur Lecture_Fichier_Config  : ', e)
        return False

############################## Fonction Remplit_Tableau
def Remplit_Tableau(Nb_Clause, File_In):
    global Tableau_Principal, Tableau_Transpose, Nb_Variable
    try:
        for i_Clause_Lue in range(int(Nb_Clause)):
            ######################## Lecture et décomposition de la clause
            Clause_Lue = File_In.readline()
            # print("Clause_Lue : " + Clause_Lue)
            Espace_1_Clause = Clause_Lue.find(" ")
            Litteral_1 = Clause_Lue[0:Espace_1_Clause]
            # print("Litteral_1 : " + Litteral_1)
            Reste_Clause = Clause_Lue[Espace_1_Clause+1:len(Clause_Lue)]
            # print("Reste_Clause : " + Reste_Clause)
            Espace_2_Clause = Reste_Clause.find(" ")
            Litteral_2 = Reste_Clause[0:Espace_2_Clause]
            # print("Litteral_2 : " + Litteral_2)
            Caract_fin = Reste_Clause[Espace_2_Clause+1:-1]
            # print("Caract_fin : " + Caract_fin)
            if (Caract_fin != "0"):
                return False
            print("L1 : " + Litteral_1 + " - L2 : " + Litteral_2 + " - Fin : " + Caract_fin)
            ######################## Ajout des 2 valeurs dans la matrice
            # Calcul pour positionner la ligne / colonne : 
            # Notre 0 est au centre donc à la position (Nb_Variable + 1)/2
            # il suffit d'ajouter ensuite la valeur de la clause (positive ou négative)
            
            # Non L1 et L2 ==> (Clause_X) x (-1)
            Clause_X = int(Nb_Variable) + int(Litteral_1)*(-1)
            Clause_Y = int(Nb_Variable) + int(Litteral_2)
            print("1 - Clause_X : " + str(Clause_X) + " - Clause_Y : " +  str(Clause_Y))
            Tableau_Principal[int(Clause_X)][int(Clause_Y)] = 1
            #print (Tableau_Principal)
            # L1 et Non L2 ==> (Clause_Y) x (-1)
            Clause_X = int(Nb_Variable) + int(Litteral_1)
            Clause_Y = int(Nb_Variable) + int(Litteral_2)*(-1)
            print("2 - Clause_X : " + str(Clause_X) + " - Clause_Y : " +  str(Clause_Y))
            Tableau_Principal[int(Clause_X)][int(Clause_Y)] = 1

        return True
    except IndexError as e:
        print('Erreur Remplit_Tableau : ', e)
        return False

############################## Fonction def Transpose_Tableau():
def Transpose_Tableau(Nb_Val_Tab):
    global Tableau_Principal, Tableau_Transpose, Nb_Variable
    try:
        # On transpose dans un tableau (i <=> j)
        for i in range(Nb_Val_Tab):
            for j in range(Nb_Val_Tab):
                Tableau_Transpose[i][j] = Tableau_Principal[j][i]

        return True

    except IndexError as e:
        print('Erreur Transpose_Tableau : ', e)
        return False

############################## Fonction def Parcours_Profondeur():
def Parcours_Profondeur(Nb_Val_Tab):
    global Tableau_Principal, Tableau_Transpose, Nb_Variable, Liste_parcourus, Tableau_Composante, Liste_Composante

    try:
        # On Vide la liste des Variables déjà parcourus
        Liste_parcourus = []
        Liste_Composante = []

        # On parcours la liste des Variables A parcourir
        print("Nb_Val_Tab = " + str(Nb_Val_Tab))
        for Nb_Val_Tab_En_Cours in range(Nb_Val_Tab):
            print("Nb_Val_Tab_En_Cours ========================= " + str(Nb_Val_Tab_En_Cours))
            # On cherche si la variable a déjà été parcourue
            if Nb_Val_Tab_En_Cours not in Liste_parcourus:
                #print("Nb_Val_Tab_En_Cours n'est pas parcourus")
                # On ajoute si la variable a déjà été parcourue
                Liste_parcourus.append(Nb_Val_Tab_En_Cours)
                # On ajoute à la liste de la composante en cours
                Liste_Composante.append(Nb_Val_Tab_En_Cours)

                # On Parcours la colonne de la clause trouvée
                Parcours_Vertical(Nb_Val_Tab_En_Cours)

                # On ajoute la composante en cours à la liste Tableau_Composante
                print("Liste_Composante = " + str(Liste_Composante))
                Tableau_Composante.append(Liste_Composante)
                #print("Tableau_Composante = ")
                #print(Tableau_Composante)

                # On efface la liste de la composante en cours pour la nouvelle
                Liste_Composante = []

        return True

    except IndexError as e:
        print('Erreur Parcours_Profondeur : ', e)
        return False

############################## Fonction def Parcours_Profondeur_Inv():
def Parcours_Profondeur_Inv():
    global Tableau_Principal, Tableau_Transpose, Nb_Variable, Liste_parcourus, Tableau_Composante, Tableau_Composante_Transpose, Liste_Composante

    try:
        # On Vide la liste des Variables déjà parcourus
        Liste_parcourus = []
        Liste_Composante = []
        Tableau_Composante_Transpose = []

        for Lst_Tab_En_Cours in reversed(Tableau_Composante):
            print(Lst_Tab_En_Cours)
            for Val_Tab_En_Cours in (Lst_Tab_En_Cours):
                print(Val_Tab_En_Cours)

                print("Val_Tab_En_Cours ========================= " + str(Val_Tab_En_Cours))
                # On cherche si la variable a déjà été parcourue
                if Val_Tab_En_Cours not in Liste_parcourus:
                    #print("Nb_Val_Tab_En_Cours n'est pas parcourus")
                    # On ajoute si la variable a déjà été parcourue
                    Liste_parcourus.append(Val_Tab_En_Cours)
                    # On ajoute à la liste de la composante en cours
                    Liste_Composante.append(Val_Tab_En_Cours)

                    # On Parcours la colonne de la clause trouvée
                    Parcours_Vertical_Transpose(Val_Tab_En_Cours)

                    # On ajoute la composante en cours à la liste Tableau_Composante
                    print("Liste_Composante = " + str(Liste_Composante))
                    Tableau_Composante_Transpose.append(Liste_Composante)
                    #print("Tableau_Composante_Transpose = ")
                    #print(Tableau_Composante_Transpose)

                    # On efface la liste de la composante en cours pour la nouvelle
                    Liste_Composante = []

        return True

    except IndexError as e:
        print('Erreur Parcours_Profondeur : ', e)
        return False

############################## Fonction def Reponse_SAT():
def Reponse_SAT():
    global Nb_Variable, Tableau_Composante_Transpose, b_Est_SAT

    try:
        print("b_Est_SAT_0 = " + str(b_Est_SAT))
        for Lst_Tab_En_Cours in (Tableau_Composante_Transpose):
            for Val_Tab_En_Cours in (Lst_Tab_En_Cours):
                print("Val_Tab_En_Cours = " + str(Val_Tab_En_Cours))
                # Calcul du complément
                Calcul_Complement = int(Nb_Variable)*2-int(Val_Tab_En_Cours)
                print("Calcul_Complement = " + str(Calcul_Complement))
                if (Calcul_Complement != Val_Tab_En_Cours): # Cas du 0 qui a le même complément
                    if (Calcul_Complement in Lst_Tab_En_Cours): b_Est_SAT = False
                    print("b_Est_SAT = " + str(b_Est_SAT))

        return True

    except IndexError as e:
        print('Erreur Reponse_SAT : ', e)
        return False

############################## Fonction def Parcours_Vertical():
def Parcours_Vertical(Nb_Val_Tab_Param):
    global Tableau_Principal, Tableau_Transpose, Nb_Variable, Liste_parcourus, Tableau_Composante, Liste_Composante
    
    try:
        # On parcours la liste des Variables à visiter
        #print("Parcours_Vertical !")
        for Nb_Val_Tab_En_Cours in range(int(Nb_Variable)*2+1):
            #print("Nb_Val_Tab_Param = " + str(Nb_Val_Tab_Param))
            #print("Nb_Val_Tab_En_Cours = " + str(Nb_Val_Tab_En_Cours))
            #print("Tableau_Principal = " + str(Tableau_Principal[Nb_Val_Tab_Param][Nb_Val_Tab_En_Cours]))
            if Tableau_Principal[Nb_Val_Tab_Param][Nb_Val_Tab_En_Cours] == 1:
                #print("Tableau_Principal = 1 - As-t'il été parcourus ?")
                # On cherche si la variable a déjà été parcourue
                if Nb_Val_Tab_En_Cours not in Liste_parcourus:
                    #print("Non pas parcourus donc on ajoute au liste !")
                    # On ajoute si la variable a déjà été parcourue
                    Liste_parcourus.append(Nb_Val_Tab_En_Cours)
                    Liste_Composante.append(Nb_Val_Tab_En_Cours)
                    #print("Et on refait un parcours Vertical !")
                    Parcours_Vertical(Nb_Val_Tab_En_Cours)

    except IndexError as e:
        print('Erreur Parcours_Vertical : ', e)
        return False

############################## Fonction def Parcours_Vertical_Transpose():
def Parcours_Vertical_Transpose(Nb_Val_Tab_Param):
    global Tableau_Principal, Tableau_Transpose, Nb_Variable, Liste_parcourus, Tableau_Composante, Liste_Composante
    
    try:
        # On parcours la liste des Variables à visiter
        #print("Parcours_Vertical !")
        for Nb_Val_Tab_En_Cours in range(int(Nb_Variable)*2+1):
            #print("Nb_Val_Tab_Param = " + str(Nb_Val_Tab_Param))
            #print("Nb_Val_Tab_En_Cours = " + str(Nb_Val_Tab_En_Cours))
            #print("Tableau_Principal = " + str(Tableau_Principal[Nb_Val_Tab_Param][Nb_Val_Tab_En_Cours]))
            if Tableau_Transpose[Nb_Val_Tab_Param][Nb_Val_Tab_En_Cours] == 1:
                #print("Tableau_Principal = 1 - As-t'il été parcourus ?")
                # On cherche si la variable a déjà été parcourue
                if Nb_Val_Tab_En_Cours not in Liste_parcourus:
                    #print("Non pas parcourus donc on ajoute au liste !")
                    # On ajoute si la variable a déjà été parcourue
                    Liste_parcourus.append(Nb_Val_Tab_En_Cours)
                    Liste_Composante.append(Nb_Val_Tab_En_Cours)
                    #print("Et on refait un parcours Vertical !")
                    Parcours_Vertical_Transpose(Nb_Val_Tab_En_Cours)

    except IndexError as e:
        print('Erreur Parcours_Vertical_Transpose : ', e)
        return False

############################## Fct Main principale
def Main():
    global Tableau_Principal, Tableau_Transpose, Nb_Variable, Liste_parcourus, Tableau_Composante, Tableau_Composante_Transpose, Liste_Composante, b_Est_SAT
    try:
        Tableau_Principal = []
        Tableau_Transpose = []
        Liste_parcourus = []
        Tableau_Composante = []
        Tableau_Composante_Transpose = []
        Liste_Composante = []
        Nb_Variable = 0
        b_Est_SAT = True

        # Création de la fenêtre
        Fen_Main = tk.Tk()
        Fen_Main.geometry("500x500")
        Fen_Main.title ("DM Graph")

        ## Ajout d'un bouton Select ##
        Fen_Main.Bouton_Select = tk.Button(Fen_Main, text="Fichier", command=lambda:[Select_Fic(Fen_Main)])
        Fen_Main.Bouton_Select.place(x=10,y=10,width=100)

        ## Ajout d'un bouton Verif_SAT ##
        Fen_Main.Bouton_Verif = tk.Button(Fen_Main, text="Verif", command=lambda:[Verif_SAT(Fen_Main.Txt_Fic.get(),Fen_Main)])
        Fen_Main.Bouton_Verif.place(x=10,y=40,width=100)

        ## Ajout d'un bouton Fin ##
        Fen_Main.Bouton_Quit = tk.Button(Fen_Main, text="Quit", command=Fen_Main.destroy)
        Fen_Main.Bouton_Quit.place(x=400,y=470,width=90)

        ## Ajout d'un Champ Fichier ##
        Fen_Main.Txt_Fic = tk.Entry(Fen_Main)
        Fen_Main.Txt_Fic.place(x=130,y=10,width=350,height=25)
 
        ## Ajout d'un Champ Ligne 1 ##
        Fen_Main.Txt_L1 = tk.Entry(Fen_Main)
        Fen_Main.Txt_L1.place(x=130,y=40,width=350,height=25)

        ## Ajout d'un Champ Ligne 2##
        Fen_Main.Txt_L2 = tk.Entry(Fen_Main)
        Fen_Main.Txt_L2.place(x=130,y=70,width=350,height=25)

        if len(sys.argv) == 1:
            ## Lancement de la fenetre car 1 seul param
            print("Pas d'argument ==> on lancera l'IHM")
            Fen_Main.mainloop()
        elif len(sys.argv) == 2:
            ## Lancement auto si 2ème Param
            print("2ème Argument trouvé ==> on lancera la verif direct avec " + sys.argv[1])
            Fen_Main.Txt_Fic.insert(0,sys.argv[1])
            Verif_SAT(sys.argv[1],Fen_Main)
        else:
            print("Erreur Nb Argument")
            return


    except IndexError as e:
        print('Erreur Main  : ', e)

############################## Lancement du Main
if (__name__ == "__main__"):
    Main()

