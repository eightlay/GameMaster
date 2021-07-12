from telegram import ReplyKeyboardMarkup, ParseMode, ReplyKeyboardRemove
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from dictionary import DICT, EMPTY


def dontknow(update: Update, context: CallbackContext):
    update.message.reply_text(DICT['dontknow'])


# region Keyboards


def get_keyboard(typ: str) -> ReplyKeyboardMarkup:
    keyboard = None
    if typ == 'user_profile_start':
        keyboard = ReplyKeyboardMarkup([['/profile']],
                                       resize_keyboard=True,
                                       one_time_keyboard=True)
    return keyboard


# endregion

# region User profile creation


def proccess_user_profile(user_data: dict) -> dict:
    profile = {}

    if user_data['name'] == EMPTY:
        profile['name'] = 'Игрок#' + str(user_data['uid'])
    else:
        profile['name'] = user_data['name'].strip()

    profile['uid'] = int(user_data['uid'])

    profile['age'] = int(user_data['age'])

    if user_data['status'] == EMPTY:
        profile['status'] = '-'
    else:
        profile['status'] = user_data['status'].strip()

    if user_data['bio'] == EMPTY:
        profile['bio'] = '-'
    else:
        profile['bio'] = user_data['bio'].strip()

    return profile


def user_profile_start(update: Update, context: CallbackContext) -> str:
    context.user_data['uid'] = update.effective_user.id
    update.message.reply_text(
        '{0}\n\n{1}: {2}.'.format(
            DICT['ask_name'],
            DICT['answer_optional'],
            f'Игрок#{update.effective_user.id}'
        ), reply_markup=ReplyKeyboardRemove())
    return 'profile_name'


def user_profile_name(update: Update, context: CallbackContext) -> str:
    context.user_data['name'] = update.message.text
    update.message.reply_text(
        '{0}\n\n{1}'.format(
            DICT['ask_age'],
            DICT['answer_required']
        ))
    return 'profile_age'


def user_profile_age(update: Update, context: CallbackContext) -> str:
    context.user_data['age'] = update.message.text
    update.message.reply_text(
        '{0}\n\n{1}: {2}.'.format(
            DICT['ask_status'],
            DICT['answer_optional'],
            '-'
        ),
        parse_mode='Markdown')
    return 'profile_status'


def user_profile_status(update: Update, context: CallbackContext) -> str:
    context.user_data['status'] = update.message.text
    update.message.reply_text(
        '{0}\n\n{1}: {2}.'.format(
            DICT['ask_bio'],
            DICT['answer_optional'],
            '-'
        ),
        parse_mode='Markdown')
    return 'profile_bio'


def user_profile_edit(update: Update, context: CallbackContext) -> str:
    context.user_data['bio'] = update.message.text
    profile = proccess_user_profile(context.user_data)
    text = """<u><b>Результат опроса</b></u>:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Статус:</b> {status}
    <b>Биография:</b> {bio}
    """.format(**profile)
    update.message.reply_text(text, parse_mode=ParseMode.HTML)
    # TODO: Make possible to edit profile
    return profile

# endregion
