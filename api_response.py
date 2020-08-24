import requests, json
from flask import jsonify, g
BASE_URL = 'https://api.collegeai.com/v1/api/college-list'
API_KEY = 'api_key'
def sendRequest(data):
    """Request API from backend """
    d1 = json.dumps(data)
    
    resp = requests.get(f'{BASE_URL}?api_key={API_KEY}&filters={d1}&info_ids=website,shortDescription,longDescription,campusImage,city,stateAbbr,aliases,acceptanceRate,locationLong,locationLat')
    
    data = json.loads(resp.text)
    
    if (data['success']):
        
        filtered_response = filterUserFavorited(data['colleges']) 
    
    return filtered_response


def sendSingleCollegeRequest(collegeID):
    """Request API from backend """
    id = collegeID['collegeID']
    
    resp = requests.get(f'{BASE_URL}?api_key={API_KEY}&college_unit_ids={id}&info_ids=average_financial_aid,application_website,campusImage,shortDescription,city,stateAbbr,in_state_tuition,out_of_state_tuition,website,acceptanceRate,student_faculty_ratio,financial_aid_website,similar_colleges')
    return resp.text

def ErrorInput(form):
    """ Compose error response """
    resp = {'errors': {}}
    for error in form.errors:
        resp['errors'][error] = eval(f'form.{error}.errors')
        
    return jsonify(resp)


def filterUserFavorited(data):
    """ Remove user favorited colleges from the response """
    
    my_colleges = []
    
    user_favorites = g.user.favorites
    college_ids = [fav.college_id for fav in user_favorites]
    
    for n in data:
        
        if int(n['collegeUnitId']) not in college_ids :
            my_colleges.append(n)
    
    return my_colleges    