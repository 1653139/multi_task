__author__ = "Quynh Do"
__copyright__ = "Copyright 2017, DAME"


class Word(object):
    def __init__(self, form=None, entity_tag=None):
        self.form = form
        self.entity_tag = entity_tag

    def is_numeric(self):
        try:
            val = self.form
            val = val.replace(",", "")
            num = float(val)
        except ValueError:
            return False
        return True

    def __str__(self):
        return '{} ({})'.format(self.form, self.entity_tag)
