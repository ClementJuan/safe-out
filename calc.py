# calc.py

def calculer_couverture(gain_pot, mise_init, cote_couv, strategie, pct_profit=0):
    """
    Calcule la mise de couverture et les bénéfices associés.
    """
    try:
        if cote_couv <= 1:
            return None, "La cote doit être supérieure à 1."

        if strategie == "Gain Global (Sécurité Totale)":
            # Formule d'arbitrage : M_couv = Gain_Pot / Cote_Couv
            mise_couv = gain_pot / cote_couv
            
        elif strategie == "Mise Uniquement (Breakeven)":
            # Mise pour récupérer uniquement l'investissement initial
            mise_couv = mise_init / (cote_couv - 1)
            
        elif strategie == "Mise + % de Profit":
            # On sécurise la mise + une fraction du profit net restant
            profit_net_max = gain_pot - mise_init
            profit_a_securiser = (pct_profit / 100) * (profit_net_max / cote_couv)
            mise_couv = (mise_init / (cote_couv - 1)) + profit_a_securiser
        else:
            mise_couv = 0

        # Calcul des bénéfices pour l'interface
        total_investi = mise_init + mise_couv
        benef_si_combine = gain_pot - total_investi
        benef_si_couv = (mise_couv * cote_couv) - total_investi

        return {
            "mise_a_placer": round(mise_couv, 2),
            "total_investi": round(total_investi, 2),
            "benef_si_combine": round(benef_si_combine, 2),
            "benef_si_couv": round(benef_si_couv, 2),
            "benef_moyen": round((benef_si_combine + benef_si_couv) / 2, 2)
        }, None

    except ZeroDivisionError:
        return None, "Erreur : La cote de couverture est trop basse."
