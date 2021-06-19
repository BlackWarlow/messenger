from django import forms

from main.models import *

class BaseForm:
    errors_list = []
    
    def app_error(self, err):
        self.errors_list.append(err)
    
    def clear_errors(self):
        self.errors_list = []
