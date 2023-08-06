from balance_service.adapters.user_basic_adapter import UserBasicAdapter

from balance_domain.models.user_models import User
from balance_domain.database.settings import ConnectionDatabase


class UserAlchemyAdapter(
    UserBasicAdapter,
    ConnectionDatabase,
):
    def __init__(self):
        super().__init__()

    def create(self,
                surname: str,
                fullname: str,
                email: str,
                hashed_password: str):
        user = User(
            surname=surname,
            fullname=fullname,
            email=email,
            hashed_password=hashed_password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: str):
        user = self.session.query(User).filter(User.id == user_id).first()
        return user

    def get_by_email(self, user_email: str):
        user = self.session.query(User).filter(User.email == user_email).first()
        return user
