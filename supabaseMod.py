from config import Config
from supabase import create_client, Client
from datetime import datetime as date


class SupabaseMod:
    def __init__(self):
        self.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.signInIntoSupabase(Config.USER_EMAIL, Config.USER_PASSWORD)
        self.tableTicket = "ticket"
        self.tableInvoice = "invoice"
        self.keyValue = "user_string"
        self.dateStart = "start_at"
        self.dateEnd = "valid_until"

    def signInIntoSupabase(self, email, password):
        result = self.supabase.auth.sign_in_with_password({"email": email, "password":password})


    def checkCodeInDatabase(self, code):
        result = self.supabase.table(self.tableTicket).select("*, user_subscription(*, invoice(*), subscriptions(*))").eq(self.keyValue, code).execute()
        print(result)
        count = result.data[0]["count"]
        user = result.data[0]["user_subscription"]["client_id"]
        startDate = result.data[0]["user_subscription"]["start_date"]
        endDate = result.data[0]["user_subscription"]["end_date"]
        status = result.data[0]["user_subscription"]["invoice"][0]["status"]
        restrictionStart = result.data[0]["user_subscription"]["subscriptions"]["restriction_start"]
        restrictionEnd = result.data[0]["user_subscription"]["subscriptions"]["restriction_end"]

        print(count, user, startDate, endDate, status, restrictionStart, restrictionEnd)
        print(user)
        return self.isResultValid(result.data[0]) if result.data else False
    
    def isResultValid(self, result):
        #validUntil = date.fromisoformat(result[self.dateEnd].replace('Z', '+00:00'))
        #startAt = date.fromisoformat(result[self.dateStart].replace('Z', '+00:00'))
        #now = date.now()
        
        return True #validUntil > now and startAt < now
    
    
