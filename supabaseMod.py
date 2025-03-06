from config import Config
from supabase import create_client
from datetime import datetime as date


class SupabaseMod:
    def __init__(self):
        self.client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.table = "ticket"
        self.column = "user_string"
        self.date_start = "start_at"
        self.date_end = "valid_until"

    def checkCodeInDatabase(self, code):
        result = self.client.from_(self.table).select("*").eq(self.column, code).execute()
        return self.isResultValid(result.data[0]) if result.data else False
    
    def isResultValid(self, result):
        valid_until = date.fromisoformat(result[self.date_end].replace('Z', '+00:00'))
        start_at = date.fromisoformat(result[self.date_start].replace('Z', '+00:00'))
        now = date.now()
        
        return valid_until > now and start_at < now
    
    
