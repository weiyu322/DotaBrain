# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 14:39:46 2016

@author: weiyu322
"""

import pymongo
import dota2api
import time

client = pymongo.MongoClient("localhost",27017)
#link to dota2 database
db = client.dota2
match_collection = db.matches
api = dota2api.Initialise();
COUNTER = 0

def is_valid_match(gmd):
    for player in gmd["players"]:
        if player["leaver_status"] is not 0:
            return False
    return True

def process_match_details(match_id):
    try:
        gmd = api.get_match_details(match_id)
    except:
        return
    
    if not is_valid_match(gmd):
        return
    
    global COUNTER
    COUNTER += 1
    if COUNTER % 100 == 0:
        print "%d mathes has been collected" % COUNTER
    match_collection.insert(gmd)

    

def main():
    '''The main entry point of dotabot.'''
    start_match_id = None
    start_time = time.time()
    #while True:
    #运行12个小时
    while True:
        # Note: GetMatchHistory returns a list of matches in descending order,
        # going back in time.
        #sleep(1.0)
        #logger.debug('Doing GMH query for start_at_match_id=%s' % start_match_id)
        try:
            gmh = api.get_match_history(start_at_match_id=start_match_id,
                                        skill=3,
                                        game_mode=2,
                                        min_players=10)
        except:
            continue
        
        error_code = gmh['status']
        matches = gmh['matches']

        if error_code is not 1:
            #msg = 'GMH query at match_id %s had error code %s. Retrying.' % (start_match_id, error_code)
            #logger.debug(msg)
            continue

        if len(matches) is 0:
            #logger.debug('Finished processing all 500 most recent matches.')
            #exit(0)
            return

        for match in matches:
            match_id = match['match_id']

            if match_collection.find_one({'match_id':match_id}) != None:
                #logger.debug('Encountered match %s already in database, exiting.' % match_id)
                #exit(0)
                continue

            #sleep(1.0)
            process_match_details(match_id)

        last_match_id = matches[-1]['match_id']
        #logger.debug('Match_id of last match of GMH query: %s' % last_match_id)
        # We don't want to record the last match twice, so subtract 1
        start_match_id = last_match_id - 1
    
    print "last_id is",start_match_id
    
        
if __name__ == "__main__":
    
    #getmatchhistory只能获取500场比赛
    #所以每隔20分钟访问一次
    while True:
        main()
        time.sleep(20*60)
    print "successfully collect"