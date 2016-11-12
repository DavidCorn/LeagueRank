import csv
import json
import os
import urllib2

from RiotCrawler import get_tier
from config import config


class TopChampion:

    FIELD_NAMES = ['totalSessionsPlayed', 'totalSessionsLost', 'totalSessionsWon',
                   'totalChampionKills', 'totalDamageDealt', 'totalDamageTaken',
                   'mostChampionKillsPerSession', 'totalMinionKills', 'totalDoubleKills',
                   'totalTripleKills', 'totalQuadraKills', 'totalPentaKills',
                   'totalUnrealKills', 'totalDeathsPerSession', 'totalGoldEarned',
                   'mostSpellsCast', 'totalTurretsKilled', 'totalPhysicalDamageDealt',
                   'totalMagicDamageDealt', 'totalFirstBlood', 'totalAssists',
                   'maxChampionsKilled', 'maxNumDeaths', 'label']

    def __init__(self, key, player_id, label, n):
        self.label = label
        self.player_id = player_id
        self.key = key
        self.n = n
        self.top_champions = []
        pass

    def get_top_champions(self):
        self.top_champions[:] = []
        data = urllib2.urlopen(
            'https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' +
            self.player_id +
            '/ranked?season=SEASON2016&api_key=' +
            self.key
        ).read()
        json_data = json.loads(data)
        champions = json_data['champions']
        champion_stats = []
        for champion in champions:
            champion_stat = champion['stats']
            champion_stat['id'] = champion['id']
            champion_stat['label'] = self.label
            champion_stats.append(champion_stat)
            pass
        self.top_champions = sorted(champion_stats,
                                    key=lambda x: x['totalSessionsPlayed'],
                                    reverse=True)[1:self.n + 1]
        return self.top_champions
        pass

    def save_top_champions(self):
        for champion in self.top_champions:
            file_name = '../data/{}.csv'.format(champion['id'])
            if os.path.isfile(file_name):
                with open(file_name, 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.FIELD_NAMES)
                    writer.writerow(
                        {
                            'totalSessionsPlayed': champion['totalSessionsPlayed'],
                            'totalSessionsLost': champion['totalSessionsLost'],
                            'totalSessionsWon': champion['totalSessionsWon'],
                            'totalChampionKills': champion['totalChampionKills'],
                            'totalDamageDealt': champion['totalDamageDealt'],
                            'totalDamageTaken': champion['totalDamageTaken'],
                            'mostChampionKillsPerSession': champion['mostChampionKillsPerSession'],
                            'totalMinionKills': champion['totalMinionKills'],
                            'totalDoubleKills': champion['totalDoubleKills'],
                            'totalTripleKills': champion['totalTripleKills'],
                            'totalQuadraKills': champion['totalQuadraKills'],
                            'totalPentaKills': champion['totalPentaKills'],
                            'totalUnrealKills': champion['totalUnrealKills'],
                            'totalDeathsPerSession': champion['totalDeathsPerSession'],
                            'totalGoldEarned': champion['totalGoldEarned'],
                            'mostSpellsCast': champion['mostSpellsCast'],
                            'totalTurretsKilled': champion['totalTurretsKilled'],
                            'totalPhysicalDamageDealt': champion['totalPhysicalDamageDealt'],
                            'totalMagicDamageDealt': champion['totalMagicDamageDealt'],
                            'totalFirstBlood': champion['totalFirstBlood'],
                            'totalAssists': champion['totalAssists'],
                            'maxChampionsKilled': champion['maxChampionsKilled'],
                            'maxNumDeaths': champion['maxNumDeaths'],
                            'label': champion['label']
                        }
                    )
                    pass
                pass
            else:
                with open(file_name, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.FIELD_NAMES)
                    writer.writeheader()
                    writer.writerow(
                        {
                            'totalSessionsPlayed': champion['totalSessionsPlayed'],
                            'totalSessionsLost': champion['totalSessionsLost'],
                            'totalSessionsWon': champion['totalSessionsWon'],
                            'totalChampionKills': champion['totalChampionKills'],
                            'totalDamageDealt': champion['totalDamageDealt'],
                            'totalDamageTaken': champion['totalDamageTaken'],
                            'mostChampionKillsPerSession': champion['mostChampionKillsPerSession'],
                            'totalMinionKills': champion['totalMinionKills'],
                            'totalDoubleKills': champion['totalDoubleKills'],
                            'totalTripleKills': champion['totalTripleKills'],
                            'totalQuadraKills': champion['totalQuadraKills'],
                            'totalPentaKills': champion['totalPentaKills'],
                            'totalUnrealKills': champion['totalUnrealKills'],
                            'totalDeathsPerSession': champion['totalDeathsPerSession'],
                            'totalGoldEarned': champion['totalGoldEarned'],
                            'mostSpellsCast': champion['mostSpellsCast'],
                            'totalTurretsKilled': champion['totalTurretsKilled'],
                            'totalPhysicalDamageDealt': champion['totalPhysicalDamageDealt'],
                            'totalMagicDamageDealt': champion['totalMagicDamageDealt'],
                            'totalFirstBlood': champion['totalFirstBlood'],
                            'totalAssists': champion['totalAssists'],
                            'maxChampionsKilled': champion['maxChampionsKilled'],
                            'maxNumDeaths': champion['maxNumDeaths'],
                            'label': champion['label']
                        }
                    )
                    pass
                pass
            pass
        pass
    pass


def main():
    import time
    tiers = get_tier()
    for tier, rank_dict in tiers.iteritems():
        print 'starting tier: {}'.format(tier)
        for summoner_id in rank_dict:
            print 'tier: {}, summoner id: {}'.format(tier, summoner_id)
            top_champion = TopChampion(config['key'], summoner_id, tier, 3)
            top_champion.get_top_champions()
            top_champion.save_top_champions()
            time.sleep(1)
        print 'end tier: {}'.format(tier)

if __name__ == '__main__':
    main()
