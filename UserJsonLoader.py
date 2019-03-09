import json

class UserJsonLoader:
    # def __init__(self, team_member, weight):
    #     self.name = name
    #     self.weight = weight   

    #when a new user is added, this will reset all users and weights
    def add_new_member(self, team_member):
        
        #read current users and weights, strip off offsets from average
        existing_user_offset = []

        current_settings = self.read_json()
        current_num_users = len(current_settings)
        old_avg_weight = 1/current_num_users

        #create list of dicts of current user names and offsets (existing_user_offset)
        for i in current_settings:
            offset_num = i['weight'] - old_avg_weight

            temp_dict = {
                "name": i['name'], 
                "weight_offset": offset_num
                }

            existing_user_offset.append(temp_dict)

        #clear thunderBabyUsers.json
        self.clear_file()

        #basic avg weight including the newbie
        avg_weight = 1 / (len(existing_user_offset) + 1)

        #add newbie to lists, and rename lists for readability
        new_team_member_offset_dict = {
            "name": team_member,
            "weight": 0
        }

        updated_user_offset_list = existing_user_offset.append(new_team_member_offset_dict)

        #store weights / user 
        updated_user_list = []

        #todo: team_member is no longer a list of dicts, its just one user name string

        for user in updated_user_offset_list:
            print(f"{user['name']}'s weight offset: {user['weight_offset']}\n"
                f"{user['name']}'s weight after offset: {avg_weight + user['weight_offset']}")
            
            json_dict = { 
                "name" : user['name'], 
                "weight": avg_weight + user['weight_offset']
            }   

        updated_user_list.append(json_dict)

        return updated_user_list

    #resets all user weights, will also set up json file when passed a list of user names
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
#user_list = t.add_new_member(team_member)
#t.create_json_file(user_list)
#t.read_json()