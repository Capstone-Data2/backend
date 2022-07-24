from os import kill
from functions.player import findRank, perMin, killParticipation, lowestGPMFiveMin, killsPerMinTen, percentageGoldGained


class TestFindRank:
    def test_herald(self):
        assert findRank(10) == "herald"

    def test_guardian(self):
        assert findRank(20) == "guardian"

    def test_crusader(self):
        assert findRank(30) == "crusader"

    def test_archon(self):
        assert findRank(40) == "archon"

    def test_legend(self):
        assert findRank(50) == "legend"

    def test_ancient(self):
        assert findRank(60) == "ancient"

    def test_divine(self):
        assert findRank(70) == "divine"

    def test_immortal(self):
        assert findRank(80) == "immortal"

class TestPerformance:
    def test_per_min(self):
        assert perMin(60, 360) == 10
    
    def test_per_min_rounding(self):
        assert perMin(56, 360) == 9.33
    
    def test_kill_participation(self):
        assert killParticipation(True, 10, 20, 10, 10) == 1
        assert killParticipation(True, 10, 20, 10, 0) == 0.5
        
        assert killParticipation(False, 10, 20, 6, 1) == 0.7
        assert killParticipation(False, 0, 20, 0, 0) == 0
        assert killParticipation(True, 10, 0, 0, 0) == 0
    
    def test_lowest_gpm_five_min(self):
        #lowest gpm of 10 at 10 min
        gold_array_1 = [1,2,3,4,5,6,7,8,9,10,100,100,100,100,100, 150, 700, 800, 1100] 
        #lowest gpm of 4 at 12 min
        gold_array_2 = [1,2,3,4,5,6,7,8,9,10,100,100,130,130,130, 130, 130, 150, 1100] 
        #too short of a game
        gold_array_3 = [1,2,3,4,5,6,7,8,9,10]
        assert lowestGPMFiveMin(gold_array_1) == [10, 10]
        assert lowestGPMFiveMin(gold_array_2) == [4, 12]
        assert lowestGPMFiveMin(gold_array_3) == 0

    def test_kills_per_min_for_ten_min(self):
        kills_log=[
            
            {
                'time': 678
            }]
        assert killsPerMinTen(kills_log) == 0
        kills_log.append({'time': 555})
        kills_log.append({'time': 442})
        assert killsPerMinTen(kills_log) == 0.2
    
    def test_percentage_gold_gained(self):
        max_gold =  4185
        assert percentageGoldGained(max_gold)== 1
        assert percentageGoldGained(max_gold/2) == 0.5