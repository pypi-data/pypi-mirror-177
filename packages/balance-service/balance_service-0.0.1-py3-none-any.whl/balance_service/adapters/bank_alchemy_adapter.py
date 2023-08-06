from balance_service.adapters.bank_basic_adapter import BankBasicAdapter

from balance_domain.models.user_models import Bank
from balance_domain.database.settings import ConnectionDatabase


class BankAlchemyAdapter(
    ConnectionDatabase,
    BankBasicAdapter
):
    def __init__(self):
        super().__init__()

    def create(self,
               token: str,
               user_id: str):
        bank = Bank(
            token=token,
            user_id=user_id)
        self.session.add(bank)
        self.session.commit()
        self.session.refresh(bank)
        return bank

    def get_by_user_id(self, user_id: str):
        banks = self.session.query(Bank).filter(Bank.user_id == user_id).all()
        return banks
