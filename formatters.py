import logging
from staticIdsByCode import teamIdByCode

def deletePropsFromStruct(data, delete):
    for item in delete:
        if item in data:
            del data[item]

    return data

def drillForProp(data, parent, child):
    if parent in data:
        childVal = data[parent].pop(child, None)
        data.pop(parent, None)
    
    if childVal:
        data[child] = childVal

    return data

propsToDelete = [  
                "league",
                "season",
                "stage",
                "status",
                "periods",
                "arena",
                "officials",
                "timesTied",
                "leadChanges",
                "nugget"
                ]

def formatGames(response):
    games = []
    
    for item in response:
        item["_id"] = item["id"]
        item["homeId"] = teamIdByCode[item["teams"]["home"]["code"]]
        item["visitorId"] = teamIdByCode[item["teams"]["home"]["code"]]
        item.pop("id", None)
        item.pop("teams", None)


        formatted = deletePropsFromStruct(item, propsToDelete)
        formatted = drillForProp(formatted, "date", "start")
  
        # ZAMENI VISITORTEAM I HOMETEAM SA FUNCIJOM GET TEAMID
        games.append(formatted)

    return games

