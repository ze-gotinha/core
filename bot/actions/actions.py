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
        'febre_amarela': 'Olha, de acordo com o calendário de vacinação, a vacina para febre amarela deve ser tomada apenas uma vez na vida a partir dos 9 meses de idade. Então, se você já tomou alguma vez, não há a necessidade de se preocupar',
        'bcg': 'Então, no caso da BCG, a dose única deve ser tomada ao nascer',
        'influenza': 'No caso da gripe (Influenza), o calendário de vacinas informa que, a partir dos 6 meses de idade, deve-se tomar de uma a duas doses por ano',
      }

    def name(self):
      return "action_vacina_atrasada"

    def run(self, dispatcher, tracker, domain):
      try:
        vacina_informada = tracker.current_state()['latest_message']['entities'][0]['value']

        if not vacina_informada is None:
          vacina_informada = vacina_informada.lower()
        
        d = {
          'febre': 'febre_amarela',
          'amarela': 'febre_amarela',
          'febre amarela': 'febre_amarela',
          'gripe': 'influenza'
        }

        if vacina_informada in d: 
          is_valid_option = True
          my_option = d[vacina_informada]
        elif vacina_informada in self.vacinas:
          is_valid_option = True
          my_option = vacina_informada

        if is_valid_option:
            dispatcher.utter_message(self.vacinas[my_option.lower()])
        else:
          dispatcher.utter_message('Não conheço essa vacina. Recomendo entrar no site do Ministério da Saúde para mais informações')
      except:
        dispatcher.utter_message('Não conheço essa vacina. Recomendo entrar no site do Ministério da Saúde para mais informações')
      return []
        


