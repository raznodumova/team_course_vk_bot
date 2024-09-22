import psycopg2
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
import DB_conf as tables

Base = declarative_base()
engine = sa.create_engine(f"postgresql://postgres:admin@localhost:5432/vk_bots", echo=True).connect()
session = sessionmaker(binds={Base: engine, }, expire_on_commit=False)()

class DB:
    """Class for initialization and work with Data base"""
    def __init__(self, db_name, SU_pasword):
        # необходимо имя BD с которой будем работать, и пароль от суперпользователя
        self.password = SU_pasword
        self.db_name = db_name

    def connection(self):  # устанавливаем соединение
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=self.password,
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        return conn

    def create_db(self):  # создание новой БД
        with self.connection().cursor() as cur:
            try:
                cur.execute(f"CREATE DATABASE {self.db_name};")
                print("База данных успешно создана")
                self.connection().commit()
                self.connection().close()
            except psycopg2.errors.DuplicateDatabase:
                print("База данных уже существует")

    def create_tables(self):  # создаем новые таблицы
        Base.metadata.create_all(engine)

    def drop_tables(self):  # удаляем все из БД
        Base.metadata.drop_all(engine)

    def create_user(self, user):
        try:
            with session as s:
                s.add(user)
                s.commit()
                print("Пользователь Добавлен")

        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            print("Такой пользователь уже существует")

    # def delete_user(self, id):
    #     try:
    #         with self.session as s:
    #             user_to_delete = self.session.query(User).filter_by(user_id=id).first()
    #             s.delete(user_to_delete)
    #             s.commit()
    #     except psycopg2.errors.UniqueViolation:
    #         print("такой пользователь не существует")

    def crete_prompt(self, prompt):
        try:
            with session as s:
                s.add(prompt)
                s.commit()
                print("Запрос добавлен")

        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            print("Пользователь уже добавил запрос")

    def like(self, user, who_liked):
        try:
            with session as s:
                like = tables.Liked(user_id=user, liked_user_id=who_liked)
                s.add(like)
                s.commit()
                print("Лайк добавлен")

        except IntegrityError as e:
            print(e)

    def unlike(self, user, who_unliked):
        try:
            with session as s:
                unlike = tables.Liked(user_id=user, liked_user_id=who_unliked)
                s.delete(unlike)
                s.commit()
                print("Лайк добавлен")

        except IntegrityError as e:
            print(e)

    def ban(self, user, user_for_ban):
        try:
            with session as s:
                ban = tables.Banned(user_id=user, banned_user_id=user_for_ban)
                s.add(ban)
                s.commit()
                print("Бан добавлен")

        except IntegrityError as e:
            print(e)

    def unban(self, user, user_for_unban):
        try:
            with session as s:
                unban = s.query(tables.Banned).filter_by(user_id=user, banned_user_id=user_for_unban).first()
                # unban = T.Banned(user_id=user, banned_user_id=user_for_unban)
                s.delete(unban)
                s.commit()
                print("Бан добавлен")

        except IntegrityError as e:
            print(e)


if __name__ == "__main__":
    test_db = DB("vk_bots", "admin")
    try:
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
        # test_db.ban(22, 14)
        # test_db.unban(14,22)
        test = session.query(tables.User).all()
        print(test)
    except Exception as e:
        print(e)
