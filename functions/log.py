def getPlayerData(players):
    player_kills = []
    player_runes = []
    for player in players:  
      player_kill_log = {
        str(player['hero_id']): player['kills_log']
      }
      player_rune_log = {
        str(player['hero_id']): player['runes_log']
      }
      player_kills.append(player_kill_log)
      player_runes.append(player_rune_log)
    
    return player_kills, player_runes

def getObjectiveData(objectives):
    towers = []
    roshan = []
    
    for objective in objectives:
      if objective['type'] == 'building_kill':
        towerData = {
          'time' : objective['time'],
          'tower' : objective['key'],
          'unit' : objective['unit'],
        }
        towers.append(towerData)
      
      elif objective['type'] == 'CHAT_MESSAGE_ROSHAN_KILL':
        roshan.append({
          'rosh_kill_time': objective['time'],
          'rosh_kill_team' : objective['team'] 
        })

    return towers, roshan