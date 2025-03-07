from config import Config
from supabase import create_client
from datetime import datetime as date


class SupabaseMod:
    def __init__(self):
        self.client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.table = "ticket"
        self.column = "user_string"
        self.dateStart = "start_at"
        self.dateEnd = "valid_until"

    def checkCodeInDatabase(self, code):
        result = self.client.from_(self.table).select("*").eq(self.column, code).execute()
        return self.isResultValid(result.data[0]) if result.data else False
    
    def isResultValid(self, result):
        validUntil = date.fromisoformat(result[self.dateEnd].replace('Z', '+00:00'))
        startAt = date.fromisoformat(result[self.dateStart].replace('Z', '+00:00'))
        now = date.now()
        
        return validUntil > now and startAt < now
    
    
