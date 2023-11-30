from nextcord import Interaction, slash_command
from nextcord.ext.commands import Bot, Cog



class PlayerProfile(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @slash_command(name="compare-players", description="A simple hello command", guild_ids=[1037945054062444604])
    async def player_profile(self, inter: Interaction) -> None:
        await inter.send("Hello!")
        
def setup(bot: Bot) -> None:
    bot.add_cog(PlayerProfile(bot))