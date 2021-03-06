# cmd_unmute.py

import discord
from lang.lang import Lang
from cmds.cmd import ServerCmd
from user import User


async def cmd_unmute(server, userid, channel, message):
    split_content = str(message.content).split()
    if len(message.mentions) < 1:
        await channel.send(Lang.get('CMD_WRONG_SYNTAX', server.lang))
        await channel.send(f"`{server.cmd_prefix}unmute <users>`")
        return False
    for mention in message.mentions:
        if mention.id not in server.members.keys():
            raise Exception(f'Cannot find user ({ mention.id }) in server')
            pass
        server.members[mention.id].lock.acquire()
        server.members[mention.id].muted = False
        server.members[mention.id].muted_until = None
        if mention.voice is not None:
            await mention.edit(mute=False)
        await channel.send(
            f"{User.get_at_mention(mention.id)} has been unmuted by {User.get_at_mention(userid)}")
        server.members[mention.id].lock.release()
    return True

UnmuteCmd = ServerCmd('unmute', cmd_unmute)
UnmuteCmd.required_perks = ['cmd.unmute']
