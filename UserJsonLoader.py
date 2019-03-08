import json

class UserJsonLoader:
    # def __init__(self, team_member, weight):
    #     self.name = name
    #     self.weight = weight   

    #when a new user is added, this will reset all users and weights
    def front_load_new_user_weights(self, team_members):
        
        #read current users and weights, strip off offsets from average
        existing_user_offset = []

        current_settings = self.read_json()
        current_num_users = len(current_settings)
        old_avg_weight = 1/current_num_users


        for i in current_settings:
            
            offset_num = i['weight'] - old_avg_weight

            temp_dict = {
                "name" :i['name'], 
                "weight_offset": offset_num
                }

            existing_user_offset.append(temp_dict)

        #clear thunderBabyUsers.json
        self.clear_file()

        #basic psuedo-rng
        avg_weight = 1/len(team_members) 

        #store weights / user 
        user_list = []

        #testing generator expression approach
        next(member for member in team_members if member['name'] == )

        #matching names from offset and new user list, adding offset
        #todo: check if this explodes on a new user w/ no offset
        for member in team_members:
            for user in existing_user_offset:
                if user['name'] == member:
                    
                    print(f"{member}'s weight offset: {user['weight_offset']}\n"
                        f"{member}'s weight after offset: {avg_weight + user['weight_offset']}")
                    
                    json_dict = { 
                        "name" : member, 
                        "weight": avg_weight + user['weight_offset']
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
            # for i in json_value:
            #     print(i['name'], i['weight'])    

            return json_value


#testing
t = UserJsonLoader()

#user list
team_members = ['Thundr', 'Adestra', 'Ava', 'Sistuh', 'Xend', 'Getinshwifty', 'Morph', 'Skrooge', 'Whirley', 'Frosty', 'Jeff', 'Devanaa', 'Shifty']


user_list = t.front_load_new_user_weights(team_members)
t.create_json_file(user_list)
t.read_json()