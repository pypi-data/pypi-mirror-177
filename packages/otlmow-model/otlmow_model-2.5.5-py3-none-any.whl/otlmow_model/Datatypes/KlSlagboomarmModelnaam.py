# coding=utf-8
import random
from otlmow_model.BaseClasses.KeuzelijstField import KeuzelijstField


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlSlagboomarmModelnaam(KeuzelijstField):
    """De modelnaam van de slagboomarm."""
    naam = 'KlSlagboomarmModelnaam'
    label = 'Slagboomarm modelnaam'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlSlagboomarmModelnaam'
    definition = 'De modelnaam van de slagboomarm.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlSlagboomarmModelnaam'
    options = {
    }

    @classmethod
    def create_dummy_data(cls):
        return random.choice(list(map(lambda x: x.invulwaarde,
                                      filter(lambda option: option.status == 'ingebruik', cls.options.values()))))

