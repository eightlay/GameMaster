from database import Database, Action
from typing import Dict, Any
from users import User, Profile
from queue import Queue


class GameMaster:
    ACTIONS = {'create_profile'}

    def __init__(self) -> None:
        self.db = Database()
        self.queue = Queue()

    def perfom_actions(self):
        while not self.queue.empty():
            self.db.perform(
                self.queue.get()
            )

    def receive_message(self, message: str, context: Dict[str, object]) -> Any:
        available = getattr(self, message)(context)
        self.perfom_actions()
        return available

    def start(self, context: Dict[str, object]):
        user = User(context.get('uid'))
        if not self.db.find_one(user):
            user.active = True
            self.add_new_user(user)
        return {'create_profile'}

    def add_new_user(self, user: User) -> bool:
        """Authentificate user"""
        action = Action('add', user)
        self.queue.put(action)


gm = GameMaster()
print(gm.receive_message('start', {'uid': 2}))
