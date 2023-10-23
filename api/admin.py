from django.contrib import admin
from .models import *
# Register your models here.

# I wrote this code

# inline class for managing protein domain links inline with other models
class ProteinDomainLinkInLine (admin.TabularInline):
    model = protein_domain_link
    extra = 3

# admin classes for managing models in the admin interface
class TaxonomyAdmin (admin.ModelAdmin):
    list_display = ('taxa_id', 'clade', 'genus', 'species')


class ProteinSequenceAdmin (admin.ModelAdmin):
    list_display = ('protein_id', 'sequence')


class ProteinAdmin (admin.ModelAdmin):
    list_display = ('protein_id', 'taxa_id', 'length')
    inlines = [ProteinDomainLinkInLine]


class DomainAdmin (admin.ModelAdmin):
    list_display = ('domain_id', 'domain_description', 'description')
    inlines = [ProteinDomainLinkInLine]


class DomainCoordinateAdmin (admin.ModelAdmin):
    list_display = ('start', 'stop', 'protein_domain_link_id')


# Register models and admin classes in the admin site

admin.site.register(protein_sequence, ProteinSequenceAdmin)
admin.site.register(proteins, ProteinAdmin)
admin.site.register(taxonomy, TaxonomyAdmin)
admin.site.register(domains, DomainAdmin)
admin.site.register(domain_coordinates, DomainCoordinateAdmin)

# end of code I wrote
