
def posfeatures(position):
    common = ['kills', 'deaths', 'assists', 'gpm', 'xpm', 'duration',]
    common_core = ['last_hits', 'hero_damage',]
    common_sup = ['stuns', 'obs_placed', 'sen_placed']
    
    #Carry position 
    if position == 1:
        return common + common_core
    #Midlane position 
    elif position == 2:
        return common + common_core + ["rune_pickups"]
    #Offlane position
    elif position == 3:
        return common + common_core + ["stuns", "tower_damage"]
    #Roamer position 
    elif position == 4:
        return common + common_sup
    #Wimpy Support position
    elif position == 5:
        return common + common_sup

def positionFiller(playermatch, position):
    feature_names = posfeatures(position)
    features = []
    for feature in feature_names:
        features.append(playermatch[feature])
    return features



"""obj = {"kills": 5, "deaths": 2, "assists": 10, "gpm": 500, "xpm": 400, "duration": 700, "last_hits": 150, "hero_damage": 15000}
print(positionFiller(obj, 1))"""