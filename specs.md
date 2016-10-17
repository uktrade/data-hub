# Models and specs for Data Hub Backend

Document containing specification for models in Korben and Leeloo, with caveats and required fields.

## Company

| CDMS | Required | Leeloo | Display | Comments |
|:---:|:---:|:---:|:---:|---|
| `Name` | `← * →` | `name` | Registered name | _Companies House name_ **XOR** _CDMS name_ |
| `optevia_Alias` | | `alias` | Trading name | |
| `optevia_CompaniesHouseNumber` | | `company_number` | Companies House number | |
| `optevia_ukorganisation` | `← *` |  | UK based | Inferred property |
| `optevia_BusinessType_Id` | `* →` | `business_type_id` | Type of business | |
| `optevia_Sector_Id` | `← * →` | `sector_id` | Sector | |
| `optevia_Address1` | `← * →` | `registered_address_1` | Address line 1 | |
| `optevia_Address2` | | `registered_address_2` | Address line 2 | |
| `optevia_Address3` | | `registered_address_3` | Address line 3 | |
| `optevia_Address4` | | `registered_address_4` | Address line 4 | |
| `optevia_TownCity` | `← *` | `registered_address_town` | Address town | Korben sends `N/A` in case of no value |
| `optevia_StateCounty` | | `registered_address_county` | Address county | |
| `optevia_PostCode` | | `registered_address_postcode` | Address postcode | |
| `optevia_Country_Id` | `← * →` | `registered_address_country_id` | Address country | |
| | | `trading_address_1` | Address line 1 | If any of the trading address is added, then required fields follow from the above|
| | | `trading_address_2` | Address line 2 | |
| | | `trading_address_3` | Address line 3 | |
| | | `trading_address_4` | Address line 4 | |
| | | `trading_address_town` | Address town | |
| | | `trading_address_county` | Address county | |
| | | `trading_address_postcode` | Address postcode | |
| | | `trading_address_country_id` | Address country | |
| | | `account_manager_id` | Agreed account manager | |
| | | `export_to_countries` | Export market | Django M2M |
| | | `future_interest_contires` | Future contries of interest | Django M2M |

### Company address display preferences

The order of preference for *registered address* is as follows:

 - Companies House registered address
 - CDMS “registered” address

There is only one source for *trading address*, that is Data Hub.

## Contact

| CDMS | Required | Leeloo | Display | Comments |
|:---:|:---:|:---:|:---:|---|
| `Title` | `* →` | `title_id` | Title | |
| `FirstName` | `← * →` | `first_name` | First name(s) | |
| `LastName` | `← * →` | `last_name` | Last name | |
| `MiddleName` | | | | Data migration case |
| `optevia_LastVerified` | `← *` | | | Korben should add current date on write |
| `ParentCustomerId_Id` | `← * →` | `company_id` | Company | |
| `optevia_PrimaryContact` | `* →` | `primary` | Is primary contact | |
| | `* →` | `teams` | Teams | Django M2M |
| `optevia_CountryCode` | `← * →` | `telephone_countrycode` | Telephone country code | |
| `optevia_AreaCode` `++` `optevia_TelephoneNumber` | `← * →` | `telephone_number` | Telephone number | Korben to fill area code |
| `EMailAddress1` | `← * →` | `email` | Email address | |
| `optevia_Address1` | `← *` | `address_1` | Address line 1 | |
| `optevia_Address2` | | `address_2` | Address line 2 | |
| `optevia_Address3` | | `address_3` | Address line 3 | |
| `optevia_Address4` | | `address_4` | Address line 4 | |
| `optevia_TownCity` | `← *` | `address_town` | Address town | Korben sends `N/A` |
| `optevia_StateCounty` | | `address_county` | Address county | |
| `optevia_PostCode` | | `address_postcode` | Address postcode | |
| `optevia_Country_Id` | `← *` | `address_country_id` | Address country | |
| | `* →` | `address_same_as_company` | Address same as company | Leeloo to send company address if this is set to true |
| `optevia_UKRegion_Id` | `← * →` | `uk_region_id` | UK region |
| | | `telephone_alternative` | Alternative telephone | |
| | | `email_alternative` | Alternative email address | |

## Interaction

| CDMS | Required | Leeloo | Display | Comments |
|:---:|:---:|:---:|:---:|---|
| `optevia_InteractionCommunicationChannel_Id` | `← * →` | `interaction_type_id` | Interaction type | Test values may appear on CDMS side |
| `Subject` | `← * →` | `subject` | Subject | |
| `ActualStart` | `← * →` | `date_of_interaction` | Date of interaction | Question if `ActualStart` populates CDMS front end properly |
| `optevia_Advisor_Id` | `← * →` | `advisor_id` | DIT advisor | |
| `optevia_Contact_Id` | `← * →` | `contact_id` | Company contact | |
| `optevia_Organisation_Id` | `← * →` | `company_id` | Automated in leeloo (from advisor data) | |
| `optevia_Notes` | `* →` | `notes` | | |
| `optevia_ServiceProvider_Id` | `← *` | `service_provider_id` | Service provider | Defaults to advisor team in Leeloo |
| `optevia_Service_Id` | `← * →` | `service_id` | Service | |
