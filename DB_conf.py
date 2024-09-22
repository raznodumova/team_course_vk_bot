from sqlalchemy import Column, Text, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
Base = declarative_base()
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

engine = sa.create_engine(f"postgresql://postgres:admin@localhost:5432/vk_bots", echo=True).connect()
session = sessionmaker(binds={Base: engine, }, expire_on_commit=False)()

# Создаем таблицы
class User(Base):
    __tablename__ = "user"

    user_id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    gender = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)

    prompts = relationship("UserPrompt", backref="user", cascade="all, delete")
    ban = relationship("Banned", backref="user", cascade="all, delete")
    like = relationship("Liked", backref="user", cascade="all, delete")

class UserPrompt(Base):
    __tablename__ = "user_prompt"

    # id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Text, ForeignKey("user.user_id"), nullable=False, unique=True, primary_key=True)
    city = Column(Text, nullable=False)
    gender = Column(Text, nullable=False)
    age = Column(Integer, nullable=False)


class Liked(Base):
    __tablename__ = "liked"

    option_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Text, ForeignKey("user.user_id"), nullable=False)
    liked_user_id = Column(Text, nullable=False)

    UniqueConstraint("user_id", "liked_user_id", name="uq_like")

class Banned(Base):
    __tablename__ = "banned"

    option_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Text, ForeignKey("user.user_id"), nullable=False)
    banned_user_id = Column(Text, nullable=False)

    UniqueConstraint("user_id", "banned_user_id", name="uq_ban")



if __name__ == "__main__":
    pass
    # test_db = DB("vk_bots", "admin")
    # try:
        # New_User = User(user_id=14, name="Vanya", city="moskow", gender="male", age=26)
        # test_db.delete_user(New_User)
        # test_db.drop_tables()
        # test_db.create_tables()
        # test_db.create_user(New_User)
        # new_prompt = UserPrompt(user_id=14, city="almaty", gender="female" , age="20")
        # test_db.crete_prompt(new_prompt)
        # user_2 = User(user_id=22, name="Masha", city="almaty", gender="female", age=20)
        # test_db.create_user(user_2)
        # test_db.like(14, 22)
        # test_db.unban(14,22)
    # except Exception as e:
    #     print(e)

    # create_db()
    # create_tables(main_engine)


    # New_User = User(user_id="masha", name="masha", city="moskow", gender="male", age=16))


test = session.query(User).filter_by(14, 22)
print(test)