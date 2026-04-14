from detector import ShelfProductDetector
from ocr_reader import ProductOCR
from nutrition_lookup import NutritionLookup
from health_scorer import HealthScorer

class ShelfAnalysisPipeline:

    def __init__(self, model_path):
        self.detector = ShelfProductDetector(model_path)
        self.ocr = ProductOCR()
        self.nutrition = NutritionLookup()
        self.scorer = HealthScorer()

    def analyze(self, image_path):
        detections = self.detector.detect(image_path)
        detections = detections[:5]

        products = []

        for det in detections:
            name = self.ocr.read_product_name(det["crop"])

            if not name:
                continue

            results = self.nutrition.lookup(name, top_k=1)

            if results:
                products.append(results[0])

        ranked = self.scorer.rank_products(products)

        return {
            "total_products": len(ranked),
            "ranked_products": ranked,
            "best_pick": ranked[0] if ranked else None
        }