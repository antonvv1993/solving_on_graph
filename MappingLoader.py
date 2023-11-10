import pandas as pd


class MappingLoader():
    
    def LoadPersonalDataMapping(filename = '/Users/antonvolkov/Desktop/MatchUp/MatchUpAlgo/Personal_Data_Mapping.xlsx') -> pd.DataFrame:
        return pd.read_excel(filename,index_col=0)
    
    def LoadPreferenceMapping(filename = '/Users/antonvolkov/Desktop/MatchUp/MatchUpAlgo/Preference_Mapping.xlsx') -> pd.DataFrame:
        return pd.read_excel(filename,index_col=0)  
    
    def LoadPersonalPreferenceMapping(filename = '/Users/antonvolkov/Desktop/MatchUp/MatchUpAlgo/Preference_Personal_Mapping.xlsx') -> pd.DataFrame:
        return pd.read_excel(filename,index_col=0)

if __name__ == "__main__":
    personal_data = MappingLoader.LoadPersonalDataMapping()
    print(personal_data)
       