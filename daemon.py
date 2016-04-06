from daemonize import Daemonize
from bot import MALnetBot

bot = MALnetBot()

daemon = Daemonize(app="MALnet_bot", pid="bot_daemon.pid", action=bot.run)
daemon.start()
