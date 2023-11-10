
import pandas as pd

class UserMatcher():

    def HardFilterUserCheck(personal_preference_mapping, user1, user2) -> bool:

        filtered_personal_preference_mapping = personal_preference_mapping[(personal_preference_mapping["Preference_Code"] == user1.preference_code)]
        list_of_personal_codes = filtered_personal_preference_mapping.iloc[0]["Personal_Data_Code"]
        try:
            list_of_personal_codes_str = list_of_personal_codes.split(";")
            list_of_personal_codes_int = list(map(int, list_of_personal_codes_str))
            return user2.personal_code in list_of_personal_codes_int
        except:
            return user2.personal_code == list_of_personal_codes

        
        
    
        
    