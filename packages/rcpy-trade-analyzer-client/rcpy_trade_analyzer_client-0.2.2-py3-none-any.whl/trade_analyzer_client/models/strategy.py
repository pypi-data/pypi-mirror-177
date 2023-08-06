from .strategy_type import StrategyType
from .platform import Platform
from .commission_model import CommissionModel


class Strategy:

    def __init__(self, id: str, description: str, type: StrategyType, commission_model: CommissionModel, platform: Platform, currency: str) -> None:
        self.id: str = id
        self.description: str = description
        self.type: StrategyType = type 
        self.commission_model: CommissionModel = commission_model
        self.platform: Platform = platform
        self.currency: str = currency