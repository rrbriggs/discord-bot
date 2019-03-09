import json

class UserJsonLoader:
    # def __init__(self, team_member, weight):
    #     self.name = name
    #     self.weight = weight   

    #when a new user is added, this will reset all users and weights
    def front_load_new_user_weights(self, team_member):
        
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
        avg_weight = 1/len(team_member) 

        #store weights / user 
        user_list = []

        for member in team_member:
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

    #todo: this is in development
    def reset_user_weights_all(self, users = None):
        user_list = []
        #current_settings = self.read_json()
        #current_num_users = len(current_settings)
        #avg_weight = 1/current_num_users

        if users is not None:
            avg_weight = 1/len(users)

            for i in users:
                temp_dict = {
                    "name" :i, 
                    "weight_offset": avg_weight
                    }

                user_list.append(temp_dict)
        else:
            current_settings = self.read_json()
            current_num_users = len(current_settings)
            avg_weight = 1/current_num_users

            for i in current_settings:
                temp_dict = {
                    "name" :i['name'], 
                    "weight_offset": avg_weight
                    }

                user_list.append(temp_dict)

        #clear thunderBabyUsers.json
        self.clear_file()
        print(user_list)
        self.create_json_file(user_list)

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
team_member = ['Thundr', 'Adestra', 'Ava', 'Sistuh', 'Xend', 'Getinshwifty', 'Morph', 'Skrooge', 'Whirley', 'Frosty', 'Jeff', 'Devanaa', 'Shifty']

t.reset_user_weights_all(team_member)
#user_list = t.front_load_new_user_weights(team_member)
#t.create_json_file(user_list)
#t.read_json()