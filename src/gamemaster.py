from os import access
from pprint import pprint
from database import Database, Action
from typing import Dict, Any
from gm_object import Object
from users import User, Profile
from queue import Queue
import utils


COMMANDS = utils.load_json('commands.json')


class GameMaster:
    def __init__(self) -> None:
        self.db = Database()
        self.queue = Queue()

    def put_action(self, name: str, obj: Object) -> None:
        action = Action(name, obj)
        self.queue.put(action)

    def perform_actions(self) -> None:
        """Perform actions in queue"""
        while not self.queue.empty():
            self.db.perform(
                self.queue.get()
            )

    def get_available_commands(self, message: str) -> Dict:
        """Return available commands and context structure for them"""
        available_commands = COMMANDS[message]['output']
        return {
            command: COMMANDS[command]['input']
            for command in available_commands
        }

    @staticmethod
    def parse_commands(commands: dict) -> str:
        result = ''
        for command, fields in commands.items():
            result += f'Команда: {command}\nКонтекст:\n'
            for field in fields:
                conds = fields[field].split(' ')
                result += f'  {field}:\n\t{conds[0]}: {conds[1:]}\n'
        return result

    @staticmethod
    def get_context_template(command) -> dict:
        return COMMANDS[command]['input'].copy()

    def receive_message(self, command: str, context: Dict) -> Any:
        getattr(self, command)(context)
        self.perform_actions()
        return self.get_available_commands(command)

    def entry_point(self, context: Dict) -> None:
        """Initial command for all new users to start work with GM"""
        user = User(context.get('id'), False)
        self.put_action('insert', user)

    def manage_profile(self, context: Dict) -> None:
        """Create or update user's profile"""
        profile = Profile(**context)
        self.put_action('upsert', profile)

    def switch_status(self, context: Dict) -> None:
        """Switch user's status (active, inactive)"""
        user = User(context['id'])
        user = self.db.find_one(user)
        user.active = not user.active
        self.put_action('upsert', user)


id = 0
gm = GameMaster()
command = 'entry_point'
context = {'id': id}

while True:
    aval = gm.receive_message(command, context)
    print(GameMaster.parse_commands(aval))

    command = input()
    context = GameMaster.get_context_template(command)
    for field, desc in context.items():
        print(desc)
        print(f'{field} = ', end='')
        context[field] = input()
        print('')

    inp = input()
    if inp == 'b':
        break
