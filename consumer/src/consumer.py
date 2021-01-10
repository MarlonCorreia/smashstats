from db import DataBase
from smash_api import API
import json
import time

def update_match(db, winner_char, loser_char):
    new_value_win = db.select_match_up_by_char_name(winner_char)
    new_value_lose = db.select_match_up_by_char_name(loser_char)


    for idx, val in enumerate(new_value_win["match_up"]):
        if val["character"] == loser_char:
            new_value_win["match_up"][idx]["wins"] += 1

    for idx, val in enumerate(new_value_lose["match_up"]):
        if val["character"] == winner_char:
            new_value_lose["match_up"][idx]["losses"] += 1

    db.update_match_up({"char": winner_char}, {"$set": new_value_win})
    db.update_match_up({"char": loser_char}, {"$set": new_value_lose})




def info_by_set(set_id, api, db):
    try:
        print("i'm on info by set")
        res = json.loads(api.query_set_by_id(set_id))

        if res["data"]["set"]["displayScore"] == "DQ":
            return

        for games in res["data"]["set"]["games"]:
            winnerId = games["winnerId"]

            player_one = {
                "char": db.select_char_by_id(games["selections"][0]["selectionValue"])["name"],
                "id":  games["selections"][0]["entrant"]["id"]
            }
                
            player_two = {
                "char": db.select_char_by_id(games["selections"][1]["selectionValue"])["name"],
                "id":  games["selections"][1]["entrant"]["id"]
            }

            if player_one["id"] == winnerId:
                print("{} has won over {}".format(player_one["char"], player_two["char"]))
                
                #update_match(db, player_one["char"], player_two["char"])
            else:
                print("{} has won over {}".format(player_one["char"], player_two["char"]))

                # update_match(db, player_two["char"], player_one["char"])        
    except:
        pass

def sets_in_event(api, event_id):
    page = 1

    while True:
        res = api.query_sets_in_event(event_id, page)
        json_res = json.loads(res)

        if json_res["data"]["event"]["sets"]["nodes"] == None:
            break
        else:
            for i in json_res["data"]["event"]["sets"]["nodes"]:
                print(i["id"])
                yield i["id"]
        
        page += 1

if __name__ == "__main__":
    api = API()
    db = DataBase()

    for game_set in sets_in_event(api, 463634):
        info_by_set(game_set, api, db)


