def hello(bot, user, channel, msg):
    bot.msg(channel, "Hey there, " + user)

def about(bot, user, channel, msg):
    bot.msg(channel, "I'm a bot originally created by Steve Gattuso <steve@stevegattuso.me>. /msg rocbot help for help.")

# Just a mapping of actions to functions
ChannelActions = {
    "hello": hello,
    "about": about
}
