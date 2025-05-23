from config import Config
from supabase import create_client, Client
from datetime import datetime as date
from datetime import time
from oledDi import OledDisplay


class SupabaseMod:

    def signInIntoSupabase(self, email, password):
        result = self.supabase.auth.sign_in_with_password({"email": email, "password":password})
        

    def __init__(self):
        self.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.signInIntoSupabase(Config.USER_EMAIL, Config.USER_PASSWORD)
        self.tableTicket = "ticket"
        self.tableInvoice = "invoice"
        self.keyValue = "user_string"
        self.dateStart = "start_at"
        self.dateEnd = "valid_until"
        self.display = OledDisplay()

    


    def checkCodeInDatabase(self, code):
        try:
            
            
            
            result = self.supabase.table(self.tableTicket).select("id, user_string, user_subscription(client_id, start_date, end_date, invoice(status), subscriptions(restriction_start, restriction_end, is_date, is_time))").eq(self.keyValue, code).execute()
            print(result)
            if result.data == []:
                print("Nav derigs kods")
                self.display.showMessage("Nav derigs kods")
                return False
            
            ticketId = result.data[0]["id"]
            user = result.data[0]["user_subscription"]["client_id"]
            print(ticketId)
            print(user)
            
            status = result.data[0]["user_subscription"]["invoice"][0]["status"]
            
            restrictionStart = date.strptime(result.data[0]["user_subscription"]["subscriptions"]["restriction_start"],"%H:%M:%S").time()
            print(restrictionStart)
            restrictionEnd = date.strptime(result.data[0]["user_subscription"]["subscriptions"]["restriction_end"], "%H:%M:%S").time()
            print(restrictionEnd)
            isDate = result.data[0]["user_subscription"]["subscriptions"]["is_date"]
            print(isDate)
            isTime = result.data[0]["user_subscription"]["subscriptions"]["is_time"]
            print(isTime)
            print(status)
           
            if status != "valid":
                print("Status nav derigs")
                self.display.showMessage("Status nav derigs")
                return False
            print("derigs")
            if isDate == True and isTime == True:
                startDate = date.strptime(result.data[0]["user_subscription"]["start_date"],"%Y-%m-%d").date()
                if self.isDateValid2(startDate) != True:
                    print("Datums nav derigs")
                    self.display.showMessage("Datums nav derigs")
                    return False
                if self.isTimeValid(restrictionStart, restrictionEnd) != True:
                    print("Laiks nav derigs")
                    self.display.showMessage("Laiks nav derigs")
                    return False
            print('ok')
            if isTime == False and isDate == True:
                startDate = date.strptime(result.data[0]["user_subscription"]["start_date"],"%Y-%m-%d").date()
                endDate = date.strptime(result.data[0]["user_subscription"]["end_date"],"%Y-%m-%d").date()
                if self.isDateValid(startDate, endDate) != True:
                    print("Datums nav derigs")
                    self.display.showMessage("Datums nav derigs")
                    return False
            print('good')
                
            self.sendCheckMark(ticketId)

            return True
        except Exception as e:
            print("Notika problema")
            return False
    
    def isTimeValid(self, restrictionStart, restrictionEnds):
        try:
            now = date.now().time()
            return restrictionStart <= now <= restrictionEnds
        except Exception as e:
            return False
    
    def isDateValid2(self, restrictionStart):
        try:
            now = date.today().date()
            return restrictionStart <= now
        except Exception as e:
            return False
    
    def isDateValid(self, startAt, validUntil):
        try:
            now = date.today().date()
            return startAt <= now <= validUntil
        except Exception as e:
            return False
    
    def sendCheckMark(self, id):
        result = self.supabase.table("time_stamps").insert({"ticket_id": id}).execute()

    
    
