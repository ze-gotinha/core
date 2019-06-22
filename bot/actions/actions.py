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
            dispatcher.utter_message('Se precisar de mais informações, entra nesse site aqui: http://www.saude.gov.br/saude-de-a-z/vacinacao/vacine-se')
        else:
          dispatcher.utter_message('Não conheço essa vacina. Recomendo entrar no site do Ministério da Saúde para mais informações: http://www.saude.gov.br/saude-de-a-z/vacinacao/vacine-se')
      except:
        dispatcher.utter_message('Não conheço essa vacina. Recomendo entrar no site do Ministério da Saúde para mais informações: http://www.saude.gov.br/saude-de-a-z/vacinacao/vacine-se')
      return []


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
