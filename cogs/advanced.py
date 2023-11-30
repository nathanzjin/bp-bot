from nextcord import Interaction, slash_command, SlashOption, Embed
from nextcord.ext.commands import Bot, Cog

from assets.teams.emojis import team_emoji

import requests
import pandas as pd
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams


class Advanced(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    # generates the embed rows for the team advanced stats leaders
    def generate_rows(self, df, stat):
        ranks = ["01", "02", "03", "04", "05"]
        rows = []
        for i in range(0, len(df)):
            team_abbr = teams.find_teams_by_full_name(df.iloc[i]["TEAM_NAME"])[0]["abbreviation"]
            rating = df.iloc[i][stat]
            row = "`{rank}   `".format(rank=ranks[i]) + team_emoji[team_abbr] + "`{team}      {rating}`".format(team=team_abbr, rating=rating)
            rows.append(row)
        
        rows = "\n".join(rows)
        return rows
        
    
    # creates the offensive rating embed
    def get_offensive_rating(self, headers, url):
        response = requests.get(url=url, headers=headers).json()
        team_stats_table = response["resultSets"][0]
        team_stats_df = pd.DataFrame(data=team_stats_table['rowSet'], columns=team_stats_table["headers"])
        advanced_df = team_stats_df[["TEAM_NAME", "OFF_RATING", "OFF_RATING_RANK"]]
        
        orating_df = advanced_df[["OFF_RATING_RANK", "TEAM_NAME", "OFF_RATING"]].sort_values("OFF_RATING_RANK").head(5)
        
        embed_off_rating = Embed(
            title="Offensive Rating Team Leaders",
            color=0xa83232
        )

        off_rating_rows = self.generate_rows(orating_df, "OFF_RATING")
        embed_off_rating.add_field(name='', value="`#     Team       OFFRTG`", inline=False)
        embed_off_rating.add_field(name='', value=off_rating_rows, inline=False)
        embed_off_rating.set_thumbnail(url="https://cdn.discordapp.com/attachments/1036788301266419713/1174117333841752104/nba_logo.png?ex=65666cfa&is=6553f7fa&hm=72e00d70b35468429035d7f014cc8aeceab9903344f483d0be1e06934124173b&")
        
        
        return embed_off_rating
    
    # creates the defensive rating embed
    def get_defensive_rating(self, headers, url):
        response = requests.get(url=url, headers=headers).json()
        team_stats_table = response["resultSets"][0]
        team_stats_df = pd.DataFrame(data=team_stats_table['rowSet'], columns=team_stats_table["headers"])
        advanced_df = team_stats_df[["TEAM_NAME", "DEF_RATING", "DEF_RATING_RANK"]]
        
        drating_df = advanced_df[["DEF_RATING_RANK", "TEAM_NAME", "DEF_RATING"]].sort_values("DEF_RATING_RANK").head(5)
        
        embed_def_rating = Embed(
            title="Defensive Rating Team Leaders",
            color=0x1e12c4
        )

        def_rating_rows = self.generate_rows(drating_df, "DEF_RATING")
        embed_def_rating.add_field(name='', value="`#     Team       DEFRTG`", inline=False)
        embed_def_rating.add_field(name='', value=def_rating_rows, inline=False)
        embed_def_rating.set_thumbnail(url="https://cdn.discordapp.com/attachments/1036788301266419713/1174117333841752104/nba_logo.png?ex=65666cfa&is=6553f7fa&hm=72e00d70b35468429035d7f014cc8aeceab9903344f483d0be1e06934124173b&")
        
        return embed_def_rating
    
    @slash_command(name="advanced", description="Returns team advanced stats for the current NBA season", guild_ids=[1037945054062444604])
    async def advanced(
        self,
        inter: Interaction,
        stat: str = SlashOption(
            name="stat",
            choices=["Offensive Rating", "Defensive Rating"]
        ),
    ):
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

        team_stats_url = ("https://stats.nba.com/stats/leaguedashteamstats?"
                            "Conference=&"
                            "DateFrom=&"
                            "DateTo=&"
                            "Division=&"
                            "GameScope=&"
                            "GameSegment=&"
                            "LastNGames=0&"
                            "LeagueID=&"
                            "Location=&"
                            "MeasureType=Advanced&"
                            "Month=0&"
                            "OpponentTeamID=0&"
                            "Outcome=&PORound=&"
                            "PaceAdjust=N&"
                            "PerMode=Per100Possessions&"
                            "Period=0&"
                            "PlayerExperience=&"
                            "PlayerPosition=&"
                            "PlusMinus=N&"
                            "Rank=N&Season=2023-24&"
                            "SeasonSegment=&"
                            "SeasonType=Regular+Season&"
                            "ShotClockRange=&"
                            "StarterBench=&"
                            "TeamID=&"
                            "TwoWay=&"
                            "VsConference=&"
                            "VsDivision=")
        
        
        
        
        if (stat == "Offensive Rating"):
            await inter.send(embed=self.get_offensive_rating(headers=headers, url=team_stats_url))
        elif (stat == "Defensive Rating"):
            await inter.send(embed=self.get_defensive_rating(headers=headers, url=team_stats_url))
            
        
        
def setup(bot: Bot) -> None:
    bot.add_cog(Advanced(bot))