import psycopg2
import requests

try:
    #connexion à la bdd
   connection = psycopg2.connect(user="tepau",
                                  password="tEPAU1992",
                                  host="",
                                  port="5432",
                                  database="lastpurbeurre")
    #Création curseur
   cursor = connection.cursor()
   
    # Sélection des produits en bdd enregistrement des pdt dans variable all_products_in_db
   postgres_insert_query = """ SELECT * FROM off_product; """
   cursor.execute(postgres_insert_query)
   all_products_in_db = cursor.fetchall()
   
   # Pour chaque produit recheche via api grace à nom du produit
   for product in all_products_in_db:
        api = 'https://fr.openfoodfacts.org/cgi/search.pl'
        config = {
            'action': 'process',
            'search_terms': product[2],
            'json': 1
        }
        response = requests.get(api, params=config)
        results = response.json()
        recovered_products = results['products']
        
        # Analyse de la réponse de l'api
        for recovered_product in recovered_products:
            #Si l'url correspond, on enregistre le produit dans la variable product_actualize
            if recovered_product['url'] == product[4]:
                product_actualize = [recovered_product['nutrition_grade_fr'], recovered_product['product_name_fr'], recovered_product['image_url'], recovered_product['url']]
                nutriscore = product_actualize[0]
                name = product_actualize[1]
                url_image = product_actualize[2]
                url_link = product_actualize[3]
                
                #Nouvelle recherche en bdd en fonction de url_LINK
                postgres_query = """ SELECT * FROM off_product WHERE url_link = (%s);"""
                cursor.execute(postgres_query, (url_link,))
                pdt = cursor.fetchone()
                if pdt[1] != nutriscore:
                    sql = """ UPDATE off_product
                    SET nutriscore = %s
                    WHERE url_link = %s"""
                    cursor.execute(sql, (nutriscore, url_link) )
                if pdt[2] != name:
                    sql = """ UPDATE off_product
                    SET name = %s
                    WHERE url_link = %s"""
                    cursor.execute(sql, (name, url_link) )
                if pdt[3] != url_image:
                    sql = """ UPDATE off_product
                    SET url_image = %s
                    WHERE url_link = %s"""
                    cursor.execute(sql, (url_image, url_link) )
                
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()

