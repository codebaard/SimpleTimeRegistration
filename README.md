# SimpleTimeRegistration
Small Flask based Webapp for easy time registration to create invoices, etc.

## Current development stage: Alpha

### Working:
* Register User
* Log In/Out (Session Cookie saved)
* Create and Edit Projects
* Create working hour dataset (Auto + Manual)
* Print recent hours
* Concise overview of particular project

### In Development:
* Export hours as csv
* Safe delete datasets

### Technical Backog
* Time handling: Server vs User vs tzinfo
* Sanitize SQL Input
* Consolidate html-templates
* Refactor naming
* Switch SQLite -> mySQL
* Modular run-config

### Feature Backlog:
* Add label to working hour dataset
* Set parent project for nested structure
* Collaborative projects
* Sleek GUI
* Email verification
* User roles
* Organisations
