from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import requests
import random
import re

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

class ActionGetAge(Action):
    def __init__(self):
        self.intervals = {
            '4 anos': ('Nesta idade, deve-se tomar o segundo reforço das vacinas Penta/DTP e '
                'VIP/VOP, além de uma dose das vacinas de varíola e de influenza.'),
            '5 anos': ('Nesta idade, dependendo da dose anterior, é necessário tomar uma'
                ' dose da vacina Pneumocócica 23V.'),
            '4 meses': ('Nesta idade, deve-se tomar a segunda dose das vacinas Penta/DTP, VIP/VOP,'
                        ' Pneumocócica 10V e RotaVirus.'),
            '5 meses': ('Nesta idade, deve-se tomar a segunda dose da Meningocócica C.'),
        }

    def name(self):
      	return "action_get_idade"

    def run(self, dispatcher, tracker, domain):
        sender_message = tracker.current_state()['latest_message']['text']

        age = re.search(r'\d+', sender_message).group()
        type = sender_message.find('mes')

        if type == -1:
            type = age + ' anos'
        else:
            type = age + ' meses'

        message = self.intervals[type]
        dispatcher.utter_message(message)
