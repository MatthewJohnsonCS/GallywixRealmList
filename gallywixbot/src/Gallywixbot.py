import os
import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
admin_role = os.getenv('ADMIN_ROLE')


client = discord.Client()

list_of_realms = ['Area-52', 'BleedingHollow', 'Dalaran', 'Illidan', 'Mal\'Ganis', 'Thrall', 'Zul\'Jin']
users_currently_on_realm = {
    'Area-52': set([]),
    'BleedingHollow': set([]),
    'Dalaran': set([]),
    'Illidan': set([]),
    'Mal\'Ganis': set([]),
    'Thrall': set([]),
    'Zul\'Jin': set([])
}


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.channels, name=CHANNEL)
    for realm in list_of_realms:
        message = await channel.send(realm+'\nUsers on Realm: ')
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        await message.add_reaction('🚫')


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    for realm in list_of_realms:
        if realm in reaction.message.content:
            await handle_reaction_to_realm(reaction, reaction.message, realm, user)
            break


async def handle_reaction_to_realm(reaction, message, realm, user):
    the_message = realm + '\nUsers on Realm: '
    await reaction.remove(user)

    if reaction.emoji == '✅':
        users_currently_on_realm[realm].add(user.name)
    if reaction.emoji == '❌':
        users_currently_on_realm[realm].discard(user.name)

    if reaction.emoji == '🚫':
        for role in user.roles:
            if str(role) == admin_role:
                users_currently_on_realm[realm] = set([])
    for user_name in users_currently_on_realm[realm]:
        the_message += user_name + ', '
    await message.edit(content=the_message)

client.run(TOKEN)
