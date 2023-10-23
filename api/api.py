from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# I wrote this code


@api_view(['GET'])
def taxonomy_detail(request, id):
    # fetch taxonomy details based on the provided taxa ID
    detail = (request.path_info)

    try:
        taxonomy_data = taxonomy.objects.get(taxa_id=id)
        protein_data = proteins.objects.filter(taxa=taxonomy_data.id)

    except taxonomy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if 'proteins' in detail:
        # fetch related proteins and their domain information
        protein_list = list()
        for record in protein_data:
            protein_domain_data = protein_domain_link.objects.filter(
                protein=record.id)
            for domain_record in protein_domain_data:
                protein_list.append(DomainIdSerializer(domain_record.domain).data |
                                    OrganismProteinSerializer(domain_record).data)

        return Response(protein_list)

    if 'pfams' in detail:
        # fetch related proteins and their pfam domain details
        pfam_detail_list = list()
        for record in protein_data:
            protein_domain_data = protein_domain_link.objects.filter(
                protein=record.id)
            for domain_record in protein_domain_data:
                pfam_detail_list.append(DomainIdSerializer(domain_record.domain).data |
                                        {'pfam': PfamSerializer(domain_record.domain).data})

        return Response(pfam_detail_list)

@api_view(['POST'])
def add_record (request):
    # handle adding a new record

     if request.method == 'POST':
        # process the data and saves it if all serializers are valid
        serializers = [
            ProteinSequenceSerializer(data=request.data),
            ProteinRecordSerializer(data=request.data),
            ProteinDomainLinkSerializer(data=request.data),
            DomainCoordinateRecordSerializer(data=request.data)
        ]

        if all(serializer.is_valid() for serializer in serializers):
            for serializer in serializers:
                serializer.save()

            return Response(request.data, status=status.HTTP_201_CREATED)

        errors = [
            serializer.errors for serializer in serializers if not serializer.is_valid()]
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def protein_detail(request, id):
    # handle fetching protein details for the provided protein ID

    if request.method == 'GET':
        # fetch protein details and related data
        try:
            protein_data = proteins.objects.get(protein_id=id)
            sequence_data = protein_sequence.objects.get(protein_id=id)

        except (proteins.DoesNotExist, protein_sequence.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        taxonomy_data = taxonomy.objects.get(taxa_id=protein_data.taxa)
        protein_domain_link_data = protein_domain_link.objects.filter(
            protein=protein_data.id)

        domain_data_list = list()

        protein_sequence_serializer = ProteinSequenceSerializer(
            sequence_data).data
        taxonomy_serializer = TaxonomySerializer(taxonomy_data).data
        protein_serializer = ProteinSerializer(protein_data).data

        for record in protein_domain_link_data:
            domain_data = domains.objects.get(domain_id=record.domain)
            domain_coordinates_data = domain_coordinates.objects.get(
                protein_domain_link=record.id)

            domain_data_list.append({'pfam_id': PfamSerializer(domain_data).data} |
                                    DomainSerializer(domain_data).data |
                                    DomainCoordinateSerializer(domain_coordinates_data).data)

        json_data = protein_sequence_serializer | {
            'taxonomy': taxonomy_serializer} | protein_serializer | {'domains': domain_data_list}

        return Response(json_data)


@api_view(['GET'])
def pfam_detail(request, id):
    # fetch pfam domain details for the provided domain ID
    try:
        domain_data = domains.objects.get(domain_id=id)

    except domains.DoesNotExist:
        return Response(status=404)

    serializer = PfamSerializer(domain_data).data
    return Response(serializer)


@api_view(['GET'])
def coverage(request, id):
    # Calculates the protein coverage for the provided protein ID
    try:
        protein_data = proteins.objects.get(protein_id=id)

    except proteins.DoesNotExist:
        return Response(status=404)

    protein_domain_link_data = protein_domain_link.objects.filter(
        protein=protein_data.id)
    coverage = 0

    for record in protein_domain_link_data:
        domain_coordinates_data = domain_coordinates.objects.get(
            protein_domain_link=record.id)
        coverage += abs(domain_coordinates_data.start -
                        domain_coordinates_data.stop)/protein_data.length

    return Response({"coverage": coverage})

# end of code I wrote
