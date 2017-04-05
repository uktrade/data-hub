# Data Hub CRM Company API

The accompanying file in this directory - company.yaml - describes the functionality of the APIs associated with teh Company data type in Data Hub CRM.

Data Hub CRM has two differing but related data types for dealing with companies. The native Company object describes a Company that exists within the CRM - that is, it has been created by a Data Hub user. The other type is a Companies House Company, which, as the name suggests, is a company that exists within the Companies House database.

It's the policy of Data Hub CRM that a Company with a UK registration cannot be created unless it is associated with its Companies House data. Companies House Companies are therefore only ever used in two modes - one is as a search result, which belongs to the Search API - and the other is as related data to a native Company object.

Data Hub Company objectsm however, do not always have Companies House Companies associated with them. Not all Data Hub Companies are UK registered, so CH data would not cover them. Also, the system Data Hub CRM replaces, CDMS, did not integrate with Companies House, so many UK companies in the legacy data are orphaned.

This API allows the user to retrieve a single company, modify it, or create a new company entry. It also allows the user to view the linked Companbies House data.

## Limitations

Although there is a GET /company/{companyId} operation, there is no matching GET /companies operation. The company data sets are huge, so the only way to retrieve a tractable numnber of companies is through a filter, which therefore belongs in the Search API. When the Search API is upgraded to V2 it will use the same definitions as are found here.

## Technical details

The company.yaml file is a Swagger 2.0 specification that generates a JSON API payload and describes JSON API behaviours. Swagger lacks the tools to describe the semantics of JSON API in detail, so the reader is advised to use the Example: data included for each object as a guide to the expected behaviour.