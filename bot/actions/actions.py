from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import requests
import random

class ActionTest(Action):
   def name(self):
      return "action_test"

   def run(self, dispatcher, tracker, domain):
        try:
          dispatcher.utter_message("Mensagem enviada por uma custom action.")
        except ValueError:
          dispatcher.utter_message(ValueError)

class ActionVacinaAtrasada(Action):
    def __init__(self):
      self.vacinas = {
        'febre_amarela': '',
      }

    def name(self):
      return "action_vacina_atrasada"

    def run(self, dispatcher, tracker, domain):
      pass
        


