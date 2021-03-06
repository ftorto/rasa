# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.forms import FormAction, FormValidationAction

import pandas as pd


class ActionReplyToUser(Action):

    def name(self) :
        return "action_reply_to_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        """  
        This function will grab the user's need toward informations 
        stored in entities and will provide him back with a convinent anwser
        """
        
        # Reading the kwowledge base file
        path_responses = r"knowledge_base/Chatbot_training_data.xlsx"
        # We want empty cells to remain as so rather than to be parsed as NA 
        # so we add na_filter = False
        data_base = pd.read_excel(path_responses, na_filter= False) 
        # The column Delivery date has empty cells that are converted in NaT (Not a Time)
        # To prevent that we coerce those empty cells into ''
        data_base['Delivery date'] = data_base['Delivery date'].astype(object).where(data_base['Delivery date'].notnull(), '')

        # retrieve informations that the user need.
        repair_order = tracker.get_slot('repair_order')
        status = tracker.get_slot('status')
        delivery_date = tracker.get_slot('delivery_date')
        
        #we declare order infos as None to begin
        infos = None
        
        bot_message = []
        
        # This commented condition is no more necessary as the current action is executed
        # only when the repair_order is not null
        
        
        if status is not None or delivery_date is not None:
            #as indexes in python start at 0 we look at information at index repair_order - 1
            infos = data_base.iloc[int(repair_order) - 1]
            if status != None:
                # We look for the information stored in the colum which is Status
                ro_status = infos.loc['Status']
                if len(ro_status.strip()) == 0:
                    bot_text = f" The status of your repair order {repair_order} is unknown. \n "
                else:
                    bot_text = f" The status of your repair order {repair_order} is {ro_status}. \n"
                bot_message.append(bot_text)
            if delivery_date !=  None:
                # We look for the information stored in the colum which is Delivery date
                # and we convert the result into a string
                ro_delivery_date = str(infos.loc['Delivery date'])
                if len(ro_delivery_date.strip()) == 0:
                    bot_text = f"The delivery date of your repair order is unknown. "
                else:               
                    bot_text = f"The estimated delivery date is {ro_delivery_date}."  
                bot_message.append(bot_text)   
        else:
            # this action is not implemented yet
            dispatcher.utter_message(text= "Send all information to the user or ask him to be more specific ")
            return[]    
        
        dispatcher.utter_message(text  = "".join(bot_message))     

        return [SlotSet("simul_info", None),
                SlotSet("repair_order", None),
                SlotSet("status", None),
                SlotSet("delivery_date", None)]


class ValidateAskRequiredInfoToUserForm(FormValidationAction):
    
    def name(self):
        return 'validate_asking_required_info_to_user_form'

    def validate_simul_info(self, slot_value, dispatcher, tracker, domain):
        
        """
        This function will validate that the required informations was given 
        by the user before he is provided with an anwser
        """
        
        repair_order = tracker.get_slot('repair_order')
        
        if repair_order is not None and type(int(str(repair_order))) == int:
            return {"simul_info": repair_order}
        else:
            return {"simul_info": None}