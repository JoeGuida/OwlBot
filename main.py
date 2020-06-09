from discord.ext import commands
from decouple import config
from events import Events

# Create the bot
bot = commands.Bot(command_prefix='-', owner_id=270032037501599747)

# Add the cogs
bot.add_cog(Events(bot))

# Run the bot
bot.run(config('DISCORD_TOKEN'))
