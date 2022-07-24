from functions.log import getPlayerData, getObjectiveData

class TestLog:
    def test_player_data(self):
        players =[{'hero_id': 12, 'kills_log': ['kills', 'and more kills'], 'runes_log':['runes', 'and more runes']}, 
        {'hero_id': 16, 'kills_log': ['kills', 'and even more kills'], 'runes_log': ['runes', 'and even more runes']}]
        
        kills, runes = getPlayerData(players)
        assert kills == [{'12': ['kills', 'and more kills']}, {'16': ['kills', 'and even more kills'] }]
        assert runes == [{'12': ['runes', 'and more runes']}, {'16': ['runes', 'and even more runes'] }]

    def test_objectives_data(self):
        objectives = [{'type': 'building_kill', 'time': 213, 'key': 'top', 'unit': 'marci'}, 
        {"type": 'CHAT_MESSAGE_ROSHAN_KILL', 'time': 123, 'team': 2},
        {"type": 'COURRIER_KILL', 'time': 123, 'team': 2},]

        towers, roshan = getObjectiveData(objectives)
        assert towers == [{'time': 213, 'tower': 'top', 'unit': 'marci'}]
        assert roshan == [{'rosh_kill_time': 123,'rosh_kill_team' : 2 }]