import gamemaster
import utils_tg as utg
from telegram.update import Update
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from dictionary import DICT
from filters_tg import CustomFilters


class TG:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self.gm = gamemaster.GameMaster()
        self.add_all_handlers(dispatcher)

    def add_all_handlers(self, dispatcher: Dispatcher) -> None:
        # Start
        dispatcher.add_handler(CommandHandler('start', self.auth_user))

        # User profile creation
        dispatcher.add_handler(
            ConversationHandler(
                entry_points=[CommandHandler(
                    'profile', self.fill_user_profile)],
                states={
                    'profile_name': [MessageHandler(Filters.text, utg.user_profile_name)],
                    'profile_age': [MessageHandler(CustomFilters.positive_int, utg.user_profile_age)],
                    'profile_status': [MessageHandler(CustomFilters.text_len_ubound(70), utg.user_profile_status)],
                    'profile_bio': [MessageHandler(CustomFilters.text_len_ubound(512), self.register_user)]
                },
                # TODO: Make fallbacks smarter
                fallbacks=[MessageHandler(Filters.text |
                                          Filters.video |
                                          Filters.photo |
                                          Filters.video,
                                          utg.dontknow)])
        )

    def auth_user(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(DICT['hello'])
        uid = update.effective_user.id
        existed = self.gm.auth_user(uid)
        has_name = self.gm.get_user_profile(uid)
        if not existed or not has_name:
            update.message.reply_text(
                DICT['require_profile'],
                reply_markup=utg.get_keyboard('user_profile_start'),
                parse_mode='Markdown')
        else:
            # TODO: Добавить возвращение (снова актив) пользователей
            pass

    def fill_user_profile(self, update: Update, context: CallbackContext) -> None:
        uid = update.effective_user.id
        existed = self.gm.auth_user(uid)
        has_name = self.gm.get_user_profile(uid)
        if not existed or not has_name:
            return utg.user_profile_start(update, context)

    def register_user(self, update: Update, context: CallbackContext) -> None:
        profile = utg.user_profile_edit(update, context)
        if profile:
            pass
            # self.gm.set_user_profile(profile)
        return ConversationHandler.END
