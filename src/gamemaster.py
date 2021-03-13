from database import Database, Action
from typing import Dict, Any
from db_object import Object
from users import User, Profile
from queue import Queue
import utils
from filters import checkConstraints
import os  # temp

COMMANDS = utils.load_json('commands.json')


class GMResponse:
    NOT_COMMAND = 40
    INVALID_CONTEXT_LEN = 41
    INVALID_CONTEXT_DATA = 42
    INVALID_CONTEXT_STRUCT = 43

    INVALID_CONTEXT = [
        INVALID_CONTEXT_LEN,
        INVALID_CONTEXT_DATA,
        INVALID_CONTEXT_STRUCT
    ]


class GameMaster:

    def __init__(self) -> None:
        self.db = Database()
        self.queue = Queue()

    def put_action(self, name: str, obj: Object) -> None:
        """
            Put action in queue
        """
        action = Action(name, obj)
        self.queue.put(action)

    def perform_actions(self) -> None:
        """
            Perform actions on db listed in queue
        """
        while not self.queue.empty():
            self.db.perform(
                self.queue.get()
            )

    @staticmethod
    def get_available_commands(message: str) -> dict:
        """
            Return available commands and context structure for them
        """
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

    def receive_message(self, command: str, context: dict) -> Any:
        # Check if command exists
        if command not in COMMANDS:
            return GMResponse.NOT_COMMAND

        command_context = COMMANDS[command]['input']

        # Check if context length equals to command's required context length
        if len(command_context) != len(context):
            return GMResponse.INVALID_CONTEXT_LEN

        # Check if context fits to command's required context
        if len(set(command_context) - set(context)) != 0:
            return GMResponse.INVALID_CONTEXT_STRUCT

        # Check if context is valid
        if checkConstraints(context, COMMANDS[command]['input']) == 0:
            return GMResponse.INVALID_CONTEXT_DATA

        # Execute command
        getattr(self, command)(context)

        # Perfom actions on db
        self.perform_actions()

        # Return next available commands
        return self.get_available_commands(command)

    def entry_point(self, context: dict) -> None:
        """
            Initial command for all new users to start work with GM
        """
        user = User(context.get('id'), False)
        self.put_action('insert', user)

    def manage_profile(self, context: dict) -> None:
        """
            Create or update user's profile
        """
        profile = Profile(**context)
        self.put_action('upsert', profile)

    def switch_status(self, context: dict) -> None:
        """
            Switch user's status (active, inactive)
        """
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
    if aval == GMResponse.NOT_COMMAND:
        print('Not a command. Try again.')
    else:
        print(GameMaster.parse_commands(aval))

    command = input()
    if command == 'b':
        break
    context = GameMaster.get_context_template(command)
    for field, desc in context.items():
        print(desc)
        print(f'{field} = ', end='')
        context[field] = input()
        try:
            context[field] = int(context[field])
        except:
            pass
        print('')

os.remove('C:\Coding\Documents\Projects\RolePlay\data\memory.sqlite')