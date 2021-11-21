# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetUserNeedAndReply(Action):

    def name(self) :
        return "action_get_user_need_and_reply"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        """  
        This function will grab the user's need toward informations 
        stored in entities and will provide him back with a convinent anwser
        """
        repair_order = tracker.get_slot('repair_order')
        status = tracker.get_slot('status')
        delivery_date = tracker.get_slot('delivery_date')
        
        bot_message = []
        if  repair_order == None:
            bot_text = "It seems that you did not provide a repair order number. Please provide one"
            dispatcher.utter_message(text  = bot_text)
            return[]
        elif status != None or delivery_date !=  None:
            if status != None:
                ##execute a function + retrive the status based on the repair number
                # + put that information into a message
                ro_status = 'Work in progress'
                bot_text = f"The status of your Repair Order is {ro_status}. "
                bot_message.append(bot_text)
            if delivery_date !=  None:
                ##execute a function + retrive the delivery date based on the repair number
                # + put that information into a message
                ro_delivery_date = '04/01/2021  09:00:00'
                bot_text = f"The estimated delivery date is {ro_delivery_date}"  
                bot_message.append(bot_text)   
        else:
            dispatcher.utter_message(text= "Envoyer toutes les informations concerant le ro")
            return[]    
            
            
        dispatcher.utter_message(text  = "".join(bot_message))     

        return []
