from model.predictModel import predictModel


bad_player_1 = [[2, 2, 5, 300, 250, 1800, 250, 1000]]
good_player_1 = [[4, 2, 6, 500, 500, 1800, 250, 5000]]

player_2 =[[4, 2, 6, 500, 500, 1800, 250, 5000, 5]]
player_3 =[[4, 2, 6, 500, 500, 1800, 250, 5000, 34, 1000]]
player_4 =[[4, 2, 6, 500, 500, 1800, 34, 5, 8]]
player_5= [[4, 2, 6, 500, 500, 1800, 34, 5, 8]]

class TestModelPredicttion:
    def test_prediction(self):
        assert predictModel('herald', 1, bad_player_1) == 0.062066
        assert predictModel('herald', 1, good_player_1) == 0.98784

        assert predictModel('crusader', 2, player_2) == 0.96655
        assert predictModel('archon', 3, player_3) == 0.9541

        assert predictModel('crusader', 4, player_4) == 0.955486
        assert predictModel('archon', 5, player_5) == 0.912410