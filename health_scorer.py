class HealthScorer:

    def score_product(self, p):
        score = (
            p.get("protein_g", 0) * 4 +
            p.get("fiber_g", 0) * 3 -
            p.get("sugar_g", 0) * 2.5 -
            (p.get("calories_per_100g", 0) / 20)
        )

        score = max(0, min(100, (score + 25) * 1.8))

        return {**p, "health_score": round(score, 1)}

    def rank_products(self, products):
        return sorted(
            [self.score_product(p) for p in products],
            key=lambda x: x["health_score"],
            reverse=True
        )