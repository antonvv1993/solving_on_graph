from RandomUserGenerator import RandomUserDetailsGenerator as rug
from User import User

class UserGeneration():
    
    def CreateUser() -> User:
        Name = rug.NameCreation()
        City = rug.CityCreation()
        Gender = rug.GenderCreation()
        Age = rug.AgeCreation()
        Smoker = rug.SmokeCreation()
        UserGenderSearch = rug.UserGenderSearch(Gender)
        UserAgeSearch = rug.UserAgeSearch(Age)
        UserSmokerSearch = rug.UserSmokerSearch()
        AgeBucket = rug.GetAgeBucketByAge(Age)
        user = User(Name,City,Gender,Age,Smoker,UserGenderSearch,UserAgeSearch,UserSmokerSearch,
                    AgeBucket)
        
        user.update_user_search_codes()
        
        return user