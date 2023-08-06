from abc import abstractmethod


class BankBasicAdapter:
    @abstractmethod
    def create(self,
               token: str,
               user_id: str):
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str):
        pass

