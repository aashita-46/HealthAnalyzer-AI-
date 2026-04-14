import requests

class NutritionLookup:

    def __init__(self, local_db_path=None, use_api=True):
        self.use_api = use_api

    def lookup(self, product_name, top_k=1):
        url = "https://world.openfoodfacts.org/cgi/search.pl"

        params = {
            "search_terms": product_name,
            "json": 1
        }

        try:
            res = requests.get(url, params=params, timeout=5)
            data = res.json()

            products = data.get("products", [])[:top_k]

            results = []
            for p in products:
                nutr = p.get("nutriments", {})

                results.append({
                    "product_name": p.get("product_name", "Unknown"),
                    "calories_per_100g": nutr.get("energy-kcal_100g", 0),
                    "protein_g": nutr.get("proteins_100g", 0),
                    "sugar_g": nutr.get("sugars_100g", 0),
                    "fiber_g": nutr.get("fiber_100g", 0),
                })

            return results

        except Exception as e:
            print("API Error:", e)
            return []