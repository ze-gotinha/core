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
        else:
          dispatcher.utter_message('Não conheço essa vacina. Recomendo entrar no site do Ministério da Saúde para mais informações')
      except:
        dispatcher.utter_message('Não conheço essa vacina. Recomendo entrar no site do Ministério da Saúde para mais informações')
      return []


class ActionGetAge(Action):
    def __init__(self):
        self.intervals = {
            "2 meses": "a primeira dose das vacinas Penta/DTP, VIP/VOP, Pneumocócica 10V, Rotavírus.",
            "3 meses": "a primeira dose da vacina Meningocócica C.",
            "4 meses": "a segunda dose das vacinas Penta/DTP, VIP/VOP, Pneumocócica 10V, Rotavírus.",
            "5 meses": "a segunda dose da vacina Meningocócica C.",
            "6 meses": "a terceira dose das vacinas Penta/DTP, VIP/VOP.",
            "9 meses": "uma dose única da febre amarela.",
            "12 meses": "um reforço das vacinas Pneumocócica 10V, Meningocócica C e a primeira dose da triplice viral.",
            "15 meses": "o primeiro reforço das vacinas Penta/DTP, VIP/VOP, e as primeiras doses da Hepatite A e Tetra viral.",
            "4 anos": "o segundo reforço das vacinas Penta/DTP, VIP/VOP e a primeira dose da Varicela.",
            "5 anos": "uma dose da vacina Pneumocócica 23V.",
        }

    def name(self):
      	return "action_get_idade"

    def run(self, dispatcher, tracker, domain):
        link = "http://portalarquivos2.saude.gov.br/images/jpg/2019/marco/22/Calendario-de-Vacinacao-2019-Atualizado-Site-22-03-19.jpg"
        message_tail = "Caso contrário, você pode encontrar a tabela completa de vacinações em: " + link
        sender_message = tracker.current_state()['latest_message']['text']
        age = re.search(r'\d+', sender_message).group()
        type = sender_message.find('mes')

        if type == -1:
            type = age + ' anos'
        else:
            type = age + ' meses'

        message_header = f"Caso sua cartela esteja em dia, com {type} deve-se tomar "

        message = self.intervals[type]
        dispatcher.utter_message(message_header + message + '\n' + message_tail)
