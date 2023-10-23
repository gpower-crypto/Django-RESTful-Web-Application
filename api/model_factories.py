import factory
from .models import *

# I wrote this code

class TaxonomyFactory(factory.django.DjangoModelFactory):
    taxa_id = factory.Sequence(lambda n: 35780 + n) # generate a sequence of unique values starting from 35780
    clade = factory.Faker('random_element', elements=['A', 'B', 'C']) # generate a random element from the given list
    genus = factory.Faker('word')  # create a random word
    species = factory.Faker('word')  # create a random word

    class Meta:
        model = taxonomy


class ProteinSequenceFactory(factory.django.DjangoModelFactory):
    protein_id = factory.Sequence(lambda n: 'A0A016VK{}'.format(n)) # generate a sequence of unique values
    sequence = factory.Faker('text', max_nb_chars=40000) # generate random text with a maximum of 40000 characters

    class Meta:
        model = protein_sequence


class ProteinFactory(factory.django.DjangoModelFactory):
    protein_id = factory.Sequence(lambda n: 'A0A016VK{}'.format(n)) # generate a sequence of unique values
    length = factory.Faker('random_int', min=100, max=1500) # generate a random integer from 100 to 1500
    taxa = factory.SubFactory(TaxonomyFactory) # create a related TaxonomyFactory instance

    class Meta:
        model = proteins


class DomainFactory(factory.django.DjangoModelFactory):
    domain_id = factory.Sequence(lambda n: 'PF0{}'.format(n)) # generate a sequence of unique values
    domain_description = factory.Faker('word') # generate a random word
    description = factory.Faker('sentence') # generate a random sentence

    class Meta:
        model = domains


class ProteinDomainLinkFactory(factory.django.DjangoModelFactory):
    protein = factory.SubFactory(ProteinFactory)  # create a related ProteinFactory instance
    domain = factory.SubFactory(DomainFactory) # create a related DomainFactory instance

    class Meta:
        model = protein_domain_link


class DomainCoordinateFactory(factory.django.DjangoModelFactory):
    start = factory.Faker('random_int', min=1, max=100) # generate a random integer from 1 to 100
    stop = factory.Faker('random_int', min=105, max=200) # generate a random integer from 105 to 200
    protein_domain_link = factory.SubFactory(ProteinDomainLinkFactory) # create a related ProteinDomainLinkFactory instance

    class Meta:
        model = domain_coordinates

# end of code I wrote