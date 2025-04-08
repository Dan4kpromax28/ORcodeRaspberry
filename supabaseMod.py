from config import Config
from supabase import create_client, Client
from datetime import datetime as date
from datetime import time


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
        count = int(result.data[0]["count"])
        user = result.data[0]["user_subscription"]["client_id"]
        #startDate = date.strptime(result.data[0]["user_subscription"]["start_date"],"%Y-%m-%d").date()
        #endDate = date.strptime(result.data[0]["user_subscription"]["end_date"],"Y-%m-%d").date()
        status = result.data[0]["user_subscription"]["invoice"][0]["status"]
        restrictionStart = date.strptime(result.data[0]["user_subscription"]["subscriptions"]["restriction_start"],"%H:%M:%S").time()
        restrictionEnd = date.strptime(result.data[0]["user_subscription"]["subscriptions"]["restriction_end"], "%H:%M:%S").time()
        isDate = result.data[0]["user_subscription"]["subscriptions"]["is_date"]
        isTime = result.data[0]["user_subscription"]["subscriptions"]["is_time"]
        if status != "valid":
            print("Status nav derigs")
            return False
        
        if isDate == True and isTime == True:
            startDate = date.strptime(result.data[0]["user_subscription"]["start_date"],"%Y-%m-%d").date()
            if self.isDateValid(startDate) != True:
                print("Datums nav derigs")
                return False
            if self.isTimeValid(restrictionStart, restrictionEnd) != True:
                print("Laiks nav derigs")
                return False
        
        if isTime == False and isDate == True:
            startDate = date.strptime(result.data[0]["user_subscription"]["start_date"],"%Y-%m-%d").date()
            endDate = date.strptime(result.data[0]["user_subscription"]["end_date"],"%Y-%m-%d").date()
            if self.isDateValid(startDate, endDate) != True:
                print("Datums nav derigs")
                return False
            
        if isTime == False and isDate == False:
            if count <= 0:
                print("Datums nav derigs")
                return False
            new_count = count - 1
            result = self.supabase.table(self.tableTicket).update({"count": new_count}).eq("user_string", code).execute()
            
        self.sendCheckMark(user)

        
        print(user)
        return True
    
    def isTimeValid(self, restrictionStart, restrictionEnds):
        #validUntil = date.fromisoformat(result[self.dateEnd].replace('Z', '+00:00'))
        #startAt = date.fromisoformat(result[self.dateStart].replace('Z', '+00:00'))
        #now = date.now()
        now = date.now().time()

        return restrictionStart <= now <= restrictionEnds
    
    def isDateValid2(self, restrictionStart):
        now = date.today().date()
        print("restType", type(restrictionStart))
        print("now" ,type(date.today()))
        return restrictionStart <= now
    
    def isDateValid(self, startAt, validUntil):
        print("startAt" , type(startAt))
        print("validUntil", type(validUntil))
        print("now" , type(date.today()))
        now = date.today().date()
        return startAt <= now <= validUntil
    
    def sendCheckMark(self, id):
        result = self.supabase.table("time_stamps").insert({"client_id": id}).execute()
        print(result)
    
    
