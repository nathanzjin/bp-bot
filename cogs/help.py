from nextcord import Interaction, slash_command
from nextcord.ext.commands import Bot, Cog



class Commands(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @slash_command(name="commands", description="Returns a list of commands that the bot supports", guild_ids=[1037945054062444604])
    async def commands(self, inter: Interaction) -> None:
        await inter.send("Hello!")
        
def setup(bot: Bot) -> None:
    bot.add_cog(Commands(bot))