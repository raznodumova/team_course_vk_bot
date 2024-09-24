from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm import sessionmaker
from tables import engine, User, Liked, UserPrompt, Banned

s = sessionmaker(engine)()

def create_user(user):
    try:
        s.add(user)
        s.commit()
        print("Пользователь Добавлен")

    except IntegrityError:
        print("Такой пользователь уже существует")

def update_user():
    pass

def delete_user(user_id):
    try:
        user_to_delete = s.query(User).filter_by(user_id=user_id).first()
        s.delete(user_to_delete)
        s.commit()
        print("Пользователь удален")
    except UnmappedInstanceError:
        print("такой пользователь не существует")

def add_prompt(prompt):
    try:
        s.add(prompt)
        s.commit()
        print("Запрос добавлен")

    except IntegrityError:
        print("Пользователь уже добавил запрос")

def update_prompt():
    pass

def like(user_id, liked_user_id):
    try:
        s.add(Liked(user_id=user_id, liked_user_id=liked_user_id))
        s.commit()
        print("Лайк добавлен")

    except IntegrityError:
        print("Лайк уже существует")

def unlike(user_id, user_for_unlike):
    s.delete(Liked(user_id=user_id, liked_user_id=user_for_unlike))
    s.commit()
    print("Лайк убран")

def ban(user_id, user_for_ban):
    try:
        s.add(Banned(user_id=user_id, banned_user_id=user_for_ban))
        s.commit()
        print("Бан добавлен")

    except IntegrityError:
        print("Бан уже существует")

def unban(user_id, user_for_unban):
    s.delete(s.query(Banned).filter_by(user_id=user_id, banned_user_id=user_for_unban).first())
    s.commit()
    print("Бан Убран")


if __name__ == "__main__":
    pass

    # минии тесты
    # test = DB("vk_bots", "admin")
    # New = User(user_id=14, name="Vanya", city="moskow", gender="male", age=26)
    # create_user(New)
    # delete_user(user_id="14")
