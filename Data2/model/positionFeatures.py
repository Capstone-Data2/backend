
def posfeatures(position):
    #Carry position 
    if position == 1:
        return [
            'kills', 
            'deaths', 
            'assists', 
            'gpm', 
            'xpm', 
            'duration',
            'last_hits',
            'hero_damage',
            ]
    
    elif position == 2:
        #Midlane position 
        return [
            'kills', 
            'deaths', 
            'assists', 
            'gpm', 
            'xpm', 
            'duration',
            'last_hits',
            'hero_damage',
            'rune_pickups'
            ]
    elif position == 3:
        #Offlane position 
        return [
            'kills', 
            'deaths', 
            'assists', 
            'gpm', 
            'xpm', 
            'duration',
            'last_hits',
            'hero_damage',
            'stuns',
            'tower_damage'
            ]
    elif position == 4:
        #Roamer position 
        return [
            'kills', 
            'deaths', 
            'assists', 
            'gpm', 
            'xpm', 
            'duration',
            'stuns',
            'obs_placed',
            'sen_placed'

            ]
    elif position == 5:
        #Wimpy Support position 
        return [
            'kills', 
            'deaths', 
            'assists', 
            'gpm', 
            'xpm', 
            'duration',
            'stuns',
            'obs_placed',
            'sen_placed'
            ]

def positionFiller(playermatch, position):
    if position == 1:
         return [
            playermatch['kills'], 
            playermatch['deaths'], 
            playermatch['assists'], 
            playermatch['gpm'], 
            playermatch['xpm'], 
            playermatch['duration'],
            playermatch['last_hits'],
            playermatch['hero_damage'],
            ]
    if position == 2:
        return [
            playermatch['kills'], 
            playermatch['deaths'], 
            playermatch['assists'], 
            playermatch['gpm'], 
            playermatch['xpm'], 
            playermatch['duration'],
            playermatch['last_hits'],
            playermatch['hero_damage'],
            playermatch['rune_pickups']
            ]
    if position == 3:
        return [
            playermatch['kills'], 
            playermatch['deaths'], 
            playermatch['assists'], 
            playermatch['gpm'], 
            playermatch['xpm'], 
            playermatch['duration'],
            playermatch['last_hits'],
            playermatch['hero_damage'],
            playermatch['stuns'],
            playermatch['tower_damage']
            ]
    if position == 4:
        return [
            playermatch['kills'], 
            playermatch['deaths'], 
            playermatch['assists'], 
            playermatch['gpm'], 
            playermatch['xpm'], 
            playermatch['duration'],
            playermatch['stuns'],
            playermatch['obs_placed'],
            playermatch['sen_placed']

            ]

    if position == 5:
        return [
            playermatch['kills'], 
            playermatch['deaths'], 
            playermatch['assists'], 
            playermatch['gpm'], 
            playermatch['xpm'], 
            playermatch['duration'],
            playermatch['stuns'],
            playermatch['obs_placed'],
            playermatch['sen_placed']
            ]