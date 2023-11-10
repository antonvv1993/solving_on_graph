from UserGeneration import UserGeneration as ug
from UserMatcher import * 
from collections import Counter
import networkx as nx
import matplotlib
import matplotlib.pyplot
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
from Group import *
import logging
import itertools

class GraphManipulation():
    

    def GenerateDictionatyWithUsers(amount_of_users) -> dict:
        dicts = {}
        keys = ["User " + str(user) for user in range(1,amount_of_users+1)]
        for i in keys:
            dicts[i] = ug.CreateUser()
        return  dicts
    
    def GenerateFullDirectedGraph(mapping_table : pd.DataFrame, users_dict: dict) -> nx.DiGraph:
        users_number = len(users_dict)
        tuples = []
        for i in range(1,users_number+1):
            for j in range(1,users_number+1):
                if i != j:
                    user_i = "User " + str(i)
                    user_j = "User " + str(j)
                    if UserMatcher.HardFilterUserCheck(mapping_table,users_dict[user_i], users_dict[user_j]):
                        tuples.append((i,j))


        G = nx.DiGraph()  # создаём объект графа
        nodes = list(range(1,users_number + 1))
        edges = tuples
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G
    
    def GenerateFullUnDirectedGraph(mapping_table : pd.DataFrame, users_dict: dict) -> nx.Graph:
        users_number = len(users_dict)
        tuples = []
        for i in range(1,users_number+1):
            for j in range(1,users_number+1):
                if i != j:
                    user_i = "User " + str(i)
                    user_j = "User " + str(j)
                    if UserMatcher.HardFilterUserCheck(mapping_table,users_dict[user_i], users_dict[user_j]) and UserMatcher.HardFilterUserCheck(mapping_table,users_dict[user_j], users_dict[user_i]) and tuple(reversed((i,j))) not in tuples:
                        tuples.append((i,j))


        G = nx.Graph()  # создаём объект графа
        nodes = list(range(1,users_number + 1))
        edges = tuples
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        #print(tuples)
        return G
    
    def PlotGraph(G,filename:  str):    
        fig = matplotlib.pyplot.figure()
        nx.draw_networkx(G, ax=fig.add_subplot())
        fig.savefig(filename)

    def Plot3Graphs(G,G1,G2,filename:  str):  
        gs = gridspec.GridSpec(2, 2)
        pl.figure(figsize=(40, 25), dpi=120)
        ax = pl.subplot(gs[0, 0]) # row 0, col 0
        nx.draw_networkx(G)

        ax = pl.subplot(gs[0, 1]) # row 0, col 0
        nx.draw_networkx(G1)

        ax = pl.subplot(gs[1, :]) # row 1, span all columns
        nx.draw_networkx(G2)
        pl.savefig(filename)

    def ReduceDimention(users_dict) -> list:
        
        data_frame_with_all_users = pd.DataFrame(columns=['User_id','user_code','user_preference_cide', 'Final_Code'])
        reduced_df_with_users = []

        new_dict = {}
        listt = []
        for i in range(1,len(users_dict) + 1):
            user = "User " + str(i)

            value = str(users_dict[user].personal_code) + str(users_dict[user].preference_code)
            new_dict[user] = value
            listt.append(value)
            data_frame_with_all_users.loc[i] = [user, str(users_dict[user].personal_code),str(users_dict[user].preference_code),value]

        reduced_dict = Counter(listt)

        reduced_df_with_users = pd.DataFrame(reduced_dict.items(), columns=['Final_Code', 'Amount_of_Users'])
        users = ['User ' + str(x) for x in range(1,len(reduced_dict)+1)]
        reduced_df_with_users['User'] = users
        reduced_df_with_users = reduced_df_with_users[['User', 'Final_Code', 'Amount_of_Users']]

        users_objects = []

        for i in range(0,len(reduced_df_with_users)):
            user_code = reduced_df_with_users.iloc[i]['Final_Code']
            real_user = data_frame_with_all_users[data_frame_with_all_users['Final_Code'] == user_code]['User_id'].iloc[0]
            user_object = users_dict[real_user]
            users_objects.append(user_object)

        reduced_df_with_users['User_Object'] = users_objects
        reduced_dict = dict(zip(reduced_df_with_users['User'], reduced_df_with_users['User_Object']))
        reduced_df_with_users_preference_split = pd.DataFrame(columns=['User','User_Code','User_Preference_Code', 'Amount_of_Users','User_Object'])
        reduced_df_with_users_preference_split["User"] = reduced_df_with_users["User"]
        reduced_df_with_users_preference_split["User_Code"] = reduced_df_with_users['Final_Code'].str[0]
        reduced_df_with_users_preference_split["User_Preference_Code"] = reduced_df_with_users['Final_Code'].str[1:]
        reduced_df_with_users_preference_split["Amount_of_Users"] = reduced_df_with_users['Amount_of_Users']
        reduced_df_with_users_preference_split["User_Object"] = reduced_df_with_users['User_Object']
        
        return [data_frame_with_all_users,reduced_df_with_users,reduced_dict,reduced_df_with_users_preference_split]

    def ReturnCliques(G) -> list:
        return [c for c in nx.find_cliques(G)]
    def ReturnCliquesPerNode(G) -> dict:
        d = {}
        for i in range(1,len(G.nodes)):
            d[i] = len([c for c in nx.find_cliques(G) if i in c])
        return d
    
    def PreliminaryGroupsCliqueSizeOne(G,total_list_of_cliques) -> list:
        logging.basicConfig(level=logging.DEBUG, filename="log.txt",filemode="w")
        logging.debug("Функция начала работу")
        d = {} # словать где будем хранить количество клик для каждом вершины
        group_number = 1 # номер группы для ее названия
        list_of_groups_output = [] # массив где храним сами группы
        users_list = [] # массив где храним номера юзеров, которые уже состоят в шруппе
        dict_with_groups = {}
        
        """"
        Идея метода первичного разбиение проста:
        1. Берем все клики и для каждой вершины считаем сколько клик есть
        2. Для тех вершин, у которых клика одна и длина которых > 1 (то есть не вершина не изолированная)
        сразу создаем группу из этим вершин. вершины запоминаем
        3. Если по правилу 1 мы обнаруживаем клику с вершиной, которая уже есть в списке,
        по вершину добавляем в соответствующую группу
        """

        for i in range(1,len(G.nodes)+1):
            d[i] = len([c for c in nx.find_cliques(G) if i in c])
        
        #сортирует словать, чтобы обрабатывать хвосты в первую очередь
        d = dict(sorted(d.items(), key=lambda item: item[1]))
        
        # бежим по каждому элементы словаря
        for i in d:
        #for i in range(1,len(G.nodes)):
            #d[i] = len([c for c in nx.find_cliques(G) if i in c]) # словарь вершина - кол-во клик
            logging.debug(f"*********************************")
            logging.debug(f"Находимся в вершине {i} длина клики {d[i]}")
            group_list_0 = [c for c in nx.find_cliques(G) if i in c]
            group_list = []
            for element in group_list_0:
                if len(element) <=2:
                    group_list.append(element)
                else:
                    for sublist in list((list(tup) for tup in itertools.combinations(element,2))):
                        group_list.append(sublist)
            group_list = [x for x in group_list if i in x]
            logging.debug(f"Cписок клик вершины {i} : {group_list}")
            #logging.debug(f"В клике следующие вершины: {group_list[0][0]} {group_list[0][1]}")
            #if len([c for c in nx.find_cliques(G) if i in c][0]) != 1:
            for j in range(0,len([c for c in nx.find_cliques(G) if i in c])):
                logging.debug(f"Находимся в клике {j} вершины {i}. Сама клика : {[c for c in nx.find_cliques(G) if i in c][j]}")
                logging.debug(f"Длина клики: {len([c for c in nx.find_cliques(G) if i in c][j])}")
                if len([c for c in nx.find_cliques(G) if i in c][j]) != 1:
                    logging.debug(f"Попали в перрый if так как длина клики !=1")
                #if d[i] == 1 and len([c for c in nx.find_cliques(G) if i in c][j]) != 1:
                    #group_list = [c for c in nx.find_cliques(G) if i in c]
                    if group_list[0][0] not in users_list and group_list[0][1] not in users_list:
                        logging.debug(f"Попали в ситуацию когда: {group_list[0][0]} {group_list[0][1]} отсутствуют в списке")
                        group = Group([group_list[0][0]],[group_list[0][1]],"Group" + str(group_number))
                        logging.debug(f"Группа: {group_number} была создана. Левая подгруппа {group_list[0][0]}, правая подгруппа {group_list[0][1]}") 
                        #group.ShowGroupInfo()
                        list_of_groups_output.append(group)
                        dict_with_groups[group_number-1] = [group_list[0][0],group_list[0][1]]
                        group_number = group_number +1
                        users_list.append(group_list[0][0])
                        users_list.append(group_list[0][1])
                        logging.debug(f"Теперь в пользовательском списке следующие элементы: {users_list}")
                        
                    elif group_list[0][0] in users_list and group_list[0][1] not in users_list:
                        logging.debug(f"Попали в ситуацию когда: {group_list[0][0]} в списке, а {group_list[0][1]} нет")
                        #needed = group_list[0][1]
                        for key in dict_with_groups:
                            if group_list[0][0] in dict_with_groups[key]:
                                #print(needed, "was found in group ", key)
                                #print("The value to be added to group ", key," is ",group_list[0][1])
                                if group_list[0][0] in list_of_groups_output[key].left_subgroup:
                                    logging.debug(f" {group_list[0][0]} оказался в левой подгруппе группу {key+1}")
                                    #print("The value to be added to group ", key," is ",group_list[0][1], ". Right Subgroup")
                                    array_list = []
                                    for element in list_of_groups_output[key].left_subgroup:
                                        array_list.append([element,group_list[0][1]])
                                        array_list.append([group_list[0][1],element])
                                        logging.debug(f"Список array_list: {array_list}")
                                        tup1 = map(tuple, array_list)
                                        tup2 = map(tuple, total_list_of_cliques) 
                                        if len(list(map(list, set(tup1).intersection(tup2)))) != 0:
                                            logging.debug(f"Пересечения: {list(map(list, set(tup1).intersection(tup2)))}")
                                            logging.debug(f"Добавляем {group_list[0][1]} в правую подгруппу группу {key+1}")
                                            if group_list[0][1] not in list_of_groups_output[key].right_subgroup:
                                                list_of_groups_output[key].right_subgroup.append(group_list[0][1])
                                                users_list.append(group_list[0][1])
                                else:
                                    if group_list[0][0] in list_of_groups_output[key].right_subgroup:
                                        logging.debug(f" {group_list[0][0]} оказался в правой подгруппе группу {key+1}")
                                        #print("The value to be added to group ", key," is ",group_list[0][1], ". Right Subgroup")
                                        array_list = []
                                        for element in list_of_groups_output[key].right_subgroup:
                                            array_list.append([element,group_list[0][1]])
                                            array_list.append([group_list[0][1],element])
                                            logging.debug(f"Список array_list: {array_list}")
                                            tup1 = map(tuple, array_list)
                                            tup2 = map(tuple, total_list_of_cliques) 
                                            if len(list(map(list, set(tup1).intersection(tup2)))) != 0:
                                        #print("The value to be added to group ", key," is ",group_list[0][1], ". Left Subgroup")
                                                logging.debug(f"Длина Пересечения: {len(list(map(list, set(tup1).intersection(tup2))))}")
                                                logging.debug(f"Пересечения: {list(map(list, set(tup1).intersection(tup2)))}")
                                                logging.debug(f"Добавляем {group_list[0][1]} в левую подгруппу группу {key+1}")
                                                if group_list[0][1] not in list_of_groups_output[key].left_subgroup:
                                                    list_of_groups_output[key].left_subgroup.append(group_list[0][1])
                                                    users_list.append(group_list[0][1])
                                #list_of_groups_output[key]
                                #break
                        
                    elif group_list[0][0] not in users_list and group_list[0][1] in users_list:
                        logging.debug(f"Попали в ситуацию когда: {group_list[0][1]} в списке, а {group_list[0][0]} нет")
                        #needed = group_list[0][0]
                        for key in dict_with_groups:
                            if group_list[0][1] in dict_with_groups[key]:
                                #print(needed, "was found in group ", key)
                                #print("The value to be added to group ", key," is ",group_list[0][0])
                                if group_list[0][1] in list_of_groups_output[key].left_subgroup:
                                    logging.debug(f" {group_list[0][1]} оказался в левой подгруппе группу {key+1}")
                                    #print("The value to be added to group ", key," is ",group_list[0][0], ". Right Subgroup")
                                    array_list = []
                                    for element in list_of_groups_output[key].left_subgroup:
                                        array_list.append([element,group_list[0][0]])
                                        array_list.append([group_list[0][0],element])
                                        logging.debug(f"Список array_list: {array_list}")
                                        tup1 = map(tuple, array_list)
                                        tup2 = map(tuple, total_list_of_cliques)
                                        if len(list(map(list, set(tup1).intersection(tup2)))) != 0:
                                            logging.debug(f"Длина Пересечения: {len(list(map(list, set(tup1).intersection(tup2))))}")
                                            logging.debug(f"Пересечения: {list(map(list, set(tup1).intersection(tup2)))}")
                                            logging.debug(f"Добавляем {group_list[0][0]} в правую подгруппу группу {key+1}")
                                            if group_list[0][0] not in list_of_groups_output[key].right_subgroup:
                                                list_of_groups_output[key].right_subgroup.append(group_list[0][0])
                                                users_list.append(group_list[0][0])
                                else:
                                    #print("The value to be added to group ", key," is ",group_list[0][0], ". Left Subgroup")
                                        array_list = []
                                        for element in list_of_groups_output[key].right_subgroup:
                                            array_list.append([element,group_list[0][0]])
                                            array_list.append([group_list[0][0],element])
                                            logging.debug(f"Список array_list: {array_list}")
                                            tup1 = map(tuple, array_list)
                                            tup2 = map(tuple, total_list_of_cliques)
                                            if len(list(map(list, set(tup1).intersection(tup2)))) != 0:
                                        #print("The value to be added to group ", key," is ",group_list[0][1], ". Left Subgroup")
                                                logging.debug(f"Длина Пересечения: {len(list(map(list, set(tup1).intersection(tup2))))}")
                                                logging.debug(f"Пересечения: {list(map(list, set(tup1).intersection(tup2)))}")
                                                logging.debug(f"Добавляем {group_list[0][0]} в левую подгруппу группу {key+1}")
                                                if group_list[0][0] not in list_of_groups_output[key].left_subgroup:
                                                    list_of_groups_output[key].left_subgroup.append(group_list[0][0])
                                                    users_list.append(group_list[0][0])
                                #list_of_groups_output[key]
                                #break
                logging.debug(f"*********************************")  



       
        #print(dict_with_groups)
        for group in list_of_groups_output:
            group.ShowGroupInfo()
        return list_of_groups_output

    def OptimizeGroups(group_list: list, G, dict_for_grahp) -> list:
        print()
        print()
        print("Total Number of reduced Users: ", len(dict_for_grahp))
        total_user_covered = 0
        total_number_of_isolated_users = 0
        list_of_isolated_users = []
        list_users_in_groups = []
        all_users_set = set(range(1,len(dict_for_grahp)+1))
        for group in group_list:
            total_user_covered =  total_user_covered + len(group.left_subgroup) + len(group.right_subgroup)
            for user_left in group.left_subgroup:
                list_users_in_groups.append(user_left)
            for user_right in group.right_subgroup: 
                list_users_in_groups.append(user_right)
        print(f"Количество пользователей в группах : {total_user_covered}")
        print(f"Пользователи попавшие в группы {list_users_in_groups}")
        users_in_groups_set = set(list_users_in_groups)
        for i in range(1,len(G.nodes)+1):
            if len([c for c in nx.find_cliques(G) if i in c]) == 1 and len([c for c in nx.find_cliques(G) if i in c][0]) == 1:
                total_number_of_isolated_users = total_number_of_isolated_users + 1
                list_of_isolated_users.append([c for c in nx.find_cliques(G) if i in c][0][0])
        isolated_users_set = set(list_of_isolated_users)
        union_isolated_and_in_groups = isolated_users_set.union(users_in_groups_set)
        print(f"Количество изолированных пользователей : {total_number_of_isolated_users}")
        print(f"Изолированные пользователи {list_of_isolated_users}")
        print(f"Количество связанных пользователей не попавших в группы : {len(dict_for_grahp) - total_number_of_isolated_users - total_user_covered }")
        if len(dict_for_grahp) - total_number_of_isolated_users - total_user_covered  != 0:
            union_users_not_in_groups = list(all_users_set ^ union_isolated_and_in_groups)
            print(f"Связанные пользователи не попавшие в группы:  {union_users_not_in_groups}")
            print()
            for user in union_users_not_in_groups:
                cliques = [c for c in nx.find_cliques(G) if user in c]
                print(f"Не попавший в группы пользователь {user} попадает в следующие клики: {cliques}")
                list_of_connected_users_for_opt = [j for sub in cliques for j in sub]
                list_of_connected_users_for_opt = [x for x in list_of_connected_users_for_opt if x != user]
                print(f"Потенциальные пользователи для оптимизации {list_of_connected_users_for_opt}")
                amount_of_initial_groups = len(group_list) + 1
                for potencial_user_for_opt in list_of_connected_users_for_opt:
                    print()
                    if len(list_of_connected_users_for_opt) == 2:
                        g1 = GraphManipulation.InWhichGroupUserIs(list_of_connected_users_for_opt[0],group_list)
                        g2 = GraphManipulation.InWhichGroupUserIs(list_of_connected_users_for_opt[1],group_list)
                        if g1[1].group_name == g2[1].group_name:
                            g1[1].left_subgroup.append(user)
                            for group in group_list:
                                group.ShowGroupInfo()
                            return group_list
                    #print("Потенциальные пользователь для оптимизации {potencial_user_for_opt}")
                    group_of_opt = GraphManipulation.InWhichGroupUserIs(potencial_user_for_opt,group_list)
                    print()
                    if group_of_opt[0] == "left" and group_of_opt[2] > 1:
                        print(f"Из группы {group_of_opt[1].group_name} был удален пользователь {potencial_user_for_opt}")
                        new_group = Group([potencial_user_for_opt],[user],"Group" + str(amount_of_initial_groups))
                        print(f"{new_group.group_name} была создана")
                        new_group.ShowGroupInfo()
                        group_list.append(new_group)
                        group_of_opt[1].left_subgroup.remove(potencial_user_for_opt)
                        amount_of_initial_groups = amount_of_initial_groups + 1
                        break
                    elif group_of_opt[0] == "right" and group_of_opt[2] > 1:
                        print(f"Из группы {group_of_opt[1].group_name} был удален пользователь {potencial_user_for_opt}")
                        new_group = Group([potencial_user_for_opt],[user],"Group" + str(amount_of_initial_groups))
                        print(f"{new_group.group_name} была создана")
                        new_group.ShowGroupInfo()
                        group_list.append(new_group)
                        group_of_opt[1].right_subgroup.remove(potencial_user_for_opt)
                        amount_of_initial_groups = amount_of_initial_groups + 1
                        break
                    
        else:
            print(f"Все связанные пользователи были распределены по группам")
        print()
        for group in group_list:
            group.ShowGroupInfo()
        return group_list

    def InWhichGroupUserIs(user_number: int, group_list: list) -> list:

        for group in group_list:
            if user_number in group.left_subgroup:
                 print(f"Пользователь {user_number} находится в левой подгруппе группы {group.group_name}")
                 return ["left",group,len(group.left_subgroup)]
            elif user_number in group.right_subgroup:
                print(f"Пользователь {user_number} находится в правой подгруппе группы {group.group_name}")
                return ["right",group,len(group.right_subgroup)]
        return "Пользователь не был найдем ни в одной группе!"

