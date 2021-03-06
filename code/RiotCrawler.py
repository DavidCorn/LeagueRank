import ujson
import urllib2

from config import config
from riotwatcher import RiotWatcher


class RiotCrawler:
    def __init__(self, key):
        self.key = key
        self.w = RiotWatcher(key)
        self.tiers = {
            'bronze': [],
            'silver': [],
            'gold': [],
            'platinum': [],
            'diamond': [],
            'challenger': [],
            'master': [],
        }

    # def get_player_list(self):
    #     recent_games = self.w.get_recent_games(self.player_id)
    #     player_list = set()
    #     for game in recent_games['games']:
    #         # only pick up ranked games
    #         if 'RANKED' in game['subType']:
    #             fellow_players = game['fellowPlayers']
    #             for fellow_player in fellow_players:
    #                 fellow_player_id = fellow_player['summonerId']
    #                 if fellow_player_id not in player_list:
    #                     player_list.add(fellow_player_id)
    #     return list(player_list)

    def get_player_by_tier(self, summoner_id):
        request_url = 'https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/{}?api_key={}'.format(
            summoner_id, self.key
        )
        response = urllib2.urlopen(request_url)
        tier_info = ujson.loads(response.read())

        tier = tier_info[str(summoner_id)][0]['tier'].lower()
        entries = tier_info[str(summoner_id)][0]['entries']

        level = self.tiers[tier]
        for entry in entries:
            level.append(entry['playerOrTeamId'])

        for l in level:
            print 'summoner id: {}'.format(str(l))


def get_tier():
    # challenger: 77759242
    # platinum: 53381
    # gold: 70359816
    # silver: 65213225
    # bronze: 22309680
    # master: 22551130
    # diamond: 34570626
    player_ids = [70359816, 77759242, 53381, 65213225, 22309680, 22551130, 34570626]
    riot_crawler = RiotCrawler(config['key'])
    for player_id in player_ids:
        print 'start crawling id: {}'.format(player_id)
        riot_crawler.get_player_by_tier(player_id)
    return riot_crawler.tiers

tiers = get_tier()
for tier, rank_dict in tiers.iteritems():
    print '--- {} ---'.format(tier)
    for summoner in rank_dict:
        print 'summoner id: {}'.format(summoner)
    print '--- end of {} ---'.format(tier)

