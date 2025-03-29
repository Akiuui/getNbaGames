from static.IdsByCode import teamIdByCode

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
        item["visitorId"] = teamIdByCode[item["teams"]["visitors"]["code"]]
        
        item["dateStart"] = item["date"]["start"].split('T')[0]
        item["timeStart"] = item["date"]["start"].split('T')[1]
           
        item.pop("id", None)
        item.pop("teams", None)
        item.pop("start", None)
        item.pop("date", None)
        
        formatted = deletePropsFromStruct(item, propsToDelete)
  
        games.append(formatted)

    return games

def deletePropsFromStruct(data, delete):
    for item in delete:
        if item in data:
            del data[item]

    return data
