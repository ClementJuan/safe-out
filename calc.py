# calc.py

def calculer_couverture(gain_pot, mise_init, cote_couv, strategie, pct_profit=0):
    """
    Calcule la mise de couverture selon la stratégie choisie.
    """
    try:
        if cote_couv <= 1:
            return 0, "La cote doit être supérieure à 1."

        if strategie == "Gain Global (Sécurité Totale)":
            # Formule d'arbitrage classique : Mise = Gain / Cote
            mise_couv = gain_pot / cote_couv
            
        elif strategie == "Mise Uniquement (Breakeven)":
            # Formule pour couvrir uniquement la mise initiale
            # Mise_couv = Mise_init / (Cote_couv - 1)
            mise_couv = mise_init / (cote_couv - 1)
            
        elif strategie == "Mise + % de Profit":
            # On récupère la mise + un % du bénéfice net théorique
            profit_net_max = gain_pot - mise_init
            profit_a_securiser = (pct_profit / 100) * (profit_net_max / cote_couv)
            mise_couv = (mise_init / (cote_couv - 1)) + profit_a_securiser
        
        else:
            mise_couv = 0

        return round(mise_couv, 2), None

    except ZeroDivisionError:
        return 0, "Erreur de calcul (Cote invalide)."
