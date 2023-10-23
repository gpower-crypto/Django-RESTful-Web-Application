import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .model_factories import *
from .serializers import *

# Create your tests here.

# I wrote this code

# test cases for the API endpoints

class ProteinTest(APITestCase):
    # test case for the protein API endpoint.
    def setUp(self):
        self.protein_id = 'A0A016VK28'
        self.protein = ProteinFactory.create(protein_id=self.protein_id)
        self.protein_sequence = ProteinSequenceFactory.create(protein_id=self.protein_id)
        self.url = reverse('protein_api', kwargs={'id': self.protein_id})

    def test_proteinDetailReturnSuccess(self):
        # test case for checking if the protein detail is returned successfully.
        response = self.client.get(self.url)
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('length' in data)
        self.assertEqual(data['length'], self.protein.length)

    def test_proteinDetailReturnFailureOnBadPk(self):
        # test case for checking if the API returns failure when an invalid protein ID is provided.
        response = self.client.get('api/protein/34')
        self.assertEqual(response.status_code, 404)


class DomainTest(APITestCase):
    # test case for the domain API endpoint.
    def setUp(self):
        self.domain_id = 'PF02931'
        self.domain = DomainFactory.create(domain_id=self.domain_id)
        self.url = reverse('domain_api', kwargs={'id': self.domain_id})

    def test_domainDetailReturnSuccess(self):
        # test case for checking if the domain detail is returned successfully.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('domain_id' in data)
        self.assertEqual(data['domain_id'], self.domain_id)

    def test_domainDetailReturnFailureOnBadPk(self):
        # test case for checking if the API returns failure when an invalid domain ID is provided.
        url = reverse('domain_api', kwargs={'id': 'RT23GH4'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CoverageAPITest(APITestCase):
    # test case for the coverage API endpoint.
    def setUp(self):
        self.protein_id = 'A0A016V7D3'
        self.protein = ProteinFactory.create(protein_id=self.protein_id)
        self.protein_sequence = ProteinSequenceFactory.create(protein_id=self.protein_id)
        self.domain = DomainFactory.create(domain_id='PF00178')
        self.protein_domain_link = ProteinDomainLinkFactory.create(protein=self.protein, domain=self.domain)
        self.domain_coordinates = DomainCoordinateFactory.create(protein_domain_link=self.protein_domain_link)
        self.url = reverse('coverage_api', kwargs={'id': self.protein_id})

    def test_coverageReturnSuccess(self):
        # test case for checking if the coverage is returned successfully.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('coverage' in data)
        expected_coverage = (self.domain_coordinates.stop - self.domain_coordinates.start) / self.protein.length
        self.assertEqual(data['coverage'], expected_coverage)

    def test_coverageReturnFailureOnBadPk(self):
        # test case for checking if the API returns failure when an invalid protein ID is provided.
        url = reverse('coverage_api', kwargs={'id': 'A0A016USI4'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

# test cases for the serializers

class TaxonomySerializerTest(TestCase):
    # test case for the Taxonomy serializer.
    def setUp(self):
        self.taxonomy_data = {
            'taxa_id': 30076,
            'clade': 'E',
            'genus': 'Triatoma',
            'species': 'Infestans',
        }
        self.serializer = TaxonomySerializer(data=self.taxonomy_data)

    def test_valid_data(self):
        # test case for checking if the provided data is valid.
        self.assertTrue(self.serializer.is_valid())

    def test_create_record(self):
        # test case for checking if a taxonomy record is created successfully.
        self.serializer.is_valid()
        taxonomy_record = self.serializer.save()
        self.assertIsInstance(taxonomy_record, taxonomy)
        self.assertEqual(taxonomy_record.taxa_id, str(self.taxonomy_data['taxa_id']))

class ProteinRecordSerialiserTest(APITestCase):
    # test case for the ProteinRecord serializer.
    def setUp(self):
        self.taxonomy_data = {
            'taxa_id': 31953,
            'clade': 'E',
            'genus': 'Ancylostoma',
            'species': 'Ceylanicum',
        }
        self.protein_data = {
            'protein_id': 'A0A016VK28',
            'length': 1374,
            'taxonomy': self.taxonomy_data,
        }
        self.serializer = ProteinRecordSerializer(data=self.protein_data)

    def test_valid_data(self):
        # test case for checking if the provided data is valid.
        self.assertTrue(self.serializer.is_valid())

    def test_create_record(self):
        # test case for checking if a protein record is created successfully.
        self.serializer.is_valid()
        protein_record = self.serializer.save()
        self.assertIsInstance(protein_record, proteins)
        self.assertEqual(protein_record.protein_id, self.protein_data['protein_id'])


class ProteinSequenceSerializerTest(TestCase):
    # test case for the ProteinSequence serializer.
    def setUp(self):
        self.protein_sequence_data = {
            'protein_id': 'A0A016S8J7',
            'sequence': 'MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA',
        }
        self.serializer = ProteinSequenceSerializer(data=self.protein_sequence_data)

    def test_valid_data(self):
        # test case for checking if the provided data is valid.
        self.assertTrue(self.serializer.is_valid())

    def test_create(self):
        # test case for checking if a protein sequence record is created successfully.
        self.serializer.is_valid()
        protein_sequence_record = self.serializer.save()
        self.assertIsInstance(protein_sequence_record, protein_sequence)
        self.assertEqual(protein_sequence_record.sequence, self.protein_sequence_data['sequence'])


class PfamSerializerTest(TestCase):
    # test case for the Pfam serializer.

    def setUp(self):
        self.domain_data = {
            'domain_id': 'PF13639',
            'domain_description': 'Ringfingerdomain',
        }
        self.serializer = PfamSerializer(data=self.domain_data)

    def test_valid_data(self):
        # test case for checking if the provided data is valid.

        self.assertTrue(self.serializer.is_valid())

    def test_create(self):
        # test case for checking if a domain record is created successfully.

        self.serializer.is_valid()
        domain_instance = self.serializer.save()
        self.assertIsInstance(domain_instance, domains)
        self.assertEqual(domain_instance.domain_id, self.domain_data['domain_id'])


class ProteinDomainLinkSerializerTest(TestCase):
    # test case for the ProteinDomainLink serializer.

    def setUp(self):
        taxonomy_record = taxonomy.objects.create(
            taxa_id=4615, clade='E', genus='Ananas', species='Comosus')
        protein = proteins.objects.create(
            protein_id=1, length=736, taxa_id=taxonomy_record.id)

        domain = domains.objects.create(
            domain_id=1, domain_description='C2HE/C2H2/C2HCzinc-bindingfinger', description='Aprataxin C2HE/C2H2/C2HC zinc finger')

        self.protein_domain_link_data = {
            'protein_id': protein.id,
            'domain_id': domain.id,
            'domains': [{
                'pfam_id': {'domain_id': domain.domain_id, 'domain_description': domain.domain_description},
                'description': domain.domain_description,
                'start': 655,
                'stop': 709
            }],
        }

        self.serializer = ProteinDomainLinkSerializer(data=self.protein_domain_link_data)

    def test_valid_data(self):
        # test case for checking if the provided data is valid.

        self.assertTrue(self.serializer.is_valid())

    def test_create(self):
        # test case for checking if a protein-domain link record is created successfully.

        is_valid = self.serializer.is_valid()
        if is_valid:
            protein_domain_link_instance = self.serializer.save()
            self.assertIsInstance(protein_domain_link_instance, protein_domain_link)
            self.assertEqual(protein_domain_link_instance.protein_id, self.protein_domain_link_data['protein_id'])
            self.assertEqual(protein_domain_link_instance.domain_id, self.protein_domain_link_data['domain_id'])


class DomainCoordinateRecordSerializerTest(TestCase):
    # test case for the DomainCoordinateRecord serializer.

    def setUp(self):
        taxonomy_record = taxonomy.objects.create(
            taxa_id=31953, clade='E', genus='Ancylostoma', species='Ceylanicum')
        protein = proteins.objects.create(
            protein_id='A0A016VK28', length=514, taxa_id=taxonomy_record.id)

        domain = domains.objects.create(
            domain_id='PF02204', domain_description='Vacuolar sorting protein 9 (VPS9) domain',
            description='VPS9 domain')

        protein_domain_link_record = protein_domain_link.objects.create(
            protein_id=protein.id, domain_id=domain.id)

        self.domain_coordinate_record_data = {
            'protein_id': protein.protein_id,
            'domains': [{
                'pfam_id': {'domain_id': domain.domain_id, 'domain_description': domain.domain_description},
                'description': domain.domain_description,
                'start': 278,
                'stop': 378
            }],
        }

        self.serializer = DomainCoordinateRecordSerializer(data=self.domain_coordinate_record_data)

    def test_valid_data(self):
        # test case for checking if the provided data is valid.

        self.assertTrue(self.serializer.is_valid())

    def test_create(self):
        # test case for checking if a domain coordinate record is created successfully.

        self.serializer.is_valid()
        domain_coordinate_record_instance = self.serializer.save()
        self.assertIsInstance(domain_coordinate_record_instance, domain_coordinates)
        self.assertEqual(domain_coordinate_record_instance.protein_domain_link.protein.protein_id, self.domain_coordinate_record_data['protein_id'])
# end of code I wrote