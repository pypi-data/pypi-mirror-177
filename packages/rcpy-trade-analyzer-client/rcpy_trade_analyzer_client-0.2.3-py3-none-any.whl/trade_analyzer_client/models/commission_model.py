from .commission_rule import CommissionRule

class CommissionModel:

    def __init__(self, commission_rule: CommissionRule, pricing: float) -> None:
        self.commission_rule: CommissionRule = commission_rule
        self.pricing: float = pricing