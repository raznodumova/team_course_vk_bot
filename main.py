import vk_api
import configparser
import time
from vk_api.longpoll import VkLongPoll, VkEventType

config = configparser.ConfigParser()
config.read('config.ini')  # отсюда токен достаем


# так значится, тут у нас класс вк бота
class VKBot:
    def __init__(self):
        self.vk = vk_api.VkApi(token=config['VK']['token'])  # сюда вставляем
        self.vk_user = vk_api.VkApi(token=config['VK']['user_token'])  # и сюда тоже
        self.longpoll = VkLongPoll(self.vk)  # слушаем сообщения

    # метод для получения информации о пользователе
    def get_user_info(self, user_id):
        return self.vk.method('users.get', {
            'user_ids': user_id,
            'fields': 'city, sex, bdate'
        })[0]

    # метод для отправки сообщения
    def send_message(self, user_id):
        user_info = self.get_user_info(user_id)
        name = user_info.get('first_name', 'Unknown')
        surname = user_info.get('last_name', 'Unknown')
        gender = 'female' if user_info.get('sex') == 1 else 'male' if user_info.get('sex') == 2 else 'unknown'
        city = user_info.get('city', {}).get('title', 'unknown') if user_info.get('city') else 'unknown'

        age_info = self.calculate_age(user_info.get('bdate'))
        message = (f"Имя: {name} {surname}\n"
                   f"Пол: {gender}\n"
                   f"Город: {city}\n"
                   f"Возраст: {age_info['age']} {age_info['message']}\n")

        # Получаем три самых популярных фотографии
        top_photos = self.get_top_photos(user_id)
        photo_attachments = []
        for photo in top_photos:
            attachment = f"photo{photo['owner_id']}_{photo['id']}"
            photo_attachments.append(attachment)

        attachments = ','.join(photo_attachments) if photo_attachments else ''
        self.vk.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'attachment': attachments,
            'random_id': 0
        })

    # метод для вычисления возраста (тут мне не нравится), но я пока не придумала, как по-другому
    @staticmethod
    def calculate_age(bdate):
        if not bdate:
            return {'age': 'unknown', 'message': 'Дата рождения не указана.'}

        bdate_parts = bdate.split('.')
        if len(bdate_parts) == 3:
            current_year = time.localtime().tm_year
            return {'age': current_year - int(bdate_parts[2]), 'message': ''}
        return {'age': 'не указан.', 'message': 'Год рождения не указан.'}

    def get_top_photos(self, user_id):
        response = self.vk_user.method('photos.get', {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 100  # Получаем максимум 100 фоток, хз, мб больше надо, мб меньше
        })

        photos = []
        for item in response['items']:
            photo = {
                'id': item['id'],
                'owner_id': item['owner_id'],
                'likes': item['likes']['count']
            }
            photos.append(photo)
        photos.sort(key=lambda x: x['likes'], reverse=True)
        return photos[:3]


if __name__ == '__main__':
    vk_bot = VKBot()
    # начинаем слушать сообщения
    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            vk_bot.send_message(event.user_id)
