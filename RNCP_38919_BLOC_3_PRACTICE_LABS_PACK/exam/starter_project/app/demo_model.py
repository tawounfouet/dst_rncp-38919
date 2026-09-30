class DemoRiskModel:
    """Tiny deterministic model used only by the practice pack."""

    def predict(self, rows):
        outputs = []
        for distance_km, package_weight_kg in rows:
            score = float(distance_km) + 2 * float(package_weight_kg)
            outputs.append(int(score >= 20))
        return outputs
