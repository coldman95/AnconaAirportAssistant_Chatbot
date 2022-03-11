from typing import Any, Text, Dict, List
import requests
from rasa_sdk.events import SlotSet
import json
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk.events import SlotSet


class ActionFindInfo(Action):

    def name(self) -> Text:
        return "action_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = str(tracker.get_slot('find_info1'))
        PARAMS = {'Flight number': name.upper()}
        r = requests.get(url='http://localhost:3000/items/', params = PARAMS)
        data = r.json()
        if data == []:
            output = "No flight with this tracking number, please put a valid tracking number."
        else:
            partenze = data[0]['Departure']
            arrivi = data[0]['Destination']
            orapartenza = data[0]['Time of departure']
            oraarrivo = data[0]['Time of arrival']
            compagnia = data[0]['Airline company']
            giorno = data[0]['Frequency']
            output = "Your flight: {}, from {} will leave {} on {} at {} and will arrive in {} at {}.".format(name.upper(), compagnia, partenze, giorno, orapartenza, arrivi, oraarrivo)
        dispatcher.utter_message(text=output)
        return []


    class ActionDeparture(Action):
        def name(self) -> Text:
            return "action_csv"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            df = pd.read_json(r'csvjson_departure.json')

            for j in df.itertuples():
                dispatcher.utter_message(
                    "COMPANY: " + str(j[2]) + '\n' + "DEPARTURE: " + str(j[3]) + '\n' + "ARRIVAL: " +
                    str(j[4]) + '\n' + "FREQUENCY: " + str(j[5]) + '\n' + "TIME OF DEPARTURE: " + str(j[6]) +
                    '\n' + "TIME OF ARRIVAL: " + str(j[7]) + '\n' + "FLIGHT CODE: " + str(j[8]))
            return []


    class ActionArrival(Action):
        def name(self) -> Text:
            return "arrival_csv"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            df = pd.read_json(r'csvjson_arrival.json')

            for j in df.itertuples():
                dispatcher.utter_message(
                    "COMPANY: " + str(j[2]) + '\n' + "DEPARTURE: " + str(j[3]) + '\n' + "ARRIVAL: " +
                    str(j[4]) + '\n' + "FREQUENCY: " + str(j[5]) + '\n' + "TIME OF DEPARTURE: " + str(j[6]) +
                    '\n' + "TIME OF ARRIVAL: " + str(j[7]) + '\n' + "FLIGHT CODE: " + str(j[8]))
            return []


class MyFallback(Action):

    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response = "utter_fallback")
        return []