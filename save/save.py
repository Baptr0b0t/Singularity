import json

def next_level(curr_level):
    with open("save.json","r") as save:
        data = json.load(save)

    if data["level"][str(curr_level)]["best_score"] > 50:
        data["current_level"]+=1

        with open("save.json","w") as save:
            json.dump(data,save)

def new_best_score(new_score):
    with open("save.json","r") as save:
        data = json.load(save)
        current_level = data["current_level"]
        data["level"][str(current_level)]["best_score"] = new_score

    with open("save.json","w") as save:
        json.dump(data,save)
