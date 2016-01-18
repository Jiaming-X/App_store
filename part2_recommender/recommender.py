from pymongo import MongoClient
from dataservice import DataService
import operator
import math
import time

class Helper(object):
    @classmethod
    def cosine_similarity(cls, app_list1, app_list2):
        return float(cls.__count_match(app_list1, app_list2) / math.sqrt(len(app_list1) * len(app_list2)))	

    @classmethod
    def __count_match(cls, list1, list2):
        count = 0
        for element in list1:
            if element in list2:
                count += 1
        return count
        

def calculate_top_k(app, user_download_history, num):
    app_similarity = {}	
    count = 0
    for apps in user_download_history:
        similarity = Helper.cosine_similarity([app], apps)
        for other_app in apps:
            if app_similarity.has_key(other_app):
                app_similarity[other_app] = app_similarity[other_app] + similarity
            else:
            	app_similarity[other_app] = similarity
    #print(app_similarity)        	
    if not app_similarity.has_key(app):            	
        return False

    app_similarity.pop(app)
    sorted_tups = sorted(app_similarity.items(), key=operator.itemgetter(1), reverse=True)
    name = "top_" + str(num) + "_app"
    DataService.update_app_info({'app_id':app}, {'$set':{name:sorted_tups[:num]}})
    return True


def generate_recommendations(user_download_history, recommendations):
    all_user_id = user_download_history.keys()
    for one_user_id in all_user_id:
        generate_recommendations_for_one_user(user_download_history, recommendations, one_user_id)
    return    


def generate_recommendations_for_one_user(user_download_history, recommendations, one_user_id):
    all_app_id = recommendations.keys()
    recommended_app_list = []
    sim_score = []	

    for app in user_download_history[ one_user_id ]:
        if app in all_app_id:
            for one_sim_app in recommendations[app]:
                recommended_app_list.append(one_sim_app[0])
                sim_score.append(one_sim_app[1])	

    sorted_list = [x for (y,x) in sorted(zip(sim_score, recommended_app_list), key=lambda pair: pair[0], reverse = True)] 
    DataService.update_user_download_history({'user_id':one_user_id}, {'$set':{"recommended_apps":sorted_list}})
    return


def main():
    try:
        client = MongoClient('localhost', 27017)
        DataService.init(client)

        user_download_history = DataService.retrieve_user_download_history()
        all_app_id = DataService.get_all_app_id()

        for one_id in all_app_id:
            calculate_top_k(one_id, user_download_history.values(), 5)
        
        recommendations = DataService.retrieve_recommended_items()
        generate_recommendations(user_download_history, recommendations)

    except Exception as e:
        print(e)
    finally:
        if 'client' in locals():
            client.close()	


start = time.clock()
if __name__ == "__main__":
    main()	
end = time.clock()
print "time elapsed = " + str(end - start)


