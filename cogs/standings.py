from nextcord import Interaction, slash_command, Embed
from nextcord.ext.commands import Bot, Cog

from assets.teams.emojis import team_emoji

import requests
import pandas as pd
from nba_api.stats.endpoints import leaguestandings
from nba_api.stats.static import teams

class Standings(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot        
    
    # returns all the relevant league standings data as a pandas dataframe
    def get_league_standings(self):
        headers  = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'x-nba-stats-token': 'true',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'x-nba-stats-origin': 'stats',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://stats.nba.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        standings_url = "https://stats.nba.com/stats/leaguestandings?LeagueID=00&Season=2023-24&SeasonType=Regular+Season&SeasonYear="
        
        response = requests.get(url=standings_url, headers=headers).json()
        standings_table = response["resultSets"][0]
        standings_df = pd.DataFrame(data=standings_table['rowSet'], columns=standings_table["headers"])
        standings_df = standings_df[["TeamName", "Conference", "Record", "LeagueRank"]]
        standings_df = standings_df.rename(columns={'LeagueRank': 'Rank', 'TeamName': 'Team'})

        east_standings_df = standings_df.groupby("Conference").get_group("East")
        west_standings_df = standings_df.groupby("Conference").get_group("West")

        east_standings_df = east_standings_df[["Rank", "Team", "Record"]]
        west_standings_df = west_standings_df[["Rank", "Team", "Record"]]
        
        return east_standings_df, west_standings_df
    
    def generate_standings_rows(self, standings_df):
        ranks = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]
        rows = []
        for i in range(0, len(standings_df)):
            team_abbr = teams.find_teams_by_nickname(standings_df.iloc[i]["Team"])[0]["abbreviation"]
            record = standings_df.iloc[i]["Record"]
            row = "`{rank}   `".format(rank=ranks[i]) + team_emoji[team_abbr] + "`{team}     {record}`".format(team=team_abbr, record=record)
            rows.append(row)
        
        rows = "\n".join(rows)
        return rows

    
    @slash_command(name="standings", description="retrieve the current nba standings", guild_ids=[1037945054062444604])
    async def standings(self, inter: Interaction) -> None:
        
    
        east_standings_df, west_standings_df = self.get_league_standings()
     
        embed_standings = Embed(
            title="2023-24 NBA Regular Season Standings",
            color=0xeb3434
        )
        
        embed_standings.set_thumbnail(url="https://cdn.discordapp.com/attachments/1036788301266419713/1174117333841752104/nba_logo.png?ex=65666cfa&is=6553f7fa&hm=72e00d70b35468429035d7f014cc8aeceab9903344f483d0be1e06934124173b&")
        
        west_rows = self.generate_standings_rows(west_standings_df)
        east_rows = self.generate_standings_rows(east_standings_df)
        
        embed_standings.add_field(name='', value="`#     Team       W-L`", inline=False)
        embed_standings.add_field(name="Eastern Conference Standings", value=east_rows, inline=False)
        embed_standings.add_field(name="Western Conference Standings", value=west_rows, inline=False)
        
        await inter.send(embed=embed_standings)

        
def setup(bot: Bot) -> None:
    bot.add_cog(Standings(bot))