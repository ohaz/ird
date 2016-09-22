from database import session
from models.room import Room
from models.user import User, new_user, hash_key
from pprint import pprint
import utils

__author__ = 'ohaz'


class Game:
    def __init__(self):
        self.users_in_registration = {}
        self.authed = {}
        self.start_room = None
        self.running = False

    def register(self, user_name, source_nick):
        if len(user_name) > 30:
            return 'Character name too long. Retry with a shorter name - .register <character name>'
        if source_nick in self.users_in_registration.keys():
            return 'You are already in registration process. Please continue with next step!'
        for character in self.users_in_registration.values():
            if character.user_name == user_name:
                return 'This character name is currently in registration process. Please try again with a different name'
        user = session.query(User).filter(User.user_name == user_name).first()
        if user:
            return 'This username is already registered. Retry with a different one or log in with .join <character name> <pass phrase>'

        # stats = utils.generate_stats()
        pw = utils.generate_password()
        user = new_user(user_name, pw)
        self.users_in_registration[user_name] = user
        return 'Your auth-key is {} - Please save it for future logins!\nYou currently have the following stats: {} - do you want to .reroll-stats <character_name> or .accept-stats <character_name>?'.format(
            pw, user.print_stats())

    def accept_character(self, user_name, source_nick):
        if user_name in self.users_in_registration.keys():
            c = self.users_in_registration[user_name]
            session.add(c.character)
            session.add(c)
            session.commit()
            self.authed[source_nick] = self.users_in_registration[user_name]
            return 'Your character has been saved.'
        return 'Sorry, but you don\'t have any characters in creation process. Use .register!'

    def reroll_stats(self, user_name):
        if user_name in self.users_in_registration.keys():
            self.users_in_registration[user_name].character.roll_stats()
            return 'You currently have the following stats: {} - do you want to .reroll-stats or .accept-stats?'.format(
                self.users_in_registration[user_name].print_stats())
        else:
            return 'Sorry, but you don\'t have any characters in creation process. Use .register!'

    def player_online(self):
        for player in self.authed:
            if player is not None:
                return True
        return False

    def generate_room(self, prepared=None, level=0, neighbours=None, parent=None):
        if neighbours is None:
            neighbours = []
        if prepared is None:
            prepared = self.prepare_room(level, neighbours, parent)
        self.generate_content(prepared, level)
        prepared.generated = True
        session.commit()
        return prepared

    def generate_content(self, room, level):
        self.generate_items(room, level)
        self.generate_enemies(room, level)
        self.generate_events(room, level)
        self.generate_others(room, level)

    def generate_items(self, room, level):
        pass

    def generate_enemies(self, room, level):
        pass

    def generate_events(self, room, level):
        pass

    def generate_others(self, room, level):
        pass

    def prepare_room(self, level=0, neighbours=None, parent=None):
        if neighbours is None:
            neighbours = []
        r = Room(generated=False)
        if parent is not None:
            parent.exits.append(r)
        for neighbour in neighbours:
            r.exits.append(r)
        session.add(r)
        session.commit()
        return r

    def start(self):
        self.running = True
        if session.query(Room).first() is None:
            self.start_room = self.generate_room()
            r2 = self.prepare_room(parent=self.start_room)
            r3 = self.prepare_room(parent=self.start_room, neighbours=[r2])

    def shutdown(self):
        if not self.player_online():
            self.running = False

    def join(self, user_name, auth_key, source_nick):
        user = session.query(User).filter(User.user_name == user_name,
                                          User.auth_key == hash_key(auth_key)).first()
        if user is None:
            return 'Wrong Character-name / Auth-Key combination. Please try again!'
        self.authed[source_nick] = user
        if self.player_online() and not self.running:
            self.start()
        return ('Authenticated as {}, have fun!'.format(user.user_name),
                'User {} joined with Character {}!'.format(source_nick, user.user_name))


