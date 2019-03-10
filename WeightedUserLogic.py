import random
import UserJsonLoader

class UserWeightedMadness:
    #changes weight when a user has a joke mentioned about them to reduce chance of repeat offenses
    weight_modifier = -0.005

    user_json_loader = UserJsonLoader.UserJsonLoader()

    #return a user  
    def GetUserForJoke(self):
        #get current user list and weights
        user_list = self.user_json_loader.get_users_and_weights()

        highest_user_and_weight_after_randomizer = {}
        highest_randomized_weight = -40

        for user in user_list:
            randomized_weight = self.MulitplyUserWeightRandomizer(user['weight'])

            if randomized_weight > highest_randomized_weight:
                highest_randomized_weight = randomized_weight

                highest_user_and_weight_after_randomizer = {
                    "name": user['name'],
                    'randomizedWeight': randomized_weight
                }

        #reduce weight on called user to reduce chance of repeat offense
        self.user_json_loader.modify_user(highest_user_and_weight_after_randomizer['name'], self.weight_modifier)

        #return user name string
        return highest_user_and_weight_after_randomizer['name']

    def MulitplyUserWeightRandomizer(self, weight):
        random_number = random.random()

        randomized_weight = random_number * weight
        
        return randomized_weight