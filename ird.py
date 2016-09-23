#!/usr/bin/python3
from jaraco.stream import buffer
import irc.bot
import irc.strings
import irc.client
from database import session
from models.user import User, new_user, hash_key
from models.room import Room
from models.character import Character
import utils
import traceback
from game import Game

__author__ = 'ohaz'


class IgnoreErrorsBuffer(buffer.DecodingLineBuffer):
    def handle_exception(self):
        pass


irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer


class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channels, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.active_channels = channels
        self.cmds = {'register': self.register, 'join': self.join, 'move': self.move, 'talk': self.talk,
                     'attack': self.attack, 'accept-stats': self.accept_character, 'reroll-stats': self.reroll_stats}
        self.users_in_registration = {}
        self.game = Game()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        for channel in self.active_channels:
            c.join(channel)

    def on_privmsg(self, c, e):
        self.incoming_msg(c, e)

    def incoming_msg(self, c, e):
        try:
            if e.arguments[0].startswith('.'):
                cmd = ((e.arguments[0].split(' '))[0]).replace('.', '')
                self.do_command(e, cmd)
        except Exception as e:
            print(e)
            traceback.print_exc()
        return

    def on_join(self, c, e):
        nick = e.source.split('!')[0]
        self.game.authed[nick] = None
        if nick == c.get_nickname():
            return
        if e.target in self.active_channels:
            c.privmsg(nick, 'Welcome to the Internet Relay Dungeon')
            c.privmsg(nick,
                      'To join the game, either .register <character name> or .join <character name> <pass phrase>!'
                      )
            c.privmsg(nick, 'Attention: Please don\'t change your IRC nick during the registration process!')

    def on_part(self, c, e):
        nick = e.source.split('!')[0]
        if nick in self.game.authed:
            del self.game.authed[nick]
        self.game.shutdown()

    def on_nick(self, c, e):
        old_nick = e.source.split('!')[0]
        nick = e.target
        status = None
        if old_nick in self.game.authed:
            status = self.game.authed[old_nick]
            del self.game.authed[old_nick]
        self.game.authed[nick] = status

    def on_pubmsg(self, c, e):
        self.incoming_msg(c, e)

    def do_command(self, e, cmd):
        if cmd in self.cmds:
            self.cmds[cmd](e)

    def register(self, e):
        c = self.connection
        msg = e.arguments[0]
        split = msg.split(' ')
        if len(split) != 2:
            c.privmsg(e.source.nick, 'Wrong amount of arguments. Retry with .register <character name>')
            return
        character_name = split[1]
        for line in self.game.register(character_name, e.source.nick).splitlines():
            c.privmsg(e.source.nick, line)

    def accept_character(self, e):
        c = self.connection
        split = e.arguments[0].split(' ')
        if len(split) != 2:
            c.privmsg(e.source.nick, 'Wrong amount of arguments. Retry with .accept-stats <character name>')
            return
        for line in self.game.accept_character(split[1], e.source.nick).splitlines():
            c.privmsg(e.source.nick, line)

    def reroll_stats(self, e):
        c = self.connection
        split = e.arguments[0].split(' ')
        if len(split) != 2:
            c.privmsg(e.source.nick, 'Wrong amount of arguments. Retry with .reroll-stats <character name>')
            return
        for line in self.game.reroll_stats(split[1]).splitlines():
            c.privmsg(e.source.nick, line)

    def join(self, e):
        c = self.connection
        split = e.arguments[0].split(' ')
        if len(split) != 3:
            c.privmsg(e.source.nick, 'Wrong amount of arguments. Retry with .join <character name> <auth key>')
            return
        character_name = split[1]
        auth_key = split[2]
        result = self.game.join(character_name, auth_key, e.source.nick)
        c.privmsg(e.source.nick, result[0])
        for name in self.channels:
            channel = self.channels[name]
            if name in self.active_channels:
                if e.source.nick in list(channel.users()):
                    c.privmsg(name, result[1])
        c.privmsg(e.source.nick, self.game.authed[e.source.nick].character.move(self.game.start_room))

    def move(self, e):
        c = self.connection
        split = e.arguments[0].split(' ')
        if len(split) != 2:
            c.privmsg(e.source.nick, 'Wrong amount of arguments. Try .move <Room-ID>.')
            return
        r = session.query(Room).get(int(split[1]))
        if r is not None:
            c.privmsg(e.source.nick, self.game.authed[e.source.nick].character.move(r))
        else:
            c.privmsg(e.source.nick, 'Invalid room.')
        #split = e.arguments[0].split(' ')

    def talk(self, e):
        pass

    def attack(self, e):
        pass


def main():
    b = Bot(["#ird"], "IRD", "blitzforum.de")
    b.start()


if __name__ == "__main__":
    main()
