

# Import des modules
# import Fenetres as Fen
# import Global as Global

# Fct Main principale
def Main():
    try:
        Tableau_Principal = []
        
        config = configparser.ConfigParser()
        config.sections()
        config.read('Param.ini')
        config.sections()
        'Dimension' in config
        Global.X_TAB = int(config['Dimension']['X_TAB'])
        Global.Y_TAB = int(config['Dimension']['Y_TAB'])
        Global.Taille_Case = int(config['Dimension']['Taille_Case'])
        'Dimension' in config
        Global.Vitesse_Base = int(config['Niveau']['Vitesse_Base'])


    except IndexError as e:
        print('Erreur Init_Param  : ', e)

if __name__ == "__main__" :
    Main()

