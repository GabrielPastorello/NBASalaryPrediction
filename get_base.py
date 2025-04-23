from BRScraper import nba
import numpy as np
import pandas as pd
import os

source_folder = os.getcwd()
path_save = os.path.join(source_folder, 'Data')

sep = r'/'

seasons = [x for x in range(2025, 1983, -1)]

dict_teams = {'Utah Jazz':'UTA','Phoenix Suns':'PHO',
             'Philadelphia 76ers':'PHI','Brooklyn Nets':'BRK',
             'Denver Nuggets':'DEN','Los Angeles Clippers':'LAC',
             'Milwaukee Bucks':'MIL','Dallas Mavericks':'DAL',
             'Los Angeles Lakers':'LAL','Portland Trail Blazers':'POR',
             'Atlanta Hawks':'ATL','New York Knicks':'NYK',
             'Miami Heat':'MIA','Golden State Warriors':'GSW',
             'Memphis Grizzlies':'MEM','Boston Celtics':'BOS',
             'Washington Wizards':'WAS','Indiana Pacers':'IND',
             'Charlotte Hornets':'CHO','Charlotte Bobcats':'CHA',
             'San Antonio Spurs':'SAS','Chicago Bulls':'CHI',
             'New Orleans Pelicans':'NOP','Sacramento Kings':'SAC',
             'Toronto Raptors':'TOR','Minnesota Timberwolves':'MIN',
             'Cleveland Cavaliers':'CLE','Oklahoma City Thunder':'OKC',
             'Orlando Magic':'ORL','Detroit Pistons':'DET',
             'Houston Rockets':'HOU','New Jersey Nets':'NJN',
             'New Orleans Hornets':'NOH','Seattle SuperSonics':'SEA',
             'Vancouver Grizzlies':'VAN','Washington Bullets':'WSB',
             'Kansas City Kings':'KCK','San Diego Clippers':'SDC'}

for season in seasons:

    ### Regular Season Standings ###
    standings = nba.get_standings(season, info='total')

    standings['Tm'] = standings['Tm'].str.replace('*','')

    standings = standings[standings['Tm'].str.contains(' Division')==False].reset_index(drop=True)

    if season==2025:
        standings['Tm'] = standings['Tm'].str.split(r'\s*\(', expand=True)[0]

    standings['Tm'] = standings['Tm'].replace(dict_teams)

    standings['Seed'] = standings.index + 1

    cols_float = ['W/L%','PS/G','PA/G','SRS']
    standings[cols_float] = standings[cols_float].astype(float)

    standings['Rank_PS/G'] = standings['PS/G'].rank(ascending=False, method='dense').astype(int)
    standings['Rank_PA/G'] = standings['PA/G'].rank(ascending=True, method='dense').astype(int)
    standings['Rank_SRS'] = standings['SRS'].rank(ascending=False, method='dense').astype(int)

    standings = standings.drop(columns=['W','L'])

    ### Coaches Info ###
    coaches = nba.get_coach_data(season)

    coaches = coaches.drop_duplicates('Tm',keep='last')

    coaches['RS_S_PCT'] = coaches['RS_S_W']/coaches['RS_S_G']
    coaches['RS_FR_PCT'] = coaches['RS_FR_W']/coaches['RS_FR_G']
    coaches['RS_CA_PCT'] = coaches['RS_CA_W']/coaches['RS_CA_G']

    coaches['PL_FR_PCT'] = coaches['PL_FR_W']/coaches['PL_FR_G']
    coaches['PL_CA_PCT'] = coaches['PL_CA_W']/coaches['PL_CA_G']

    coaches = coaches.fillna(-1)

    coaches = coaches.drop(columns=['Coach','RS_S_G','RS_S_W', 'RS_S_L', 'RS_FR_G',
                                    'RS_FR_W', 'RS_FR_L', 'RS_CA_G','RS_CA_W',
                                    'RS_CA_L','PL_S_G', 'PL_S_W', 'PL_S_L',
                                    'PL_FR_G', 'PL_FR_W', 'PL_FR_L', 'PL_CA_G',
                                    'PL_CA_W', 'PL_CA_L'])

    coaches.columns = ['COACHES_' + x.replace(' ', '_') if x != 'Tm' else x for x in coaches.columns]

    ### Player Stats info - Per Game ###
    stats = nba.get_stats(season, info='per_game', playoffs=False, rename=False)

    stats = stats.rename(columns={'Team':'Tm'})

    stats = stats[(stats['G']>30)&(stats['Tm'].str.endswith('TM')==False)]

    stats[['3P%','FT%']] = stats[['3P%','FT%']].fillna(0)

    # All star in that season
    stats['Awards'] = stats['Awards'].fillna('-')
    stats['ALL_STAR'] = (stats['Awards'].str.contains('AS')).astype(int)

    # Averages
    stats['Top3_PTS'] = np.where(stats['PTS'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_AST'] = np.where(stats['AST'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_REB'] = np.where(stats['TRB'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_FG'] = np.where(stats['FG'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_FG%'] = np.where(stats['FG%'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_3P'] = np.where(stats['3P'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_3P%'] = np.where(stats['3P%'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_FT'] = np.where(stats['FT'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_FT%'] = np.where(stats['FT%'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_STL'] = np.where(stats['STL'].rank(ascending=False).astype(int)<=3,1,0)
    stats['Top3_BLK'] = np.where(stats['BLK'].rank(ascending=False).astype(int)<=3,1,0)
    
    stats['Top10_PTS'] = np.where(stats['PTS'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_AST'] = np.where(stats['AST'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_REB'] = np.where(stats['TRB'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_FG'] = np.where(stats['FG'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_FG%'] = np.where(stats['FG%'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_3P'] = np.where(stats['3P'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_3P%'] = np.where(stats['3P%'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_FT'] = np.where(stats['FT'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_FT%'] = np.where(stats['FT%'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_STL'] = np.where(stats['STL'].rank(ascending=False).astype(int)<=10,1,0)
    stats['Top10_BLK'] = np.where(stats['BLK'].rank(ascending=False).astype(int)<=10,1,0)

    stats['Top30_PTS'] = np.where(stats['PTS'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_AST'] = np.where(stats['AST'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_REB'] = np.where(stats['TRB'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_FG'] = np.where(stats['FG'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_FG%'] = np.where(stats['FG%'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_3P'] = np.where(stats['3P'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_3P%'] = np.where(stats['3P%'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_FT'] = np.where(stats['FT'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_FT%'] = np.where(stats['FT%'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_STL'] = np.where(stats['STL'].rank(ascending=False).astype(int)<=30,1,0)
    stats['Top30_BLK'] = np.where(stats['BLK'].rank(ascending=False).astype(int)<=30,1,0)

    stats = stats.groupby(['Tm']).agg({'Age':'mean','ALL_STAR':'sum',
                                       'Top3_PTS':'sum','Top10_PTS':'sum','Top30_PTS':'sum',
                                       'Top3_AST':'sum','Top10_AST':'sum','Top30_AST':'sum',
                                       'Top3_REB':'sum','Top10_REB':'sum','Top30_REB':'sum',
                                       'Top3_FG':'sum','Top10_FG':'sum','Top30_FG':'sum',
                                       'Top3_FG%':'sum','Top10_FG%':'sum','Top30_FG%':'sum',
                                       'Top3_3P':'sum','Top10_3P':'sum','Top30_3P':'sum',
                                       'Top3_3P%':'sum','Top10_3P%':'sum','Top30_3P%':'sum',
                                       'Top3_FT':'sum','Top10_FT':'sum','Top30_FT':'sum',
                                       'Top3_FT%':'sum','Top10_FT%':'sum','Top30_FT%':'sum',
                                       'Top3_STL':'sum','Top10_STL':'sum','Top30_STL':'sum',
                                       'Top3_BLK':'sum','Top10_BLK':'sum','Top30_BLK':'sum'}).reset_index()

    ### Player Stats info - Advanced ###
    adv = nba.get_stats(season, info='advanced', playoffs=False, rename=False)

    adv = adv.rename(columns={'Team':'Tm'})

    adv = adv[(adv['G']>30)&(adv['Tm'].str.endswith('TM')==False)]

    # Averages
    adv['Top3_PER'] = np.where(adv['PER'].rank(ascending=False).astype(int)<=3,1,0)
    adv['Top3_WS'] = np.where(adv['WS'].rank(ascending=False).astype(int)<=3,1,0)
    adv['Top3_WS/48'] = np.where(adv['WS/48'].rank(ascending=False).astype(int)<=3,1,0)
    adv['Top3_VORP'] = np.where(adv['VORP'].rank(ascending=False).astype(int)<=3,1,0)
    adv['Top3_BPM'] = np.where(adv['BPM'].rank(ascending=False).astype(int)<=3,1,0)
    adv['Top3_USG%'] = np.where(adv['USG%'].rank(ascending=False).astype(int)<=3,1,0)
    
    adv['Top10_PER'] = np.where(adv['PER'].rank(ascending=False).astype(int)<=10,1,0)
    adv['Top10_WS'] = np.where(adv['WS'].rank(ascending=False).astype(int)<=10,1,0)
    adv['Top10_WS/48'] = np.where(adv['WS/48'].rank(ascending=False).astype(int)<=10,1,0)
    adv['Top10_VORP'] = np.where(adv['VORP'].rank(ascending=False).astype(int)<=10,1,0)
    adv['Top10_BPM'] = np.where(adv['BPM'].rank(ascending=False).astype(int)<=10,1,0)
    adv['Top10_USG%'] = np.where(adv['USG%'].rank(ascending=False).astype(int)<=10,1,0)

    adv['Top30_PER'] = np.where(adv['PER'].rank(ascending=False).astype(int)<=30,1,0)
    adv['Top30_WS'] = np.where(adv['WS'].rank(ascending=False).astype(int)<=30,1,0)
    adv['Top30_WS/48'] = np.where(adv['WS/48'].rank(ascending=False).astype(int)<=30,1,0)
    adv['Top30_VORP'] = np.where(adv['VORP'].rank(ascending=False).astype(int)<=30,1,0)
    adv['Top30_BPM'] = np.where(adv['BPM'].rank(ascending=False).astype(int)<=30,1,0)
    adv['Top30_USG%'] = np.where(adv['USG%'].rank(ascending=False).astype(int)<=30,1,0)

    adv = adv.groupby(['Tm']).agg({'Top3_PER':'sum','Top10_PER':'sum','Top30_PER':'sum',
                                   'Top3_WS':'sum','Top10_WS':'sum','Top30_WS':'sum',
                                   'Top3_WS/48':'sum','Top10_WS/48':'sum','Top30_WS/48':'sum',
                                   'Top3_VORP':'sum','Top10_VORP':'sum','Top30_VORP':'sum',
                                   'Top3_BPM':'sum','Top10_BPM':'sum','Top30_BPM':'sum',
                                   'Top3_USG%':'sum','Top10_USG%':'sum','Top30_USG%':'sum'}).reset_index()

    ### Team Ratings ###
    team = nba.get_team_ratings(season)

    team = team.rename(columns={'Team':'Tm'})
    team['Tm'] = team['Tm'].replace(dict_teams)

    team = team.drop(columns=['Rk', 'Conf', 'Div', 'W', 'L', 'W/L%'])

    team['Rank_MOV'] = team['MOV'].rank(ascending=False).astype(int)
    team['Rank_ORtg'] = team['ORtg'].rank(ascending=False).astype(int)
    team['Rank_DRtg'] = 31 - team['DRtg'].rank(ascending=False).astype(int)
    team['Rank_NRtg'] = team['NRtg'].rank(ascending=False).astype(int)
    team['Rank_MOV/A'] = team['MOV/A'].rank(ascending=False).astype(int)
    team['Rank_ORtg/A'] = team['ORtg/A'].rank(ascending=False).astype(int)
    team['Rank_DRtg/A'] = 31 - team['DRtg/A'].rank(ascending=False).astype(int)
    team['Rank_NRtg/A'] = team['NRtg/A'].rank(ascending=False).astype(int)
    
    # Merges
    df = standings.merge(coaches, how='left', on='Tm', validate='1:1')
    df = df.merge(stats, how='left', on='Tm', validate='1:1')
    df = df.merge(adv, how='left', on='Tm', validate='1:1')
    df = df.merge(team, how='left', on='Tm', validate='1:1')

    df.to_csv(path_save+sep+str(season)+'.csv',
              sep=';', decimal=',', encoding='latin-1',index=False)
    print(season)
