from GetUserCodes import *
from MappingLoader import *


class User():
    def __init__(self, name : str,  city : str, gender: str, age : int, smoker : str,
                gender_search: str, age_search : list, smoker_search : str, age_bucket :list):
        self.name = name
        self.city = city
        self.gender = gender
        self.age = age
        self.smoker = smoker
        self.gender_search = gender_search
        self.age_search = age_search
        self.smoker_search = smoker_search
        self.age_bucket = age_bucket

        # Will be updated in update_user_search_codes method
        self.personal_code = 0
        self.preference_code = 0

    def update_user_search_codes(self):
        personal_code = MappingLoader.LoadPersonalDataMapping()
        preference_code = MappingLoader.LoadPreferenceMapping()
        self.personal_code = GetUserCodes.GetPersonalCode(personal_code,
                                                 self.gender,
                                                 self.age_bucket[0],
                                                 self.age_bucket[1],
                                                 self.smoker)
        self.preference_code = GetUserCodes.GetPreferenceCode(preference_code,
                                                 self.gender_search,
                                                 self.age_search[0],
                                                 self.age_search[1],
                                                 self.smoker_search)
        
    def show_user_info(self):
        print()
        print("*********************************************************************************************************")
        print("User Name : ", self.name)
        print("User's City : ", self.city)
        print("User's Gender : ", self.gender)
        print("User's Age : ", self.age)
        print("User's Age Bucket : ", self.age_bucket)
        print("User Smokes? : ", self.smoker)
        print("User's Gender Seach : ", self.gender_search)
        print("User's Age Seach : ", self.age_search)
        print("User's Smoke Search : ", self.smoker_search)
        print("User's Personal code : ", self.personal_code)
        print("User's Preference code : ", self.preference_code)
        print("*********************************************************************************************************")
        print()

