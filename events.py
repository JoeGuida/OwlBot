from discord.ext import commands
import json
from datetime import datetime

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.role_message = None

    # Load JSON data when bot is ready
    # Add reactions to role message
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()

        # Read the JSON data to self.data
        with open('./roles.json', 'r') as file:
            self.data = json.loads(file.read())

        # Get guild, role channel and role message
        self.guild = self.bot.get_guild(self.data['guild_id'])
        channel = self.bot.get_channel(self.data['role_channel_id'])
        self.role_message = await channel.fetch_message(self.data['role_message_id'])

        # Get each emoji and add the reactions
        for key, value in list(self.data.items())[3:]:
            emoji = self.bot.get_emoji(value['emoji_id'])
            await self.role_message.add_reaction(emoji)

        # Print to console
        print(f'-------------\nBot Online At {datetime.now()}')

    # Force quit the bot
    @commands.command(name='q')
    async def _quit(self, ctx):
        await self.bot.logout()

    # Adds or removes role based on reaction in a specific channel
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Only look at reactions to the role message
        if payload.message_id != self.data['role_message_id']:
            return

        # If one of the correct emojis is used
        # add the role if the member doesn't have it
        # remove the role if the member has it
        if payload.emoji.name in self.data:
            role = self.guild.get_role(self.data[payload.emoji.name]['role_id'])

            if role not in payload.member.roles:
                await payload.member.edit(roles=payload.member.roles + [role])   
            else:
                roles = payload.member.roles
                roles.remove(role)
                await payload.member.edit(roles=roles)

        # Remove the reaction when done
        await self.role_message.remove_reaction(payload.emoji, payload.member)
