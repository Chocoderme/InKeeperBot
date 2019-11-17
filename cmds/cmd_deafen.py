# cmd_deafen.py

import discord
from lang.lang import Lang
from datetime import datetime, timedelta
from cmds.cmd import ServerCmd
from user import User


async def cmd_deafen(server, userid, channel, message):
    split_content = str(message.content).split()
    if len(message.mentions) < 1:
        await channel.send(Lang.get('CMD_WRONG_SYNTAX', server.lang))
        await channel.send(f"`{server.cmd_prefix}deaf <users> (<time>)`")
        return False
    time = -1
    if len(split_content) > len(message.mentions) + 1:
        time = int(split_content[-1])
    for mention in message.mentions:
        if mention.id not in server.members.keys():
            raise Exception(f'Cannot find user ({ mention.id }) in server')
            pass
        server.members[mention.id].lock.acquire()
        server.members[mention.id].deaf = True
        if mention.voice is not None:
            await mention.edit(deafen=True)
        if time > 0:
            server.members[mention.id].deaf_until = datetime.now() + timedelta(seconds=time)
            await channel.send(
                f"{User.get_at_mention(mention.id)} has been deafen by {User.get_at_mention(userid)} for {time} seconds")
        else:
            server.members[mention.id].deaf_until = None
            await channel.send(
                f"{User.get_at_mention(mention.id)} has been deafen by {User.get_at_mention(userid)}")
        server.members[mention.id].lock.release()
    return True

DeafenCmd = ServerCmd('deafen', cmd_deafen)
DeafenCmd.required_perks = ['cmd.deafen']
