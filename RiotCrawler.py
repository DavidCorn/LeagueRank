import ujson
import urllib2

from config import config
from riotwatcher import RiotWatcher


class RiotCrawler:
    def __init__(self, key):
        self.key = key
        self.w = RiotWatcher(key)
        self.division = {
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

    def get_player_by_division(self, summoner_id):
        request_url = 'https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/{}?api_key={}'.format(
            summoner_id, self.key
        )
        response = urllib2.urlopen(request_url)
        division_info = ujson.loads(response.read())

        tier = division_info[str(summoner_id)][0]['tier'].lower()
        entries = division_info[str(summoner_id)][0]['entries']

        level = self.division[tier]
        cnt = 0
        for entry in entries:
            level.append(entry['playerOrTeamId'])
            cnt += 1
            if cnt == 3:
                break

        # for l in level:
        #     print 'summoner id: {}, name: {}'.format(str(l.id), l.name)


def get_division():
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
        riot_crawler.get_player_by_division(player_id)
    return riot_crawler.division


# for tier, rank_dict in riot_crawler.division.iteritems():
#     print '--- {} ---'.format(tier)
#     for summoner in rank_dict:
#         print 'summoner id: {}'.format(summoner)
#     print '--- end of {} ---'.format(tier)

