import requests
def no_doublons(liste_de_produits):
    liste_produits_final = []
    for produit in (liste_de_produits):
        if len(liste_produits_final) > 0:
            if produit not in liste_produits_final:
                nom_produit = []
                for produits in liste_produits_final:
                    nom_produit.append(produits[1])
                if produit[1] not in nom_produit:
                    liste_produits_final.append(produit)
        else:
            liste_produits_final.append(produit)
    return liste_produits_final


def clean_list(liste):
    for i, elt in enumerate(liste):
        if elt[ 0 ] == " ":
            elt = elt[ 1: ]
            liste[ i ] = elt
    return liste

class OpenFoodFacts:

    def __init__(self, liste_categories):
        self.liste_categories = liste_categories

    @staticmethod
    def clean_cat(liste_cat_produit, liste_cat):
        final_liste = [ ]
        liste = clean_list(liste_cat_produit)
        for categorie in liste:
            if categorie in liste_cat:
                final_liste.append(categorie)
        return final_liste

    @staticmethod
    def valid_product(keys, all_products):
        for key in keys:
            if key not in all_products:
                return False
        return True

    def get_selected_product(self):
        all_products = []
        for categorie in self.liste_categories:
            api = 'https://fr.openfoodfacts.org/cgi/search.pl'
            config = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': categorie,
                'tagtype_1': 'brands',
                'tag_contains_1': 'does_not_contains',
                'tag_1': 'Nutella',
                'page_size': 10,
                'json': 1
            }
            response = requests.get(api, params=config)
            results = response.json()
            all_products.extend(results['products'])

        selected_products = []
        keys = ('nutrition_grade_fr', 'product_name_fr', 'categories', 'image_url', 'url')

        for product in all_products:
            if self.valid_product(keys, product):
                cat = self.clean_cat(product['categories'].split(","), self.liste_categories)
                nutriscore = product['nutrition_grade_fr']
                nom = product['product_name_fr']
                image_url = product['image_url']
                url_link = product['url']

                key = [nutriscore, nom, cat, image_url, url_link]
                selected_products.append(key)


        final_products_list = no_doublons(selected_products)


        return final_products_list

if __name__ == '__main__':
    
    from off.thetest import OpenFoodFacts
    from off.models import Category, Product

    liste_categories = [ 'Produits à tartiner', 'Petit-déjeuners', 'Produits à tartiner sucrés', 'Pâtes à tartiner',
                         'Pâtes à tartiner aux noisettes', 'Pâtes à tartiner au chocolat',
                         'Pâtes à tartiner aux noisettes et au cacao' ]

    produits = OpenFoodFacts(liste_categories).get_selected_product()

    for categorie in liste_categories:
        Category.objects.create(name=categorie)

    for produit in produits:
        element = Product.objects.create(name=produit[1].lower(), nutriscore=produit[0], url_image=produit[3], url_link=produit[4])
        for cat in produit[2]:
            element.category.add(Category.objects.get(name=cat))
            element.save()




