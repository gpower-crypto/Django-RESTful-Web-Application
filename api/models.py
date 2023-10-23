from django.db import models

# Create your models here.

# I wrote this code

from django.db import models

# Create your models here.

# model for the taxonomy data
class taxonomy(models.Model):
    taxa_id = models.CharField(max_length=256, null=False, blank=False)  # ID of the taxonomy
    clade = models.CharField(max_length=100, null=False, blank=False)  # clade information
    genus = models.CharField(max_length=100, null=False, blank=False)  # genus information
    species = models.CharField(max_length=100, null=False, blank=False)  # species information

    def __str__(self):
        return self.taxa_id

# model for the protein sequences
class protein_sequence(models.Model):
    protein_id = models.CharField(max_length=256, null=False, blank=False)  # ID of the protein
    sequence = models.CharField(max_length=40000, null=False, blank=False)  # Protein sequence data

# model for the proteins
class proteins(models.Model):
    protein_id = models.CharField(max_length=256, null=False, blank=False)  # ID of the protein
    taxa = models.ForeignKey(taxonomy, on_delete=models.CASCADE)  # foreign key to taxonomy model
    length = models.IntegerField(null=False, blank=False)  # length of the protein

    def __str__(self):
        return self.protein_id

# model for the protein domains
class domains(models.Model):
    domain_id = models.CharField(max_length=256, null=False, blank=False)  # ID of the domain
    domain_description = models.CharField(max_length=500, null=False, blank=False)  # description of the domain
    description = models.CharField(max_length=500, null=False, blank=False)  # additional description
    protein = models.ManyToManyField(proteins, through='protein_domain_link')  # many-to-many relationship with proteins

    def __str__(self):
        return self.domain_id

# model for the the junction table between proteins and domains
class protein_domain_link(models.Model):
    protein = models.ForeignKey(proteins, on_delete=models.CASCADE)  # foreign key to proteins model
    domain = models.ForeignKey(domains, on_delete=models.CASCADE)  # foreign key to domains model

# model for the domain coordinates
class domain_coordinates(models.Model):
    start = models.IntegerField(null=False, blank=False)  # start position of domain coordinates
    stop = models.IntegerField(null=False, blank=False)  # stop position of domain coordinates
    protein_domain_link = models.ForeignKey(protein_domain_link, on_delete=models.CASCADE)  # foreign key to protein_domain_link model

# end of code I wrote