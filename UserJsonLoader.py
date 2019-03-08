import json
from User import User

class UserJsonLoader:
    # def __init__(self, team_member, weight):
    #     self.name = name
    #     self.weight = weight   

    #when a new user is added, this will reset all users and weights
    def front_load_new_user_weights(self, team_members):
    
        #clear thunderBabyUsers.json
        self.clear_file()

        #basic psuedo-rng
        avg_weight = 1/len(team_members) 

         #store weights / user 
        user_list = []

        for member in team_members:
            json_dict = { 
                "name" : member, 
                "weight": avg_weight 
                }

            user_list.append(json_dict)

        return user_list

    def clear_file(self):
        open("thunderBabyUsersJson.json", "w").close
    
    #accepts a list of dicts
    def create_json_file(self, users):
        with open("thunderBabyUsersJson.json", "a") as f:
            f.write(json.dumps(users, indent=2))

        f.close
    
    # def write_new_weights(self, user):
        
    #returns list of user data as dict [{}, {}]   
    def read_json(self):
        with open("thunderBabyUsersJson.json", "r") as fh:
            json_string = fh.read()
            json_value = json.loads(json_string)

            #for testing
            for i in json_value:
                print(i['name'], i['weight'])    

            return json_value


#testing
t = UserJsonLoader()

#user list
team_members = ['Thundr', 'Adestra', 'Ava', 'Sistuh', 'Xend', 'Getinshwifty', 'Morph', 'Skrooge', 'Whirley', 'Frosty', 'Jeff', 'Devanaa', 'Shifty']


user_list = t.front_load_new_user_weights(team_members)
t.create_json_file(user_list)
t.read_json()