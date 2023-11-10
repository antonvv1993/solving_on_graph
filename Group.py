class Group():

    def __init__(self, left_subgroup : list, right_subgroup : list, group_name : str):
        
        self.left_subgroup = left_subgroup
        self.right_subgroup = right_subgroup
        self.group_name = group_name

    
    def ShowGroupInfo(self):
        print("*" * 40)
        print(self.group_name, "                               *")
        print("Left Subgroup ", self.left_subgroup, "                      *")
        print("Right Subgroup ", self.right_subgroup, "                    *")
        print("*" * 40)

    def GetUsersFromGroups(groups) -> list:
        users_list = []
        user_string_list = []
        for group in groups:
            users_list.append(group.left_subgroup)
            users_list.append(group.right_subgroup)
            user_string_list.append("User " + str(group.left_subgroup))
            user_string_list.append("User " + str(group.right_subgroup))
        return [users_list,user_string_list]
    
    def AddUserToLeftSubgroup(self, user_id):
        self.left_subgroup.append(user_id)

    def AddUserToRightSubgroup(self, user_id):
        self.right_subgroup.append(user_id)

    
    
