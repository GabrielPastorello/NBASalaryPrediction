import os
import pandas as pd

source_folder = os.getcwd()
path_save = os.path.join(source_folder, 'Data')

sep = r'/'

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

arquivos = os.listdir(path_save)

df = pd.DataFrame()
for arquivo in arquivos:
    if arquivo.endswith('.csv') and (arquivo.startswith('20') or arquivo.startswith('19')):
        apoio = pd.read_csv(path_save+sep+arquivo,
                              sep=';', decimal=',', encoding='latin-1')

        apoio['Season'] = int(arquivo.replace('.csv',''))

        df = pd.concat([df,apoio],ignore_index=True)

df = df[df['Tm'].str.len()==3]

df = df[df['Top10_PTS'].notna()]

champions = pd.read_csv(path_save+sep+'champions.csv',
                        sep=',', encoding='latin-1')

champions['Tm'] = champions['Tm'].replace(dict_teams)

champions['Playoff Share'] = champions['Playoff Wins']/champions['Wins Needed']

champions = champions.rename(columns={'Playoff Share':'CLASSE'})

champions = champions[champions['CLASSE'].notna()]

df = df.merge(champions[['Tm','Season','CLASSE']], on=['Tm','Season'], how='left', validate='1:1').fillna(0)

df = df.drop(columns=['COACHES_PL_FR_PCT','COACHES_PL_CA_PCT','COACHES_RS_S_PCT',
                      'COACHES_RS_CA_PCT','COACHES_RS_CA_W%','COACHES_RS_FR_PCT'])

# Desempenho temporadas anteriores
df = df.sort_values(['Tm', 'Season']).reset_index(drop=True)

df['Champion_Share_Previous_Season'] = df.groupby('Tm')['CLASSE'].shift(1).fillna(0)

df['Champion_Share_Last_3_Seasons'] = (
    df
    .groupby('Tm', group_keys=False)
    .apply(lambda g: g['CLASSE'].shift(1).rolling(window=3, min_periods=1).mean())
    .reset_index(drop=True)
).fillna(0)

df.to_csv(path_save+sep+'BASE_FINAL.csv',
            sep=';', decimal=',', encoding='latin-1',index=False)
