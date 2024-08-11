import requests

def obtenir_categories(titre):
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": titre,
        "prop": "categories",
        "format": "json",
        "cllimit": "max"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        categories = []
        
        for page_id, page_data in pages.items():
            if "categories" in page_data:
                for category in page_data["categories"]:
                    categories.append(category["title"])
        
        return categories
    else:
        print(f"Erreur HTTP {response.status_code} lors de l'appel à l'API.")
        return []

def est_personne_humaine(titre):
    categories = obtenir_categories(titre)
    
    # Filtrer par des catégories typiques des personnes humaines
    categories_humaines = ["Catégorie:Personnalité", "Catégorie:Biographie", "Catégorie:Naissance"]
    
    for categorie in categories:
        for cat_hum in categories_humaines:
            if cat_hum in categorie:
                return True
    return False

def obtenir_liens_personnes(titre):
    liens = obtenir_liens_article(titre)
    liens_personnes = []
    
    for lien in liens:
        if est_personne_humaine(lien):
            liens_personnes.append(lien)
    
    return liens_personnes

def obtenir_liens_article(titre):
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": titre,
        "prop": "links",
        "format": "json",
        "pllimit": "max"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        liens = []
        
        for page_id, page_data in pages.items():
            if "links" in page_data:
                for link in page_data["links"]:
                    liens.append(link["title"])
        
        return liens
    else:
        print(f"Erreur HTTP {response.status_code} lors de l'appel à l'API.")
        return []

def rechercher_sur_wikipedia(nom):
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": nom,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if "query" in data and "search" in data["query"]:
            resultats = data["query"]["search"]
            
            if resultats:
                print(f"Résultats de recherche pour '{nom}':")
                tous_les_liens_personnes = {}
                
                for resultat in resultats:
                    titre = resultat['title']
                    print(f"Recherche des liens pour l'article: {titre}")
                    
                    liens_personnes = obtenir_liens_personnes(titre)
                    tous_les_liens_personnes[titre] = liens_personnes
                    
                print("\nLiens cliquables vers des personnes humaines extraits :")
                for titre, liens in tous_les_liens_personnes.items():
                    print(f"\nArticle: {titre}")
                    for lien in liens:
                        print(f"- {lien}")
                
                return tous_les_liens_personnes
            else:
                print(f"Aucun résultat trouvé pour '{nom}'.")
        else:
            print("Erreur dans les données reçues de l'API.")
    else:
        print(f"Erreur HTTP {response.status_code} lors de l'appel à l'API.")
        return {}

# Demander à l'utilisateur de saisir un nom propre
nom_propre = input("Entrez le nom propre à rechercher sur Wikipédia: ")

# Rechercher et afficher les résultats
liens_personnes = rechercher_sur_wikipedia(nom_propre)
