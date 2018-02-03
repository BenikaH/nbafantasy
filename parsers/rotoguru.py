import logging
import re

from bs4 import BeautifulSoup

from nba.dates import convert_format
from nba.seasons import in_what_season

class RotoGuruNBAParser:
    '''
    RotoGuruNBAParser

    Usage:
        site = 'dk'
        p = RotoGuruNBAParser()

        from RotoGuruNBAScraper import RotoGuruNBAScraper
        s = RotoGuruNBAScraper()
        content = s.salaries_day('2015-12-09', 'dk')
        salaries = p.salaries(content, site)
        players = p.players(content, site)
    '''

    def __init__(self):
        logging.getLogger(__name__).addHandler(logging.NullHandler())


    def _pre_ssv(self, content):
        '''
        Parses rotoguru <pre> block into a list of ssv lines
        
        Arguments:
            content (str): HTML string

        Returns:
            rows (list): each item is a string of semicolon-separated values
        '''

        # rotoguru encloses SSV lines in a <pre> block, need to get that first and then split on newline
        pattern = re.compile(r'<pre>(Date;.*?)</pre>',  re.IGNORECASE | re.MULTILINE | re.DOTALL)
        match = re.search(pattern, content)

        if match:
            ssv = match.group(1)
            rows = ssv.split('\n')
            return rows

        else:
            return None           


    def _salaries_headers(self, row=None):
        '''
        Provides headers for salaries method
        TODO: parse the actual headers rather than pre-supplied headers

        Arguments:
            row (str): string of semicolon-separated values

        Returns:
            headers (list): list of strings, each representing header / column name
        '''

        if row:
            pass
            #Original rotoguru headers --- Date;GID;Pos;Name;Starter;DK Pts;DK Salary;Team;H/A;Oppt;Team Score;Oppt Score;Minutes;Stat line
            #return ['game_date', 'rotoguru_gid', 'site_player_position', 'site_player_name', 'starter', 'points', 'salary', 'team_abbreviation',
            #    'venue', 'opponent_team', 'team_score', 'opponent_score', 'min', 'stat_line']
        
        else:
            return ['game_date', 'rotoguru_gid', 'site_position', 'site_player_name', 'starter', 'points', 'salary', 'team_abbreviation', 'venue', 'opponent_team', 'team_score', 'opponent_score', 'min', 'stat_line']


    def players(self, content, site):
        '''
        Returns list of dictionaries with player salary/points information from rotoguru

        Arguments:
            content (str): HTML string
            site (str): name of site ('dk', 'fd', 'yh', etc.)

        Returns:
            players (list): list of dictionaries representing player & his salary on a given date on a given site

        Usage:
            players = p.players(content, 'dk')
            
        '''

        pass
            
        ''' NOT NEEDED AT THIS TIME
        # team abbreviations should be uppercase
        t = player.get('team_abbreviation', None)

        if t:
            player['team_abbreviation'] = t.upper()

        t = player.get('opponent_team', None)

        if t:
            player['opponent_team'] = t.upper()
    
        points = player.get('points', None)
        minutes = player.get('min', None)

        '''

        ''' NOT NEEDED AT THIS TIME
        # player value
        if minutes == 'DNP' or minutes == 'NA':
            pass
            
        else:
            try:
                player['points_per_minute'] = float(points)/float(minutes)
                player['multiple'] = float(points)/(player['salary']/1000)

            except:
                logging.error('could not convert {0} {1}'.format(points, minutes))

        # fix missing - want NULL value instead of empty string
        stat_line = player.get('stat_line', None)
        starter = player.get('starter', None)

        if not stat_line or stat_line == '':
            player['stat_line'] = None
            
        if not starter or player['starter'] == '':
            player['starter'] = 0
        '''             


    def salaries(self, content, game_date, site, ssv='0'):
        '''
        Returns list of dictionaries with player salary information

        Arguments:
            content (str): HTML string
            game_date (str): likely YYYYmmdd
            site (str): name of site ('dk', 'fd', 'yh', etc.)

        Returns:
            salaries (list): list of dictionaries representing player & his salary on a given date on a given site
        '''
        sals = []
        if ssv == '1':
            rows = self._pre_ssv(content)
            headers = self._salaries_headers()
            wanted = ['game_date', 'site_position', 'site_player_name', 'salary']
            for row in rows[1:]:
                cells = row.split(';')
                sal = {k:v for k,v in dict(list(zip(headers, cells))).items() if k in wanted}
                sal['site'] = site
                if sal.get('salary', None):
                    sal['salary'] = re.sub("[^0-9]", "", sal['salary'])
                sals.append(sal)
        else:
            season = int(in_what_season(game_date)[0:4]) + 1
            soup = BeautifulSoup(content, 'lxml')
            t = soup.find('table', {'cellspacing': 5})
            headers = ['dfs_site', 'season', 'game_date', 'source', 'source_player_id', 'source_player_name', 'team_code',
               'dfs_position', 'salary']
            for tr in t.find_all('tr'):
                try:
                    tds = tr.find_all('td')
                    a = tr.find('a')
                    if a and a.get('href', '') and '?' in a.get('href'):
                        source_player_id = int(a.get('href', '').split('?')[1].replace('x', ''))
                        dfs_position = tds[0].text
                        source_player_name = a.text.replace('^', '').replace('*', '')
                        salary = int(tds[3].text.replace('$', '').replace(',', ''))
                        team_code = tds[4].text.strip().upper()
                        vals = ['dk', season, convert_format(game_date, 'nba'), 'rotoguru', source_player_id,
                                    source_player_name, team_code,
                                    dfs_position, salary]
                        sals.append(dict(zip(headers, vals)))
                except Exception as e:
                    logging.exception(e)
        return sals


if __name__ == '__main__':
    pass
