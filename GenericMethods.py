import pandas as pd
from User import *
from UserGeneration import UserGeneration as ug
from MappingLoader import *
from UserMatcher import *
from GraphManipulation import *
import  xlsxwriter

class GenericMethods():
    def GetUserReference(mapping_table: pd.DataFrame, user: str) -> User:
        return mapping_table[mapping_table["User_id"] == user]["User"].iloc[0]
    
    def GetGraphsStructure(amount_of_users: int) -> list:
        users_dict = GraphManipulation.GenerateDictionatyWithUsers(amount_of_users)
        return [GraphManipulation.ReduceDimention(users_dict),users_dict]
    
    def WriteMappingsToexcelAndReturnDfFromDict(reduces_dimention_outcome : list, filename : str) -> pd.DataFrame:
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            reduces_dimention_outcome[0].to_excel(writer, sheet_name='Sheet1')  # Default position, cell A1.
            reduces_dimention_outcome[1].to_excel(writer, sheet_name='Sheet2')
            keys = reduces_dimention_outcome[2].keys()
            values = reduces_dimention_outcome[2].values()
            reduces_dimention_outcome_2 = pd.DataFrame({"User_id": keys, "User": values})
            reduces_dimention_outcome_2.to_excel(writer, sheet_name='Sheet3')
            reduces_dimention_outcome[3].to_excel(writer, sheet_name='Sheet4')
            writer.save()
            return reduces_dimention_outcome_2
