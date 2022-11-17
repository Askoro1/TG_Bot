import telebot
from telebot import types

TOKEN = input()
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id, "Всем привет ✌")


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    user_name = message.new_chat_members[0].username
    bot.send_message(message.chat.id, "Добро пожаловать в этот чат, @" + user_name + '!')
    bot.send_message(message.chat.id, "Как твои дела сегодня, @" + user_name + "?",
                     reply_markup=types.ForceReply(selective=True))
    bot.register_next_step_handler(message, message_reply, message.new_chat_members[0].id)


def message_reply(message, new_user):
    if message.from_user.id == new_user:
        bot.reply_to(message, 'Понятно! Ну ладно! Я наверное пойду по своим делам! Зовите 😉')


@bot.message_handler(commands=['leave'])
def leave(message):
    bot.send_message(message.chat.id, "До свидания!")
    bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['stats'])
def get_stats(message):
    bot.send_message(message.chat.id,
                     "Участников в чате: " +
                     str(bot.get_chat_member_count(message.chat.id)) +
                     "\nИз них админов: " +
                     str(len(bot.get_chat_administrators(message.chat.id))))


@bot.message_handler(commands=['promote'])
def promote_user(message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if user.is_bot:
            bot.set_my_default_administrator_rights(types.ChatAdministratorRights(can_change_info=True,
                                                                                  can_delete_messages=True,
                                                                                  can_invite_users=True,
                                                                                  can_restrict_members=True,
                                                                                  can_pin_messages=True,
                                                                                  can_promote_members=True,
                                                                                  can_manage_chat=False,
                                                                                  can_manage_video_chats=False,
                                                                                  is_anonymous=False))
            bot.send_message(message.chat.id, "Ура, я теперь админ!")
        else:
            if bot.get_chat_member(message.chat.id, user.id).status == 'administrator':
                bot.send_message(message.chat.id, "Вы уже имеете права администратора.")
            else:
                if bot.get_chat_member(message.chat.id, user.id).status == 'creator':
                    # метод не работает((
                    '''bot.promote_chat_member(message.chat.id, message.from_user.id,
                                            can_change_info=True, can_delete_messages=True, can_invite_users=True,
                                            can_restrict_members=True, can_pin_messages=True, can_promote_members=True,
                                            can_manage_chat=False, can_manage_video_chats=False, is_anonymous=False)'''
                    bot.send_message(message.chat.id, "@" + user.username +
                                     " теперь администратор, а не только владелец.")
                else:
                    # метод не работает((
                    '''bot.promote_chat_member(message.chat.id, message.from_user.id,
                                            can_change_info=True, can_delete_messages=True, can_invite_users=True,
                                            can_restrict_members=True, can_pin_messages=True, can_promote_members=True,
                                            can_manage_chat=False, can_manage_video_chats=False, is_anonymous=False)'''
                    bot.send_message(message.chat.id, "@" + user.username +
                                     " теперь администратор.")


bot.polling(none_stop=True, interval=0)
