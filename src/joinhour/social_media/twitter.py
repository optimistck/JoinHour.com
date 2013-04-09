__author__ = 'aparbane'

import json
import httplib2


def get_friends_and_followers_count(screen_name):
    """

    :param screen_name:
    :return: Friends count , followed by follower's count for a screen name. Returns "No available" if no http connection can be made

    """
    TWITTER_SHOW_FOLLOWERS_API = "https://api.twitter.com/1/users/show.json?screen_name=" + screen_name
    resp, content = {},{}
    try:
        resp, content = httplib2.Http(timeout=10).request(TWITTER_SHOW_FOLLOWERS_API)
    except Exception as e:
        pass
        #Ignore any http connection related exceptions
    if 'status' not in resp or resp['status'] != '200':
        return {'friends_count' : 'Not available', 'followers_count' : 'Not available'}
    else:
        response = json.loads(content)
        return {'friends_count':response['friends_count'], 'followers_count':response['followers_count']}




def main():
    print get_friends_and_followers_count('aparupb')


if __name__ == '__main__':
    main()