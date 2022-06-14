
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

