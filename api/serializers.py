from rest_framework import serializers
from .models import *

# I wrote this code


class TaxonomySerializer(serializers.ModelSerializer):
    # serialize taxonomy model data
    class Meta:
        model = taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']

    def create(self, validated_data):
        # create and return a new taxonomy record
        organism = taxonomy.objects.create(**validated_data)
        return organism


class ProteinSerializer(serializers.ModelSerializer):
    # serialize protein model data
    class Meta:
        model = proteins
        fields = ['length']


class ProteinSequenceSerializer(serializers.ModelSerializer):
    # serialize protein sequence model data
    class Meta:
        model = protein_sequence
        fields = ['protein_id', 'sequence']

    def validate(self, data):
        # validation for protein_id and sequence fields
        protein_id = data.get('protein_id')
        sequence = data.get('sequence')
        if not protein_id:
            raise serializers.ValidationError("protein_id field is required.")
        if not sequence:
            raise serializers.ValidationError("sequence field is required.")
        return data

    def create(self, validated_data):
        # create a new protein sequence record
        protein_id = self.initial_data.get('protein_id')
        protein_exists = protein_sequence.objects.filter(
            protein_id=protein_id).exists()

        protein_seq = protein_sequence(**{**validated_data})

        if not protein_exists:
            protein_seq.save()
            return protein_seq
        return protein_seq


class PfamSerializer(serializers.ModelSerializer):
    # serialize pfam domain model data
    class Meta:
        model = domains
        fields = ['domain_id', 'domain_description']


class DomainSerializer(serializers.ModelSerializer):
    # serialize domain model data
    class Meta:
        model = domains
        fields = ['description']


class DomainCoordinateSerializer(serializers.ModelSerializer):
    # serialize domain coordinate model data
    class Meta:
        model = domain_coordinates
        fields = ['start', 'stop']


class OrganismProteinSerializer(serializers.ModelSerializer):
    # serialize protein model data associated with an organism
    class Meta:
        model = proteins
        fields = ['protein_id']


class DomainIdSerializer(serializers.ModelSerializer):
    # serialize domain model data based on its ID
    class Meta:
        model = domains
        fields = ['id']


class ProteinRecordSerializer(serializers.ModelSerializer):
    # serialize protein model data along with taxonomy
    class Meta:
        model = proteins
        fields = ['protein_id', 'length', 'taxa_id']

    def validate(self, data):
        # validation for protein_id, length, and taxa_id fields
        protein_id = data.get('protein_id')
        length = data.get('length')
        taxonomy_data = self.initial_data.get('taxonomy')
        taxa_id = taxonomy_data['taxa_id']

        if not protein_id:
            raise serializers.ValidationError("protein_id field is required.")
        if not length:
            raise serializers.ValidationError("length field is required.")
        if not taxa_id:
            raise serializers.ValidationError("taxa_id field is required.")
        return data

    def create(self, validated_data):
        protein_id = self.initial_data.get('protein_id')
        protein_exists = proteins.objects.filter(
            protein_id=protein_id).exists()

        taxonomy_data = self.initial_data.get('taxonomy')
        taxonomy_exists = taxonomy.objects.filter(
            taxa_id=taxonomy_data['taxa_id']).exists()

        length = self.initial_data.get('length')
        # check if protein already exists
        if protein_exists:
            protein_data = proteins.objects.get(protein_id=protein_id)
            # check if the protein is linked to the correct taxonomy
            if not taxonomy_exists:
                raise serializers.ValidationError(
                    "Invalid taxa_id, please enter the correct organism taxa_id for the given protein")
            if str(protein_data.length) != str(length):
                raise serializers.ValidationError(
                    "Incorrect length, please enter the correct length for the given protein")
            return protein_data

        # if it's a new protein
        else:
            if not taxonomy_exists:
                # add the new organism to the taxonomy table
                taxonomy_serializer = TaxonomySerializer(data=taxonomy_data)
                taxonomy_serializer.is_valid(raise_exception=True)
                taxonomy_serializer.save()

            data = taxonomy.objects.get(taxa_id=taxonomy_data['taxa_id'])

            protein = proteins(**{**validated_data,
                                  'taxa_id': data.id})

            protein.save()
            return protein


class ProteinDomainLinkSerializer(serializers.ModelSerializer):
    # serialize protein-domain link model data
    class Meta:
        model = protein_domain_link
        fields = ['protein_id', 'domain_id']

    def validate(self, data):
        # validation for domain_id field
        domain_data_list = self.initial_data.get('domains')

        if not domain_data_list:
            raise serializers.ValidationError("domains field is required.")
        for record in domain_data_list:
            pfam_data = record.get('pfam_id')
            if not pfam_data:
                raise serializers.ValidationError(
                    "pfam_id field is required in domains.")
            domain_id = pfam_data.get('domain_id')
            if not domain_id:
                raise serializers.ValidationError(
                    "domain_id field is required in pfam_id.")
        return data

    def create(self, validated_data):
        protein_id = self.initial_data.get('protein_id')
        protein_data = proteins.objects.get(protein_id=protein_id)
        domain_data_list = self.initial_data.get('domains')
        protein_domain = None
        for data in domain_data_list:
            pfam_data = data['pfam_id']
            domain_id = pfam_data['domain_id']

            # check if the domain already exists
            domain_exists = domains.objects.filter(
                domain_id=domain_id).exists()

            # if the domain doesn't exist, create a new domain
            if not domain_exists:
                domain_record = domains(**{**validated_data,
                                           'domain_id': pfam_data['domain_id'],
                                           'domain_description': pfam_data['domain_description'],
                                           'description': data['description']})
                domain_record.save()

            domain_data = domains.objects.get(domain_id=pfam_data['domain_id'])

            # check if the protein-domain link already exists
            protein_domain_link_data = protein_domain_link.objects.filter(
                protein_id=protein_data.id, domain_id=domain_data.id).first()

            # if the protein-domain link doesn't exist, create a new link
            if not protein_domain_link_data:
                protein_domain = protein_domain_link(**{**validated_data,
                                                        'protein_id': protein_data.id,
                                                        'domain_id': domain_data.id})
                protein_domain.save()
        if protein_domain is None:
            raise serializers.ValidationError(
                "Record already exists, Please enter a new record.")
        return protein_domain


class DomainCoordinateRecordSerializer(serializers.ModelSerializer):
    # serialize domain coordinate record model data
    class Meta:
        model = domain_coordinates
        fields = ['protein_domain_link_id']

    def validate(self, data):
        # add validation logic for start and stop fields
        domain_data_list = self.initial_data.get('domains')

        for data in domain_data_list:
            start = data.get('start')
            if not start:
                raise serializers.ValidationError(
                    "start field is required in domains.")
            stop = data.get('stop')
            if not stop:
                raise serializers.ValidationError(
                    "stop field is required in domains.")
        return data

    def create(self, validated_data):
        protein_id = self.initial_data.get('protein_id')
        protein_data = proteins.objects.get(protein_id=protein_id)

        domain_data_list = self.initial_data.get('domains')

        domain_coordinate = None  # Initialize the variable

        for data in domain_data_list:
            pfam_data = data['pfam_id']
            domain_data = domains.objects.get(domain_id=pfam_data['domain_id'])
            protein_domain_link_data = protein_domain_link.objects.get(domain_id=domain_data.id,
                                                                       protein_id=protein_data.id)
            protein_domain_link_exists = domain_coordinates.objects.filter(
                protein_domain_link_id=protein_domain_link_data.id).exists()

            if not protein_domain_link_exists:
                # remove unnecessary fields from validated_data
                validated_data.pop('pfam_id', None)
                validated_data.pop('description', None)

                domain_coordinate = domain_coordinates(**{**validated_data,
                                                          'start': data['start'],
                                                          'stop': data['stop'],
                                                          'protein_domain_link_id': protein_domain_link_data.id})
                domain_coordinate.save()

        if domain_coordinate is None:
            raise serializers.ValidationError(
                "Record already exists, Please enter a new record.")
        return domain_coordinate


# end of code I wrote
