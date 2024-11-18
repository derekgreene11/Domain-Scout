# Domain Scout 

## Description

Domain Scout is the primary GUI to view vulnerable domains found by CT Domain Data (see https://derekrgreene.com/ct-data).
CT Domain Data identifies disposable email addresses used as contact methods in WHOIS records. Domains are collected using Certstream Server Go which streams Certificate Transparency logs continuously to a websocket connection. Domains are extracted from the data stream and WHOIS queries are subsequently made to identify contact email addresses which are compared against a list of 15k+ known disposable email domains. If a disposable email address is found, the domain and associated data is added to the database and displayed in Domain Scout.

## Usage

To install the application, run:

`pip install DomainScout`

Run the application

`domainscout`
