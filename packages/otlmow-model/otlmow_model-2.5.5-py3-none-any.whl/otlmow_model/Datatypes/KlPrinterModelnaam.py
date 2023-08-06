# coding=utf-8
import random
from otlmow_model.BaseClasses.KeuzelijstField import KeuzelijstField


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlPrinterModelnaam(KeuzelijstField):
    """Lijst met modelnamen van weegcellen."""
    naam = 'KlPrinterModelnaam'
    label = 'Weegcel modelnaam'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlPrinterModelnaam'
    definition = 'Lijst met modelnamen van weegcellen.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlPrinterModelnaam'
    options = {
    }

    @classmethod
    def create_dummy_data(cls):
        return random.choice(list(map(lambda x: x.invulwaarde,
                                      filter(lambda option: option.status == 'ingebruik', cls.options.values()))))

