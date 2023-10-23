import csv
import django
import sys
import os
from collections import defaultdict

# I wrote this code

sys.path.append("C:/Users/Mohan Krishna/Desktop/djangoVenv/RESTWebApp")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RESTWebApp.settings')

django.setup()
from api.models import *

# paths to data files
data_file1 = 'C:/Users/Mohan Krishna/Desktop/djangoVenv/RESTWebApp/data/assignment_data_sequences.csv'
data_file2 = 'C:/Users/Mohan Krishna/Desktop/djangoVenv/RESTWebApp/data/assignment_data_set.csv'
data_file3 = 'C:/Users/Mohan Krishna/Desktop/djangoVenv/RESTWebApp/data/pfam_descriptions.csv'

# data structures for storing the data
taxonomy_list = defaultdict(list)  # store taxonomy information
protein_sequences = defaultdict(str)  # store protein sequences
protein_list = defaultdict(list)  # store protein information
domain_list = defaultdict(list)  # store domain information
domain_coordinate_set = set()  # store domain coordinates
protein_domain_set = set()  # store protein-domain links

# read and process data from data_file1 (protein sequences)
with open(data_file1) as csv_file1:
    csv_reader = csv.reader(csv_file1, delimiter=',')
    for row in csv_reader:
        protein_sequences[row[0]] = row[1]

# read and process data from data_file2 (protein and taxonomy data)
with open(data_file2) as csv_file2:
    csv_reader = csv.reader(csv_file2, delimiter=',')
    for row in csv_reader:
        protein_list[row[0]] = [row[1]] + [row[8]]
        scientific_names = row[3].split(' ')
        for i in range(len(scientific_names)):
            scientific_names[i] = scientific_names[i].capitalize()
        taxonomy_list[row[1]] = [row[2]] + scientific_names
        domain_list[row[5]] = [row[0]] + [row[4]]
        domain_coordinate_set.add((row[0], row[5], row[6], row[7]))
        protein_domain_set.add((row[0], row[5]))

# read and process data from data_file3 (domain descriptions)
with open(data_file3) as csv_file3:
    csv_reader = csv.reader(csv_file3, delimiter=',')
    for row in csv_reader:
        domain_list[row[0]].insert(1, row[1])

# clear existing data in the database tables
protein_domain_link.objects.all().delete()
proteins.objects.all().delete()
protein_sequence.objects.all().delete()
taxonomy.objects.all().delete()
domains.objects.all().delete()
domain_coordinates.objects.all().delete()

# populate taxonomy table
bulk_list = list()
for taxa_id, data in taxonomy_list.items():
    bulk_list.append(
        taxonomy(taxa_id=taxa_id, clade=data[0], genus=data[1], species=data[2]))
taxonomy.objects.bulk_create(bulk_list)

# populate proteins table
bulk_list = []
for protein_id, data in protein_list.items():
    taxonomy_id = taxonomy.objects.get(taxa_id=data[0])
    bulk_list.append(proteins(protein_id=protein_id,
                     taxa=taxonomy_id, length=data[1]))
proteins.objects.bulk_create(bulk_list)

# populate protein_sequence table
bulk_list = []
for protein_id, sequence in protein_sequences.items():
    bulk_list.append(protein_sequence(
        protein_id=protein_id, sequence=sequence))
protein_sequence.objects.bulk_create(bulk_list)

# populate domains table
bulk_list = []
for domain_id, data in domain_list.items():
    bulk_list.append(domains(domain_id=domain_id,
                     domain_description=data[1], description=data[2]))
domains.objects.bulk_create(bulk_list)

# populate protein_domain_link table
bulk_list = []
for set in protein_domain_set:
    domainId = domains.objects.get(domain_id=set[1])
    proteinId = proteins.objects.get(protein_id=set[0])
    bulk_list.append(domains.protein.through(
        domain=domainId, protein=proteinId))
domains.protein.through.objects.bulk_create(bulk_list)

# populate domain_coordinates table
bulk_list = []
for set in domain_coordinate_set:
    proteinId = proteins.objects.get(protein_id=set[0])
    domainId = domains.objects.get(domain_id=set[1])
    protein_domain_link_data = protein_domain_link.objects.get(
        protein=proteinId, domain=domainId)
    bulk_list.append(domain_coordinates(
        start=set[2], stop=set[3], protein_domain_link=protein_domain_link_data))
domain_coordinates.objects.bulk_create(bulk_list)

# end of code I wrote