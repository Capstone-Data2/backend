from functions.player import findRank


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
