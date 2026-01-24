import django.template.context
from copy import copy

def _pinned_base_context_copy(self):
    # Fix for Python 3.14 where copy(super()) returns a super object
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.__dict__ = self.__dict__.copy()
    duplicate.dicts = self.dicts[:]
    return duplicate

# Monkeypatch
print("Applying Django Python 3.14 compatibility patch for BaseContext.__copy__")
django.template.context.BaseContext.__copy__ = _pinned_base_context_copy
