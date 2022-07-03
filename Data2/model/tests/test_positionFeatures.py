from model.positionFeatures import positionFiller

obj = {
    "kills": 5, 
    "deaths": 2, 
    "assists": 10, 
    "gpm": 500, 
    "xpm": 400, 
    "duration": 700, 
    "last_hits": 150, 
    "hero_damage": 15000, 
    "rune_pickups": 3, 
    "stuns": 10, 
    "tower_damage": 4000,
    "obs_placed": 4,
    "sen_placed": 3
}

def test_positionFiller():
    assert positionFiller(obj, 1) == [obj['kills'], obj['deaths'], obj['assists'], obj['gpm'], obj['xpm'], obj['duration'], obj['last_hits'], obj['hero_damage']]
    assert positionFiller(obj, 2) == [obj['kills'], obj['deaths'], obj['assists'], obj['gpm'], obj['xpm'], obj['duration'], obj['last_hits'], obj['hero_damage'], obj['rune_pickups']]
    assert positionFiller(obj, 3) == [obj['kills'], obj['deaths'], obj['assists'], obj['gpm'], obj['xpm'], obj['duration'], obj['last_hits'], obj['hero_damage'], obj['stuns'], obj['tower_damage']]
    assert positionFiller(obj, 4) == [obj['kills'], obj['deaths'], obj['assists'], obj['gpm'], obj['xpm'], obj['duration'], obj['stuns'], obj["obs_placed"], obj["sen_placed"]]
    assert positionFiller(obj, 5) == [obj['kills'], obj['deaths'], obj['assists'], obj['gpm'], obj['xpm'], obj['duration'], obj['stuns'], obj["obs_placed"], obj["sen_placed"]]