from datetime import datetime

from database import Session, User, UserQuery


class UserDatabase:

    def save_user_to_db(self, user_id: int, username: str, first_name: str,
                        last_name: str, active: bool, register_at: datetime):
        session = Session()
        if not self.check_if_user_exist(user_id=user_id):
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                active=active,
                register_at=register_at
            )
            session.add(user)
            session.commit()
            session.close()

    @staticmethod
    def check_if_user_exist(user_id: int):
        session = Session()
        user_exists = session.query(User).filter_by(user_id=user_id).first() is not None
        session.close()
        return user_exists


class UserQueryDatabase:

    @staticmethod
    def save_user_query(user_id: int, user_query: str):
        session = Session()
        user_query = UserQuery(
            user_id=user_id,
            user_query=user_query,
        )
        session.add(user_query)
        session.commit()
        session.close()