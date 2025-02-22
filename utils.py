from datetime import datetime

def getTodaysDate():
    DTnow = datetime.now() 
    DTformatted = DTnow.strftime("%Y-%m-%d")
    return DTformatted