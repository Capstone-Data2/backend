from model.predictModel import predictModel


bad_player_1 = [[2, 2, 5, 300, 250, 1800, 250, 1000]]
good_player_1 = [[4, 2, 6, 500, 500, 1800, 250, 5000]]

player_2 =[[4, 2, 6, 500, 500, 1800, 250, 5000, 5]]
player_3 =[[4, 2, 6, 500, 500, 1800, 250, 5000, 34, 1000]]
player_4 =[[4, 2, 6, 500, 500, 1800, 34, 5, 8]]
player_5= [[4, 2, 6, 500, 500, 1800, 34, 5, 8]]

class TestModelPredicttion:
    def test_prediction(self):
        assert predictModel('herald', 1, bad_player_1) == 0.06206617257497607
        assert predictModel('herald', 1, good_player_1) == 0.9878395720283559

        assert predictModel('crusader', 2, player_2) == 0.9665500651350488
        assert predictModel('archon', 3, player_3) == 0.9541003627111506

        assert predictModel('crusader', 4, player_4) == 0.9554857455542284
        assert predictModel('archon', 5, player_5) == 0.9124103273138414