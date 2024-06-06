users_list = [1, 2, 3, 4, 5, 6, 7, 8]

groups_list = [[5, 6, 7, 8, 9, 10], [7, 8, 9, 10, 11, 122]]



def unique_user(users_list, groups_list):
    user = set(users_list)
    groups_by_user = set([item for sublist in groups_list for item in sublist])
    user.update(groups_by_user)
    return user
    
print(unique_user(users_list, groups_list))