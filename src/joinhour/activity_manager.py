__author__ = 'aparbane'

from src.joinhour.models.activity import Activity
from src.joinhour.models.activity import Status

class ActivityManager(object):

    '''
    TODO- Following a stateful model for this as of now. Do we need a more stateless implementation of activity manager in future?
    Things to think about
    * Concurrency
    * Memory
    '''

    @classmethod
    def get(cls,activityId):
        return ActivityManager(activityId)

    def __init__(self,activity_id):
        self._activity = Activity.get_by_id(activity_id)


    def connect(self,user_id,**kwargs):
        #Check what is the current status and the spots_remaining
        #If more than one spots are remaining
            #If the status is INITIATED change it to FORMING
            #else If the status is FORMING
                #If this would be the last spot change status to COMPLETE
                    #Queue a task in JoinNotificationQueue for notifying user
                #else Don't change the status
                    #Queue a task in JoinNotificationQueue for notifying user
        #else - raise an exception
        pass


    def mark_expired(self):
        self._change_status(Status.EXPIRED)

    def can_join(self,userId):
        pass

    def _change_status(self,new_status):
        #TODO Need to think about Thread safety here
        #TODO Once the activity is expired or complete need to move it to a different table. Primarly for analytics support
        self._activity.status = new_status
        self._activity.put()



















