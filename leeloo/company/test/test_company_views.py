import pytest
from django.conf import settings
from django.core.exceptions import ValidationError

from django.urls import reverse
from rest_framework import status

from core import constants
from core.test_utils import LeelooTestCase
from es.services import document_exists
from es.utils import get_elasticsearch_client

from company import models
from .factories import CompanyFactory, CompaniesHouseCompanyFactory


class CompanyTestCase(LeelooTestCase):

    def test_list_companies(self):
        """List the companies."""

        CompanyFactory()
        CompanyFactory()
        url = reverse('company-list')
        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

    def test_detail_company_with_company_number(self):
        """Test company detail view with companies house data.

        Make sure that the registered name and registered address are coming from CH data
        """

        ch_company = CompaniesHouseCompanyFactory(
            company_number=123,
            name='Foo ltd.',
            registered_address_1='Hello st.',
            registered_address_town='Fooland',
            registered_address_country_id=constants.Country.united_states.value.id
        )
        company = CompanyFactory(
            company_number=123,
            name='Bar ltd.',
            alias='Xyz trading'
        )

        url = reverse('company-detail', kwargs={'pk': company.id})
        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(company.pk)
        assert response.data['companies_house_data']
        assert response.data['companies_house_data']['id'] == ch_company.id
        assert response.data['name'] == ch_company.name
        assert response.data['trading_name'] == company.alias
        assert response.data['registered_address'] == {
            'address_1': ch_company.registered_address_1,
            'address_2': None,
            'address_3': None,
            'address_4': None,
            'address_town': ch_company.registered_address_town,
            'address_country': str(ch_company.registered_address_country.pk),
            'address_county': None,
            'address_postcode': None,
        }

    def test_detail_company_without_company_number(self):
        """Test company detail view without companies house data.

        Make sure that the registered name and address are coming from CDMS.
        """

        company = CompanyFactory(
            name='Foo ltd.',
            registered_address_1='Hello st.',
            registered_address_town='Fooland',
            registered_address_country_id=constants.Country.united_states.value.id
        )

        url = reverse('company-detail', kwargs={'pk': company.id})
        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(company.pk)
        assert response.data['companies_house_data'] is None
        assert response.data['name'] == company.name
        assert response.data['registered_address'] == {
            'address_1': company.registered_address_1,
            'address_2': None,
            'address_3': None,
            'address_4': None,
            'address_town': company.registered_address_town,
            'address_country': str(company.registered_address_country.pk),
            'address_county': None,
            'address_postcode': None,
        }

    def test_update_company(self):
        """Test company update."""

        company = CompanyFactory(
            name='Foo ltd.',
            registered_address_1='Hello st.',
            registered_address_town='Fooland',
            registered_address_country_id=constants.Country.united_states.value.id
        )

        # now update it
        url = reverse('company-detail', kwargs={'pk': company.pk})
        response = self.api_client.patch(url, {
            'name': 'Acme',
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Acme'

        # make sure we're writing to ES
        es_client = get_elasticsearch_client()
        es_result = es_client.get(
            index=settings.ES_INDEX,
            doc_type='company_company',
            id=response.data['id'],
            realtime=True
        )
        assert es_result['_source']['name'] == 'Acme'

    def test_add_uk_company(self):
        """Test add new UK company."""

        url = reverse('company-list')
        response = self.api_client.post(url, {
            'name': 'Acme',
            'alias': None,
            'business_type': constants.BusinessType.company.value.id,
            'sector': constants.Sector.aerospace_assembly_aircraft.value.id,
            'registered_address_country': constants.Country.united_kingdom.value.id,
            'registered_address_1': '75 Stramford Road',
            'registered_address_town': 'London',
            'uk_region': constants.UKRegion.england.value.id
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Acme'

        # make sure we're writing to ES
        es_client = get_elasticsearch_client()
        assert document_exists(
            client=es_client,
            doc_type='company_company',
            document_id=response.data['id']
        )

    def test_add_uk_company_without_uk_region(self):
        """Test add new UK without UK region company."""

        url = reverse('company-list')
        with pytest.raises(ValidationError) as error:
            response = self.api_client.post(url, {
                'name': 'Acme',
                'alias': None,
                'business_type': constants.BusinessType.company.value.id,
                'sector': constants.Sector.aerospace_assembly_aircraft.value.id,
                'registered_address_country': constants.Country.united_kingdom.value.id,
                'registered_address_1': '75 Stramford Road',
                'registered_address_town': 'London',
            })

        assert 'UK region is required for UK companies.' in str(error.value)

    def test_add_not_uk_company(self):
        """Test add new not UK company."""

        url = reverse('company-list')
        response = self.api_client.post(url, {
            'name': 'Acme',
            'alias': None,
            'business_type': constants.BusinessType.company.value.id,
            'sector': constants.Sector.aerospace_assembly_aircraft.value.id,
            'registered_address_country': constants.Country.united_states.value.id,
            'registered_address_1': '75 Stramford Road',
            'registered_address_town': 'London',
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Acme'

        # make sure we're writing to ES
        es_client = get_elasticsearch_client()
        assert document_exists(
            client=es_client,
            doc_type='company_company',
            document_id=response.data['id']
        )

    def test_add_company_partial_trading_address(self):
        """Test add new company with partial trading address."""

        url = reverse('company-list')

        with pytest.raises(ValidationError) as error:
            self.api_client.post(url, {
                'name': 'Acme',
                'business_type': constants.BusinessType.company.value.id,
                'sector': constants.Sector.aerospace_assembly_aircraft.value.id,
                'registered_address_country': constants.Country.united_kingdom.value.id,
                'registered_address_1': '75 Stramford Road',
                'registered_address_town': 'London',
                'trading_address_1': 'test',
                'uk_region': constants.UKRegion.england.value.id
            })

        assert 'If a trading address is specified, it must be complete.' in str(error.value)

    def test_add_company_with_trading_address(self):
        """Test add new company with trading_address."""

        url = reverse('company-list')
        response = self.api_client.post(url, {
            'name': 'Acme',
            'business_type': constants.BusinessType.company.value.id,
            'sector': constants.Sector.aerospace_assembly_aircraft.value.id,
            'registered_address_country': constants.Country.united_kingdom.value.id,
            'registered_address_1': '75 Stramford Road',
            'registered_address_town': 'London',
            'trading_address_country': constants.Country.ireland.value.id,
            'trading_address_1': '1 Hello st.',
            'trading_address_town': 'Dublin',
            'uk_region': constants.UKRegion.england.value.id
        })

        assert response.status_code == status.HTTP_201_CREATED

        # make sure we're writing to ES
        es_client = get_elasticsearch_client()
        assert document_exists(
            client=es_client,
            doc_type='company_company',
            document_id=response.data['id']
        )

    def test_archive_company_no_reason(self):
        """Test company archive."""

        company = CompanyFactory()
        url = reverse('company-archive', kwargs={'pk': company.id})
        response = self.api_client.post(url)

        assert response.data['archived']
        assert response.data['archived_reason'] == ''
        assert response.data['id'] == str(company.id)

        # make sure we're writing to ES
        es_client = get_elasticsearch_client()
        es_result = es_client.get(
            index=settings.ES_INDEX,
            doc_type='company_company',
            id=response.data['id'],
            realtime=True
        )
        assert es_result['_source']['archived']
        assert es_result['_source']['archived_reason'] == ''
    
    def test_archive_company_reason(self):
        """Test company archive."""

        company = CompanyFactory()
        url = reverse('company-archive', kwargs={'pk': company.id})
        response = self.api_client.post(url, {'reason': 'foo'})

        assert response.data['archived']
        assert response.data['archived_reason'] == 'foo'
        assert response.data['id'] == str(company.id)

        # make sure we're writing to ES
        es_client = get_elasticsearch_client()
        es_result = es_client.get(
            index=settings.ES_INDEX,
            doc_type='company_company',
            id=response.data['id'],
            realtime=True
        )
        assert es_result['_source']['archived']
        assert es_result['_source']['archived_reason'] == 'foo'


class CHCompanyTestCase(LeelooTestCase):

    def test_list_ch_companies(self):
        """List the companies house companies."""

        CompaniesHouseCompanyFactory()
        CompaniesHouseCompanyFactory()

        url = reverse('companieshousecompany-list')
        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] ==  models.CompaniesHouseCompany.objects.all().count()

    def test_detail_ch_company(self):
        """Test companies house company detail."""

        ch_company = CompaniesHouseCompanyFactory(company_number=123)

        url = reverse('companieshousecompany-detail', kwargs={'company_number': ch_company.company_number})
        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == ch_company.id

    def test_ch_company_cannot_be_written(self):
        """Test CH company POST is not allowed."""

        url = reverse('companieshousecompany-list')
        response = self.api_client.post(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_promote_a_ch_company(self):
        """Promote a CH company to full company, ES should be updated correctly."""

        ch_company = CompaniesHouseCompanyFactory(company_number=1234567890)

        # make sure it's in ES
        es_client = get_elasticsearch_client()

        assert document_exists(
            client=es_client,
            doc_type='company_companieshousecompany',
            document_id=ch_company.pk
        )

        # promote a company to ch

        url = reverse('company-list')
        response = self.api_client.post(url, {
            'name': 'Acme',
            'company_number': 1234567890,
            'business_type': constants.BusinessType.company.value.id,
            'sector': constants.Sector.aerospace_assembly_aircraft.value.id,
            'registered_address_country': constants.Country.united_kingdom.value.id,
            'registered_address_1': '75 Stramford Road',
            'registered_address_town': 'London',
            'trading_address_country': constants.Country.ireland.value.id,
            'trading_address_1': '1 Hello st.',
            'trading_address_town': 'Dublin',
            'uk_region': constants.UKRegion.england.value.id
        })

        assert response.status_code == status.HTTP_201_CREATED

        assert not document_exists(
            client=es_client,
            doc_type='company_companieshousecompany',
            document_id=ch_company.pk
        )

        assert document_exists(
            client=es_client,
            doc_type='company_company',
            document_id=response.data['id']
        )
