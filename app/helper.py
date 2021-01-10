from datetime import datetime, timedelta

def getTimestamp():
    return datetime.utcnow()

def getDeltaTimeDecimal(start, end):
    return (end-start).total_seconds()/3600