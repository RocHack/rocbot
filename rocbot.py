from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from datetime import datetime
import actions

class RocBot(irc.IRCClient):
    nickname = "rocbot"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print("[connected at %s]" % datetime.now())

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print("[disconnected at %s]" % datetime.now())

    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        print("[joined channel %s]" % channel)

    def privmsg(self, user, channel, msg):
        user = user.split("!", 1)[0]

        # Getting a private message
        if channel == self.nickname:
            self.msg(user, "Hello there. I can't really do anything cool yet, so hang tight")
            return
        
        if msg.startswith("!" + self.nickname):
            # Parse the message
            msg = msg.replace("!" + self.nickname + " ", "").split(" ")

            if msg[0] in actions.ChannelActions:
                actions.ChannelActions[msg[0]](self, user, channel, msg)
            else:
                self.msg(channel, "I'm not sure what to do with that, " + user)

class RocBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel
    
    def buildProtocol(self, addr):
        protocol = RocBot()
        protocol.factory = self
        return protocol

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

if __name__ == "__main__":
    factory = RocBotFactory("##rochack")
    reactor.connectTCP("irc.freenode.net", 6667, factory)
    reactor.run()
