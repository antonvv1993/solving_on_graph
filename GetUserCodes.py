import pandas as pd

class GetUserCodes():

    def GetPersonalCode(df : pd.DataFrame, gender : str, left_age : int,
                        right_age :int, smoker : str) -> int:

        personal_data = df[(df["Gender"] == gender) & (df["Smoker"] == smoker) & 
                     (df["Left_Age"] == left_age) & (df["Right_Age"] == right_age)]
        return personal_data.iloc[0]["Code"]
    

    def GetPreferenceCode(df : pd.DataFrame, gender : str, left_age : int,
                        right_age :int, smoker : str) -> int:

        preference_data = df[(df["Gender"] == gender) & (df["Smoker"] == smoker) & 
                     (df["Left_Age"] == left_age) & (df["Right_Age"] == right_age)]

        return preference_data.iloc[0]["Preference_Code"]