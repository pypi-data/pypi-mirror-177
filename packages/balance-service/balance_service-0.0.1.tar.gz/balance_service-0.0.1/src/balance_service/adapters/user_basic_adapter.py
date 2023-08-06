from abc import abstractmethod


class UserBasicAdapter:
    @abstractmethod
    def create(self,
               surname: str,
               fullname: str,
               email: str,
               hashed_password: str):
        pass

    @abstractmethod
    def get_by_id(self, user_id: str):
        pass

    @abstractmethod
    def get_by_email(self, user_email: str):
        pass
