from model.positionFeatures import positionFiller, posfeatures

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

common_features = ['kills', 'deaths', 'assists', 'gpm', 'xpm', 'duration',]
common_core_features = ['last_hits', 'hero_damage',]
common_sup_features = ['stuns', 'obs_placed', 'sen_placed']

common_obj = [obj['kills'], obj['deaths'], obj['assists'], obj['gpm'], obj['xpm'], obj['duration']]
common_core_obj = [obj['last_hits'], obj['hero_damage']]
common_supp_obj = [obj['stuns'], obj["obs_placed"], obj["sen_placed"]]

class TestPosFeatures:
    def test_posfeatures1(self):
        assert posfeatures(1) == common_features + common_core_features
    
    def test_posfeatures2(self):
        assert posfeatures(2) == common_features + common_core_features + ["rune_pickups"]
    
    def test_posfeatures3(self):
        assert posfeatures(3) == common_features + common_core_features + ["stuns", "tower_damage"]
    
    def test_posfeatures4(self):
        assert posfeatures(4) == common_features + common_sup_features
    
    def test_posfeatures5(self):
        assert posfeatures(5) == common_features + common_sup_features

class TestPositionFiller:
    def test_positionFiller1(self):
         assert positionFiller(obj, 1) == common_obj + common_core_obj

    def test_positionFiller2(self):
          assert positionFiller(obj, 2) == common_obj + common_core_obj + [obj['rune_pickups']]
    
    def test_positionFiller3(self):
        assert positionFiller(obj, 3) == common_obj + common_core_obj + [obj['stuns'], obj['tower_damage']]
    
    def test_positionFiller4(self):
        assert positionFiller(obj, 4) == common_obj + common_supp_obj
    
    def test_positionFiller5(self):
        assert positionFiller(obj, 5) == common_obj + common_supp_obj

