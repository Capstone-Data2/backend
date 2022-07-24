from os import kill
from functions.player import (
    findRank,
    perMin,
    killParticipation,
    lowestGPMFiveMin,
    killsPerMinTen,
    percentageGoldGained,
    common,
    commonCore,
    commonSup,
    rivalResponse,
    pos1Rival,
    pos2Rival,
    pos3Rival,
    pos4Rival,
    pos5Rival,
    checkRanks,
    fixExcess,
    findHighestAndLowest,
    findRole,
)


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

class TestRivals:
    def test_common(self):
        player = setupPlayerTestingObject(1)
        common_resp = common(player, "immortal")
        player["name"] = player["personaname"]
        player["HDM"] = round(player["hero_damage"] / (player["duration"] / 60), 2)
        player["buybacks"] = player["buyback_log"]
        player["deaths_per_min"] = round(
            player["deaths"] / (player["duration"] / 60), 2
        )
        player["predicted_win"] = 99.666
        del (
            player["gpm"],
            player["xpm"],
            player["last_hits"],
            player["personaname"],
            player["buyback_log"],
            player["duration"],
            player["kill_streaks"],
            player["multi_kills"],
            player["kills_log"],
            player["camps_stacked"],
            player["stuns"],
            player["max_hero_hit"],
            player["runes_log"],
            player["tower_damage"],
            player["damage_taken"],
            player["is_roaming"],
            player["obs_placed"],
            player["sen_placed"],
            player["hero_healing"],
        )
        assert common_resp == player

    def test_commonCore(self):
        player = setupPlayerTestingObject(1)
        commonCore_resp = commonCore(player)
        expected_resp = {
            "last_hits": player["last_hits"],
            "lane_kills": 2,
            "multi_kills": 4,
            "XPM": 550,
            "GPM": 500,
            "kill_streaks": 2,
            "lane_performance": 0.003,
        }
        assert commonCore_resp == expected_resp

    def test_commonSup(self):
        player = setupPlayerTestingObject(5)
        commonSup_resp = commonSup(player)
        expected_resp = {
            "camps_stacked": player["camps_stacked"],
            "stuns": player["stuns"],
        }
        assert commonSup_resp == expected_resp

    def test_pos1Rival(self):
        player = setupPlayerTestingObject(1)
        pos1Rival_resp = pos1Rival(player)
        expected_resp = {
            "KPM": 0.48,
            "max_hero_hit": player["max_hero_hit"],
            "lowest_gpm": [1.0, 10],
            "LHM": 6.0,
        }
        assert pos1Rival_resp == expected_resp

    def test_pos2Rival(self):
        player = setupPlayerTestingObject(2)
        pos2Rival_resp = pos2Rival(player)
        expected_resp = {
            "runes_picked_up": player["runes_log"],
            "KPM": 0.48,
            "max_hero_hit": player["max_hero_hit"],
            "lowest_gpm": [1.0, 10],
            "LHM": 6.0,
        }
        assert pos2Rival_resp == expected_resp

    def test_pos3Rival(self):
        player = setupPlayerTestingObject(3)
        pos3Rival_resp = pos3Rival(player)
        expected_resp = {
            "tower_damage": player["tower_damage"],
            "TDM": 60.0,
            "damage_taken": player["damage_taken"],
            "stuns": round(player["stuns"], 2),
        }
        assert pos3Rival_resp == expected_resp

    def test_pos4Rival(self):
        player = setupPlayerTestingObject(4)
        pos4Rival_resp = pos4Rival(player)
        expected_resp = {
            "runes_picked_up": player["runes_log"],
            "is_roaming": player["is_roaming"],
        }
        assert pos4Rival_resp == expected_resp

    def test_pos5Rival(self):
        player = setupPlayerTestingObject(5)
        pos5Rival_resp = pos5Rival(player)
        expected_resp = {
            "obs_placed": player["obs_placed"],
            "sen_placed": player["sen_placed"],
            "hero_healing": player["hero_healing"],
            "HHM": 33.96,
        }
        assert pos5Rival_resp == expected_resp

    def test_rivalResponse1(self):
        player = setupPlayerTestingObject(1)
        rivalResponse_1 = rivalResponse(player, "immortal")
        player["name"] = player["personaname"]
        player["HDM"] = round(player["hero_damage"] / (player["duration"] / 60), 2)
        player["buybacks"] = player["buyback_log"]
        player["deaths_per_min"] = round(
            player["deaths"] / (player["duration"] / 60), 2
        )
        player["predicted_win"] = 99.666
        player["GPM"] = 500
        player["XPM"] = 550
        player["lane_kills"] = 2
        player["lane_performance"] = 0.003
        player["LHM"] = 6.0
        player["KPM"] = 0.48
        player["lowest_gpm"] = [1.0, 10]
        del (
            player["gpm"],
            player["xpm"],
            player["personaname"],
            player["buyback_log"],
            player["duration"],
            player["kills_log"],
            player["camps_stacked"],
            player["stuns"],
            player["runes_log"],
            player["tower_damage"],
            player["damage_taken"],
            player["is_roaming"],
            player["obs_placed"],
            player["sen_placed"],
            player["hero_healing"],
        )
        assert rivalResponse_1 == player

    def test_rivalResponse2(self):
        player = setupPlayerTestingObject(2)
        player["rune_pickups"] = player["runes_log"]
        rivalResponse_2 = rivalResponse(player, "immortal")
        player["name"] = player["personaname"]
        player["HDM"] = round(player["hero_damage"] / (player["duration"] / 60), 2)
        player["buybacks"] = player["buyback_log"]
        player["deaths_per_min"] = round(
            player["deaths"] / (player["duration"] / 60), 2
        )
        player["predicted_win"] = 99.966
        player["GPM"] = 500
        player["XPM"] = 550
        player["lane_kills"] = 2
        player["lane_performance"] = 0.003
        player["LHM"] = 6.0
        player["KPM"] = 0.48
        player["lowest_gpm"] = [1.0, 10]
        player["runes_picked_up"] = player["runes_log"]
        del (
            player["gpm"],
            player["xpm"],
            player["personaname"],
            player["buyback_log"],
            player["duration"],
            player["kills_log"],
            player["camps_stacked"],
            player["stuns"],
            player["runes_log"],
            player["tower_damage"],
            player["damage_taken"],
            player["is_roaming"],
            player["obs_placed"],
            player["sen_placed"],
            player["hero_healing"],
            player["rune_pickups"],
        )
        assert rivalResponse_2 == player

    def test_rivalResponse3(self):
        player = setupPlayerTestingObject(3)
        rivalResponse_3 = rivalResponse(player, "immortal")
        player["name"] = player["personaname"]
        player["HDM"] = round(player["hero_damage"] / (player["duration"] / 60), 2)
        player["buybacks"] = player["buyback_log"]
        player["deaths_per_min"] = round(
            player["deaths"] / (player["duration"] / 60), 2
        )
        player["predicted_win"] = 99.573
        player["GPM"] = 500
        player["XPM"] = 550
        player["lane_kills"] = 2
        player["lane_performance"] = 0.003
        player["TDM"] = 60
        del (
            player["gpm"],
            player["xpm"],
            player["personaname"],
            player["buyback_log"],
            player["duration"],
            player["kills_log"],
            player["camps_stacked"],
            player["runes_log"],
            player["is_roaming"],
            player["obs_placed"],
            player["sen_placed"],
            player["hero_healing"],
            player["max_hero_hit"],
        )
        assert rivalResponse_3 == player

    def test_rivalResponse4(self):
        player = setupPlayerTestingObject(4)
        rivalResponse_4 = rivalResponse(player, "immortal")
        player["name"] = player["personaname"]
        player["HDM"] = round(player["hero_damage"] / (player["duration"] / 60), 2)
        player["buybacks"] = player["buyback_log"]
        player["deaths_per_min"] = round(
            player["deaths"] / (player["duration"] / 60), 2
        )
        player["predicted_win"] = 99.817
        player["runes_picked_up"] = player["runes_log"]
        del (
            player["gpm"],
            player["xpm"],
            player["personaname"],
            player["buyback_log"],
            player["duration"],
            player["kills_log"],
            player["runes_log"],
            player["obs_placed"],
            player["sen_placed"],
            player["hero_healing"],
            player["max_hero_hit"],
            player["damage_taken"],
            player["last_hits"],
            player["multi_kills"],
            player["kill_streaks"],
            player["tower_damage"],
        )
        assert rivalResponse_4 == player

    def test_rivalResponse5(self):
        player = setupPlayerTestingObject(5)
        rivalResponse_5 = rivalResponse(player, "immortal")
        player["name"] = player["personaname"]
        player["HDM"] = round(player["hero_damage"] / (player["duration"] / 60), 2)
        player["buybacks"] = player["buyback_log"]
        player["deaths_per_min"] = round(
            player["deaths"] / (player["duration"] / 60), 2
        )
        player["predicted_win"] = 99.963
        player["HHM"] = 33.96
        del (
            player["gpm"],
            player["xpm"],
            player["personaname"],
            player["buyback_log"],
            player["duration"],
            player["kills_log"],
            player["runes_log"],
            player["max_hero_hit"],
            player["damage_taken"],
            player["last_hits"],
            player["multi_kills"],
            player["kill_streaks"],
            player["tower_damage"],
            player["is_roaming"],
        )
        assert rivalResponse_5 == player


class TestCheckingRanks:
    expected_players = [
        {"hero_id": 1, "lane_role": 1, "ml_lane_role": 1, "net_worth": 10000},
        {"hero_id": 2, "lane_role": 1, "ml_lane_role": 5, "net_worth": 5000},
        {"hero_id": 3, "lane_role": 2, "ml_lane_role": 2, "net_worth": 15000},
        {"hero_id": 4, "lane_role": 3, "ml_lane_role": 4, "net_worth": 7800},
        {"hero_id": 5, "lane_role": 3, "ml_lane_role": 3, "net_worth": 12000},
    ]
    all_expected_players = [
        {
            "hero_id": 1,
            "lane_role": 1,
            "ml_lane_role": 1,
            "net_worth": 10000,
            "is_radiant": True,
        },
        {
            "hero_id": 2,
            "lane_role": 1,
            "ml_lane_role": 5,
            "net_worth": 5000,
            "is_radiant": True,
        },
        {
            "hero_id": 3,
            "lane_role": 2,
            "ml_lane_role": 2,
            "net_worth": 15000,
            "is_radiant": True,
        },
        {
            "hero_id": 4,
            "lane_role": 3,
            "ml_lane_role": 4,
            "net_worth": 7800,
            "is_radiant": True,
        },
        {
            "hero_id": 5,
            "lane_role": 3,
            "ml_lane_role": 3,
            "net_worth": 12000,
            "is_radiant": True,
        },
        {
            "hero_id": 6,
            "lane_role": 1,
            "ml_lane_role": 1,
            "net_worth": 11200,
            "is_radiant": False,
        },
        {
            "hero_id": 7,
            "lane_role": 1,
            "ml_lane_role": 5,
            "net_worth": 6150,
            "is_radiant": False,
        },
        {
            "hero_id": 8,
            "lane_role": 2,
            "ml_lane_role": 2,
            "net_worth": 17500,
            "is_radiant": False,
        },
        {
            "hero_id": 9,
            "lane_role": 3,
            "ml_lane_role": 4,
            "net_worth": 6300,
            "is_radiant": False,
        },
        {
            "hero_id": 10,
            "lane_role": 3,
            "ml_lane_role": 3,
            "net_worth": 14200,
            "is_radiant": False,
        },
    ]

    def test_checkRanksEven(self):
        players = [
            {
                "hero_id": 1,
                "lane_role": 1,
                "ml_lane_role": 1,
                "net_worth": 10000,
                "is_radiant": True,
            },
            {
                "hero_id": 2,
                "lane_role": 1,
                "ml_lane_role": 5,
                "net_worth": 5000,
                "is_radiant": True,
            },
            {
                "hero_id": 3,
                "lane_role": 2,
                "ml_lane_role": 2,
                "net_worth": 15000,
                "is_radiant": True,
            },
            {
                "hero_id": 4,
                "lane_role": 3,
                "ml_lane_role": 4,
                "net_worth": 7800,
                "is_radiant": True,
            },
            {
                "hero_id": 5,
                "lane_role": 3,
                "ml_lane_role": 3,
                "net_worth": 12000,
                "is_radiant": True,
            },
            {
                "hero_id": 6,
                "lane_role": 1,
                "ml_lane_role": 1,
                "net_worth": 11200,
                "is_radiant": False,
            },
            {
                "hero_id": 7,
                "lane_role": 1,
                "ml_lane_role": 5,
                "net_worth": 6150,
                "is_radiant": False,
            },
            {
                "hero_id": 8,
                "lane_role": 2,
                "ml_lane_role": 2,
                "net_worth": 17500,
                "is_radiant": False,
            },
            {
                "hero_id": 9,
                "lane_role": 3,
                "ml_lane_role": 4,
                "net_worth": 6300,
                "is_radiant": False,
            },
            {
                "hero_id": 10,
                "lane_role": 3,
                "ml_lane_role": 3,
                "net_worth": 14200,
                "is_radiant": False,
            },
        ]
        checked_players = checkRanks(players)
        assert checked_players == self.all_expected_players

    def test_checkRanks(self):
        players = [
            {
                "hero_id": 1,
                "lane_role": 1,
                "ml_lane_role": 5,
                "net_worth": 10000,
                "is_radiant": True,
            },
            {
                "hero_id": 2,
                "lane_role": 1,
                "ml_lane_role": 5,
                "net_worth": 5000,
                "is_radiant": True,
            },
            {
                "hero_id": 3,
                "lane_role": 2,
                "ml_lane_role": 2,
                "net_worth": 15000,
                "is_radiant": True,
            },
            {
                "hero_id": 4,
                "lane_role": 3,
                "ml_lane_role": 4,
                "net_worth": 7800,
                "is_radiant": True,
            },
            {
                "hero_id": 5,
                "lane_role": 3,
                "ml_lane_role": 4,
                "net_worth": 12000,
                "is_radiant": True,
            },
            {
                "hero_id": 6,
                "lane_role": 1,
                "ml_lane_role": 1,
                "net_worth": 11200,
                "is_radiant": False,
            },
            {
                "hero_id": 7,
                "lane_role": 1,
                "ml_lane_role": 5,
                "net_worth": 6150,
                "is_radiant": False,
            },
            {
                "hero_id": 8,
                "lane_role": 2,
                "ml_lane_role": 4,
                "net_worth": 17500,
                "is_radiant": False,
            },
            {
                "hero_id": 9,
                "lane_role": 3,
                "ml_lane_role": 4,
                "net_worth": 6300,
                "is_radiant": False,
            },
            {
                "hero_id": 10,
                "lane_role": 3,
                "ml_lane_role": 3,
                "net_worth": 14200,
                "is_radiant": False,
            },
        ]
        checked_players = checkRanks(players)
        assert checked_players == self.all_expected_players

    def test_fixExcess4(self):
        players = [
            {"hero_id": 1, "lane_role": 1, "ml_lane_role": 1, "net_worth": 10000},
            {"hero_id": 2, "lane_role": 1, "ml_lane_role": 5, "net_worth": 5000},
            {"hero_id": 3, "lane_role": 2, "ml_lane_role": 2, "net_worth": 15000},
            {"hero_id": 4, "lane_role": 3, "ml_lane_role": 4, "net_worth": 7800},
            {"hero_id": 5, "lane_role": 3, "ml_lane_role": 4, "net_worth": 12000},
        ]

        checked_players = fixExcess([4], [3], players)
        assert checked_players == self.expected_players

    def test_fixExcess5(self):
        players = [
            {"hero_id": 1, "lane_role": 1, "ml_lane_role": 5, "net_worth": 10000},
            {"hero_id": 2, "lane_role": 1, "ml_lane_role": 5, "net_worth": 5000},
            {"hero_id": 3, "lane_role": 2, "ml_lane_role": 2, "net_worth": 15000},
            {"hero_id": 4, "lane_role": 3, "ml_lane_role": 4, "net_worth": 7800},
            {"hero_id": 5, "lane_role": 3, "ml_lane_role": 3, "net_worth": 12000},
        ]

        checked_players = fixExcess([5], [1], players)
        assert checked_players == self.expected_players

    def test_fixExcess3(self):
        players = [
            {"hero_id": 1, "lane_role": 1, "ml_lane_role": 1, "net_worth": 10000},
            {"hero_id": 2, "lane_role": 1, "ml_lane_role": 5, "net_worth": 5000},
            {"hero_id": 3, "lane_role": 2, "ml_lane_role": 2, "net_worth": 15000},
            {"hero_id": 4, "lane_role": 3, "ml_lane_role": 3, "net_worth": 7800},
            {"hero_id": 5, "lane_role": 3, "ml_lane_role": 3, "net_worth": 12000},
        ]

        checked_players = fixExcess([3], [4], players)
        assert checked_players == self.expected_players

    def test_fixExcess4and5(self):
        players = [
            {"hero_id": 1, "lane_role": 1, "ml_lane_role": 5, "net_worth": 10000},
            {"hero_id": 2, "lane_role": 1, "ml_lane_role": 5, "net_worth": 5000},
            {"hero_id": 3, "lane_role": 2, "ml_lane_role": 2, "net_worth": 15000},
            {"hero_id": 4, "lane_role": 3, "ml_lane_role": 4, "net_worth": 7800},
            {"hero_id": 5, "lane_role": 3, "ml_lane_role": 4, "net_worth": 12000},
        ]

        checked_players = fixExcess([4, 5], [3, 1], players)
        assert checked_players == self.expected_players

    def test_findHighestAndLowest(self):
        players = [
            {"hero_id": 1, "lane_role": 1, "ml_lane_role": 1, "net_worth": 10000},
            {"hero_id": 2, "lane_role": 1, "ml_lane_role": 5, "net_worth": 5000},
        ]
        highest, lowest = findHighestAndLowest(players)
        assert highest == players[0]
        assert lowest == players[1]


class TestFindRole:
    def test_findRole1(self):
        player = {"last_hits": 500, "gpm": 700, "obs_placed": 1, "lane_role": 1}
        role = findRole(player, "immortal")
        assert role == 1

    def test_findRole2(self):
        player = {"last_hits": 500, "gpm": 700, "obs_placed": 1, "lane_role": 2}
        role = findRole(player, "immortal")
        assert role == 2

    def test_findRole3(self):
        player = {"last_hits": 500, "gpm": 700, "obs_placed": 1, "lane_role": 3}
        role = findRole(player, "immortal")
        assert role == 3

    def test_findRole4(self):
        player = {"last_hits": 200, "gpm": 500, "obs_placed": 10, "lane_role": 3}
        role = findRole(player, "immortal")
        assert role == 4

    def test_findRole5(self):
        player = {"last_hits": 200, "gpm": 500, "obs_placed": 10, "lane_role": 1}
        role = findRole(player, "immortal")
        assert role == 5


def setupPlayerTestingObject(ml_lane):
    player = {
        "personaname": "playername",
        "hero_id": 15,
        "gold_t": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "xp_t": [0, 10],
        "lh_t": [0, 2],
        "is_radiant": True,
        "ml_lane_role": ml_lane,
        "item_0": 5,
        "item_1": 12,
        "item_2": 19,
        "item_3": 34,
        "item_4": 37,
        "item_5": 23,
        "item_neutral": 96,
        "backpack_0": 7,
        "backpack_1": 9,
        "backpack_2": 41,
        "level": 16,
        "net_worth": 12000,
        "gpm": 500,
        "xpm": 550,
        "last_hits": 100,
        "kills": 8,
        "assists": 10,
        "deaths": 4,
        "hero_damage": 10000,
        "tower_damage": 1000,
        "damage_taken": 500,
        "permanent_buffs": 5,
        "rank_tier": 81,
        "life_state_dead": 100,
        "buyback_log": [],
        "kills_log": [{"time": 1}, {"time": 3}],
        "multi_kills": 4,
        "kill_streaks": 2,
        "camps_stacked": 1,
        "stuns": 5,
        "max_hero_hit": 320,
        "runes_log": 0,
        "is_roaming": True,
        "obs_placed": 5,
        "sen_placed": 2,
        "hero_healing": 566,
        "duration": 1000,
    }
    return player
