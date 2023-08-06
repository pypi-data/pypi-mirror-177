# coding=utf-8
import random
from otlmow_model.BaseClasses.KeuzelijstField import KeuzelijstField
from otlmow_model.BaseClasses.KeuzelijstWaarde import KeuzelijstWaarde


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlVerkeersregelaarModelnaam(KeuzelijstField):
    """Keuzelijst met modelnamen voor Verkeersregelaar."""
    naam = 'KlVerkeersregelaarModelnaam'
    label = 'verkeersregelaar modelnaam'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlVerkeersregelaarModelnaam'
    definition = 'Keuzelijst met modelnamen voor Verkeersregelaar.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlVerkeersregelaarModelnaam'
    options = {
        'civa-2020': KeuzelijstWaarde(invulwaarde='civa-2020',
                                      label='CIVA 2020',
                                      status='ingebruik',
                                      definitie='CIVA 2020',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlVerkeersregelaarModelnaam/civa-2020'),
        'flow-node': KeuzelijstWaarde(invulwaarde='flow-node',
                                      label='FlowNode',
                                      status='ingebruik',
                                      definitie='FlowNode',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlVerkeersregelaarModelnaam/flow-node'),
        'sx': KeuzelijstWaarde(invulwaarde='sx',
                               label='SX',
                               status='ingebruik',
                               definitie='SX',
                               objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlVerkeersregelaarModelnaam/sx')
    }

    @classmethod
    def create_dummy_data(cls):
        return random.choice(list(map(lambda x: x.invulwaarde,
                                      filter(lambda option: option.status == 'ingebruik', cls.options.values()))))

