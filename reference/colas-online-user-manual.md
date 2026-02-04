# COLAs Online 3.11.3 Public COLA Registry User Manual

**U.S. Department of the Treasury**
**Alcohol and Tobacco Tax and Trade Bureau (TTB)**
1310 G Street NW., Box 12
Washington, D.C. 20005

Prepared by: Office of the Chief Information Officer
TTB RFC# TTB-2015-0124-MOD1

FOR OFFICIAL USE ONLY
Dated: June 11, 2015

---

## Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 08/03/2010 | A. Sharifi | Initial Version |
| 1.1 | 08/17/2010 | A. Sharifi | Performed minor format and edit |
| 1.2 | 09/01/2010 | A. Sharifi | Incorporated comments from internal review |
| 1.3 | 09/10/2010 | A. Sharifi | Performed minor format and edit |
| 1.4 | 11/02/2010 | A. Sharifi | Performed minor format and edit |
| 1.5 | 01/14/2011 | A. Sharifi | Updated based on fixes to COLAs Online |
| 2.0 | 06/07/2011 | A. Sharifi | Updated for COLAs Online 3.5 |
| 2.1 | 06/10/2011 | A. Sharifi | Incorporated comments from internal review |
| 3.0 | 09/22/2011 | A. Sharifi | Updated for COLAs Online 3.5.2 |
| 4.0 | 03/02/2012 | A. Sharifi | Updated for COLAs Online 3.6 |
| 5.0 | 06/12/2012 | A. Sharifi | Updated for COLAs Online 3.7 |
| 5.1 | 06/15/2012 | A. Sharifi | Incorporated comments from internal review |
| 6.0 | 10/05/2012 | A. Sharifi | Updated for COLAs Online 3.8 |
| 7.0 | 04/04/2013 | A. Sharifi | Updated for COLAs Online 3.9 |
| 7.1 | 04/11/2013 | A. Sharifi | Performed minor format and edit |
| 7.2 | 05/03/2013 | A. Sharifi | Performed minor format and edit |
| 7.3 | 06/10/2013 | A. Sharifi | Updated for COLAs Online 3.9.1 |
| 7.4 | 07/29/2013 | A. Sharifi | Performed minor format and edit |
| 8.0 | 08/16/2013 | A. Sharifi | Updated for COLAs Online 3.10 |
| 8.1 | 09/05/2013 | A. Sharifi | Performed minor format and edit |
| 9.0 | 10/21/2013 | A. Sharifi | Updated for COLAs Online 3.10.1 |
| 9.1 | 11/01/2013 | A. Sharifi | Updated for TTB Portal changes |
| 9.2 | 11/14/2013 | A. Sharifi | Updated for TTB Contact Us changes |
| 9.3 | 12/13/2013 | A. Sharifi | Updated for TTB Contact Us changes |
| 10.0 | 06/09/2014 | A. Sharifi | Updated for COLAs Online 3.11 |
| 11.0 | 06/05/2015 | A. Sharifi | Updated for COLAs Online 3.11.3 |
| 11.1 | 06/11/2015 | A. Sharifi | Incorporated comments from internal review |

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [Background](#11-background)
   - 1.2 [Purpose and Scope](#12-purpose-and-scope)
   - 1.3 [Organization of the User Manual](#13-organization-of-the-user-manual)
   - 1.4 [Glossary](#14-glossary)
2. [System Capabilities](#2-system-capabilities)
   - 2.1 [General Description](#21-general-description)
   - 2.2 [Privacy Act Considerations](#22-privacy-act-considerations)
3. [System Functions](#3-system-functions)
   - 3.1 [System Basics](#31-system-basics)
   - 3.2 [Getting Started – Using the TTB Online Portal Page](#32-getting-started--using-the-ttb-online-portal-page)
   - 3.3 [Public COLA Registry Menu Options](#33-public-cola-registry-menu-options)
   - 3.4 [Search the Registry](#34-search-the-registry)
   - 3.5 [Printable Version of COLA](#35-printable-version-of-cola)
4. [Help Facilities](#4-help-facilities)

**Appendices**
- [Appendix A: Definition of Terms](#appendix-a-definition-of-terms)
- [Index](#index)

---

## List of Figures

| Figure | Description | Page |
|--------|-------------|------|
| Figure 1 | Privacy Policy | 5 |
| Figure 2 | Privacy Impact Assessments | 6 |
| Figure 3 | Privacy Impact Assessment (COLAs Online) | 7 |
| Figure 4 | TTB Online Portal | 8 |
| Figure 5 | Public COLA Registry Basic Search | 9 |
| Figure 6 | Public COLA Registry Menu Options | 10 |
| Figure 7 | Public COLA Registry Basic Search | 11 |
| Figure 8 | COLAs Online FAQs | 12 |
| Figure 9 | Contact Us | 13 |
| Figure 10 | Public COLA Registry Online Help | 15 |
| Figure 11 | Public COLA Registry User Manual | 16 |
| Figure 12 | TTB Online Portal | 17 |
| Figure 13 | Public COLA Registry Basic Search | 19 |
| Figure 14 | Product/Class Type Lookup | 21 |
| Figure 15 | Show All Codes (Product Class/Type Codes) | 22 |
| Figure 16 | Origin Code Lookup | 23 |
| Figure 17 | Show All Codes (Origin Codes) | 24 |
| Figure 18 | Public COLA Registry Advanced Search (Top) | 25 |
| Figure 19 | Public COLA Registry Advanced Search (Bottom) | 26 |
| Figure 20 | Vendor Code Lookup | 28 |
| Figure 21 | Search Results: COLAs (Top) | 30 |
| Figure 22 | Search Results: COLAs (Bottom) | 31 |
| Figure 23 | COLA Detail (Top) | 33 |
| Figure 24 | COLA Detail (Bottom) | 34 |
| Figure 25 | Printable E-filed COLA (Top) | 35 |
| Figure 26 | Printable E-filed COLA (Bottom) | 36 |
| Figure 27 | Printable Paper Filed COLA | 37 |

---

## List of Tables

| Table | Description | Page |
|-------|-------------|------|
| Table 1 | Manual Organization | 2 |
| Table 2 | Manual Conventions | 2 |
| Table 3 | Acronyms and Terms | 2 |

---

## 1 Introduction

This Public COLA Registry User Manual provides information on how to operate the Public Certificate of Label Approval (COLA) Registry for public users. The Public COLA Registry will enable a user to view approved, expired, surrendered, and revoked COLAs. This document is written on behalf of the Advertising, Labeling and Formulation Division (ALFD), Office of the Chief Information Officer (OCIO), Alcohol and Tobacco Tax and Trade Bureau (TTB).

This section provides information on the project background, project objectives, and points of contact, as well as the document organization and conventions.

### 1.1 Background

**TTB Mission:**
- Collect alcohol, tobacco, firearms, and ammunition taxes
- Ensure that alcohol beverages are labeled, advertised and marketed in accordance with the law
- Administer the laws and regulations in a manner that protects the revenue, protects the consumer, and promotes voluntary compliance

**ALFD Mission:**
- Ensure the proper tax classification of alcohol beverages
- Ensure that formulas, labels, and advertisements for alcohol beverages are in compliance with Federal laws and regulations
- Ensure that labels provide consumers with adequate information on the identity and quality of alcohol beverage products
- Prevent consumer deception
- Educate and provide guidance to industry and the public on laws, regulations, and activities regarding ALFD's mission and functions

### 1.2 Purpose and Scope

The purpose of the Public COLA Registry User Manual is to provide a brief understanding of how to operate and navigate through the Public COLA Registry.

The Public COLA Registry is used by Industry Members (IM), Industry Representatives and the general public to view information on approved, expired, surrendered, and revoked COLAs, as required by law. The public module of the COLAs Online system requires no user name and password and contains, as required by the Freedom of Information Act (FOIA), details of only approved, expired, surrendered, or revoked COLAs for viewing by the general public, as well as a printable version of the COLA if available.

This manual discusses who should use this manual and reviews the menu options, screens available and step-by-step procedures for the system interfaces.

This manual is intended to provide information on how to use the system for the public users of the Public COLA Registry.

### 1.3 Organization of the User Manual

**Table 1: Manual Organization**

| Section Number | Section Title | Description |
|----------------|---------------|-------------|
| 1 | Introduction | Provides information on the project background, as well as the document organization and conventions |
| 2 | System Capabilities | Provides an overview of the Public COLA Registry system and its capabilities |
| 3 | System Functions | Describes each specific function including step-by-step procedures for using the function |
| 4 | Help Facilities | Discusses the help facilities provided to users of the Public COLA Registry system |
| Appendix A | Definition of Terms | Defines important terms used in the Public COLA Registry system |

#### 1.3.1 Conventions of the User Manual

**Table 2: Manual Conventions**

| Convention | Description |
|------------|-------------|
| **Bold** | Bold text indicates a button or key label |
| ►Note: | Indicates a note or message to the user |
| 1. Numbered List | Numbered lists provide step-by-step procedures for performing an action |
| • Bulleted List | Bulleted lists provide information, not procedural steps |
| Link | Indicates a link to a specific application or web page |
| ❓ | Question Mark – field-level help |

### 1.4 Glossary

**Table 3: Acronyms and Terms**

| Acronym / Term | Description |
|----------------|-------------|
| ALFD | Advertising, Labeling and Formulation Division |
| COLA | Certificate of Label Approval |
| COLAs Online | Certificate of Label Approval System |
| FAQs | Frequently Asked Questions |
| FOIA | Freedom of Information Act |
| FONL | Formulas Online |
| IM | Industry Member |
| OIM | Online Industry Member |
| NRC | National Revenue Center |
| PIA | Privacy Impact Assessment |
| PCR | Public COLA Registry |
| SDLC | Systems Development Life Cycle |
| TTB | Alcohol and Tobacco Tax and Trade Bureau |

---

## 2 System Capabilities

This section provides an overview of the Public COLA Registry system and its capabilities.

### 2.1 General Description

The following functions are provided to general public users of the Public COLA Registry system:

- Search for and view approved, expired, revoked, or surrendered COLAs
- Save search results to a .csv file (viewable through Microsoft Excel or other associated application)
- View COLA Details (only limited data fields available as public information via the FOIA)
- Display and print completed COLA forms (approved, expired, revoked, or surrendered)
- View COLAs Online Frequently Asked Questions (FAQs)
- Report problems and contact ALFD Customer Service

### 2.2 Privacy Act Considerations

The TTB privacy policy is described in the Privacy Policy page linked on the TTB Online Portal page and on the Public COLA Registry entry point, the Public COLA Registry Basic Search page. The TTB privacy impact assessment (PIA) is available in the Privacy Impact Assessments page linked on the TTB Online Portal page and on the Public COLA Registry entry point, the Public COLA Registry Basic Search page.

#### Figure 1: Privacy Policy

> *[Screenshot: TTB.gov website showing the Privacy Policy and Legal Notice page. The page displays the TTB header with navigation tabs (HOME, TTB FOR..., RESOURCES, TOOLS/TUTORIALS, FILING/PAYMENTS, REGULATIONS/GUIDANCE, ABOUT TTB). Below is the "About TTB" section header followed by "Privacy Policy and Legal Notice" with a numbered list of 11 topics: 1. Privacy Policy Summary, 2. Email, 3. Sending Personal Information, 4. Comments, 5. Information Collection, 6. Cookies, 7. Site Security, 8. Links to Other Sites, 9. Disclaimer of Endorsement, 10. Copyright, 11. Official Seal, Names, and Symbols. The Privacy Policy Summary section explains that the Privacy Act of 1974 protects privacy rights and that TTB respects visitor privacy, does not collect personal information, and only uses voluntarily provided information for its stated purpose.]*

#### Figure 2: Privacy Impact Assessments

> *[Screenshot: TTB.gov Freedom of Information Act (FOIA) page showing Privacy Impact Assessments (PIA). The page explains that PIA is a process to determine the risk of collecting, managing, and disseminating identifiable information electronically. A list of TTB systems with PIAs includes: Automated Commercial Systems, Auto Audit, Caliber, Chief Counsel Management System, Certificate of Label Approval Formula Modernization Laboratory, Certificate of Label Approval Online (COLA), Dimensions, Federal Excise Tax, Formulas Online, Integrated Revenue Information System, Laboratory Information Management System, Network Infrastructure GSS, Permits Online, Regulatory Major Application System, Rockville Laboratory Imaging System, Special Occupational Tax/Floor Stocks Tax, Sunflower System, Tax Major Application, TLC Library Solutions, TTBDocs. On the right side is a statistics table showing TTB Annual Report Statistics for Initial Requests by year (2004-2013) with Received, Processed, and Pending columns. Also shown: Most Requested items and "HOW DO I...?" section.]*

#### Figure 3: Privacy Impact Assessment (COLAs Online)

> *[Screenshot: A formal document titled "Alcohol and Tobacco Tax and Trade Bureau - Certificate of Label Approval Online (COLAs Online) - Privacy Impact Assessment." The document has two main sections visible: "Information Collected and Purpose" - explaining that COLAs Online is a web-based application facilitating the submission and review process for alcohol beverage labels (TTB Form 5100.31, OMB Number 1513-0020), providing an expedient and paperless means of obtaining Federal label approval. It authorizes certificate holders to bottle and remove or import alcohol beverages with labels identical to those on the Certificate. The system facilitates electronic applications and interfaces with other strategic systems including IRIS for permit, registry, and other authorized data. It stores Personally Identifiable Information (PII) only from submitted applications. "Information Use and Sharing" section begins to explain that COLAs Online stores names and phone numbers of those who provided information on COLA applications.]*

**Government Warning:**

> WARNING! THIS SYSTEM IS THE PROPERTY OF THE UNITED STATES DEPARTMENT OF TREASURY. UNAUTHORIZED USE OF THIS SYSTEM IS STRICTLY PROHIBITED AND SUBJECT TO CRIMINAL AND CIVIL PENALTIES. THE DEPARTMENT MAY MONITOR, RECORD, AND AUDIT ANY ACTIVITY ON THE SYSTEM AND SEARCH AND RETRIEVE ANY INFORMATION STORED WITHIN THE SYSTEM. BY ACCESSING AND USING THIS COMPUTER YOU ARE AGREEING TO ABIDE BY THE TTB RULES OF BEHAVIOR, AND ARE CONSENTING TO SUCH MONITORING, RECORDING, AND INFORMATION RETRIEVAL FOR LAW ENFORCEMENT AND OTHER PURPOSES. USERS SHOULD HAVE NO EXPECTATION OF PRIVACY WHILE USING THIS SYSTEM.

---

## 3 System Functions

This section describes each specific system function of the Public COLA Registry system.

### 3.1 System Basics

This section discusses all of the basic information needed to start using the system. This section includes the following information:

- **Getting Started – Using the TTB Online Portal Page** – See Section 3.2
- **Public COLA Registry Menu Options** – See Section 3.3
- **Search the Registry** – See Section 3.4
- **Print Filed COLAs** – See Section 3.5

### 3.2 Getting Started – Using the TTB Online Portal Page

You may access the Public COLA Registry through the TTB Online Portal page.

#### Figure 4: TTB Online Portal

> *[Screenshot: TTBONLINE.GOV portal page with TTB logo and "ALCOHOL AND TOBACCO TAX AND TRADE BUREAU, U.S. DEPARTMENT OF THE TREASURY" header. The page has a horizontal navigation bar with five links: REGISTER, HOW TO REGISTER, PUBLIC COLAS REGISTRY, FAQ, CONTACT US. Below is a login section titled "Already registered? Log in:" with fields for User Name (with "Expired password?" link) and Password (with "New or forgotten password?" link). Two login buttons appear: "COLAs Online" and "Formulas Online". A yellow notice box warns about pop-up blockers and provides links to check processing times for label applications and beverage formula applications, plus a link to check status of individual applications. At the bottom: PRIVACY POLICY and PRIVACY IMPACT ASSESSMENT links, a disclaimer about TTB data accuracy, accessibility information, screen resolution recommendations (1280x800), TTB PORTAL Version 1.5.07, and the full government warning about unauthorized system use.]*

#### Figure 5: Public COLA Registry Basic Search

> *[Screenshot: The COLA Registry search interface with TTB header banner ("ALCOHOL AND TOBACCO TAX AND TRADE BUREAU, U.S. Department of the Treasury") and American flag graphic. Left side shows "COLA Registry - ALCOHOL AND TOBACCO TAX AND TRADE BUREAU" branding with a link to "TTB F 5100.31: Application For and Certification/Exemption of Label/Bottle Approval". Right side has a menu box with links: Search Public COLA Registry, COLAs Online FAQs, Contact Us, Public COLA Registry Manual, Download Public COLA Registry Manual, COLAs Online Logon. Below is "Search for COLAs" section with a note about generic searches and date parameters. The form shows "Basic Search | Advanced Search" tabs, with "Basic Search Criteria" fields including: Date Completed (From: 7/01/2013 To: 08/05/2013 in MM/DD/YYYY format with calendar icons), Product Name text field with radio buttons for "Brand Name / Fanciful Name / Either", Product Class/Type range fields with "Lookup Class Type>" button, Origin Code field with "Lookup Origin>" button. Bottom has "Clear and Start Over" and "Search" buttons, plus Privacy Policy and Privacy Impact Assessment links.]*

#### 3.2.1 Access the Public COLA Registry

Follow these steps to access the Public COLA Registry through the TTB Online Portal page:

1. Open your Internet Explorer web browser.
2. Enter `https://www.ttbonline.gov/` in the address field.
3. Press the **Enter** key. The TTB Online Portal page displays. See Figure 4.
4. Select the **Public COLAS Registry** link. The Public COLA Registry entry point, the Public COLA Registry Basic Search page, displays. See Figure 5.

### 3.3 Public COLA Registry Menu Options

The Public COLA Registry menu options are available in the menu box in the upper right of every page.

#### Figure 6: Public COLA Registry Menu Options

> *[Screenshot: A menu box with dark blue header, containing the following links with arrow bullets:
> - Search Public COLA Registry
> - COLAs Online FAQs
> - Contact Us
> - Public COLA Registry Manual
> - Download Public COLA Registry Manual
> - COLAs Online Logon]*

The following menu options are available in the Public COLA Registry:

- **Search Public COLA Registry** – See Section 3.3.1
- **COLAs Online FAQs** – See Section 3.3.2
- **Contact Us** – See Section 3.3.3
- **Public COLA Registry Manual** – See Section 3.3.4
- **Download Public COLA Registry Manual** – See Section 3.3.5
- **COLAs Online Logon** – See Section 3.3.6

#### 3.3.1 Search Public COLA Registry

The Search Public COLA Registry menu option allows you to search for approved, expired, revoked, and surrendered COLAs.

#### Figure 7: Public COLA Registry Basic Search

> *[Screenshot: Same as Figure 5 - The full COLA Registry Basic Search page with TTB header, menu box, and search form containing Date Completed fields, Product Name field with Brand Name/Fanciful Name/Either options, Product Class/Type range fields, and Origin Code field.]*

See Section 3.4 Search the Registry for information on searching the Public COLA Registry.

#### 3.3.2 COLAs Online FAQs

The COLAs Online FAQs menu option displays the COLAs Online Frequently Asked Questions page.

#### Figure 8: COLAs Online FAQs

> *[Screenshot: A FAQ page titled "COLAs Online" with a yellow "IMPORTANT" disclaimer box stating that TTB attempts to keep answers current and accurate but doesn't guarantee 100% accuracy, and that information may be modified or made obsolete by changes in laws and regulations. Users are directed to THOMAS (Library of Congress) and The Federal Register for recent changes. A "CONTACT US" box advises contacting TTB or legal advisor for concerns about accuracy. Below is "General Questions" section with a Print link, followed by expandable FAQ items marked with triangular arrows:
> - G1: Can I produce beer, wine or spirits for my personal or family use without paying Federal excise tax and filing Federal paperwork?
> - G2: What are the Federal and State excise taxes rates for spirits, wine and beer?
> - G3: Who can I contact when I have a complaint or suspect illegal activity by a bar, club, liquor store, restaurant or other business selling beverage alcohol products (spirits, wine or beer)?
> - G4: Does TTB have information or studies about the effects of consuming alcohol?
> - G5: How does TTB change its regulations?
> - G6: Can a student make alcohol as part of a science fair project?
> - G7: Are commercial vinegar producers regulated by TTB?
> - G8: Can I make vinegar for personal use?
> - G9: Does TTB regulate butanols, such as isobutanol?
> - G10: Do I need a permit to import beverage alcohol products for my own use, or to ship or bring my personal alcohol collection into the U.S. from overseas?]*

#### 3.3.3 Contact Us

The Contact Us menu option displays the Contact Us page. The Contact Us page provides information on how to contact ALFD Customer Service via the ALFD mailing address, Phone Number, Fax Number, ALFD e-mail address as well as submit a problem report.

#### Figure 9: Contact Us

> *[Screenshot: Contact Us page with TTB header banner. Title "Contact Us" with instructions to report problems or issues with COLAs Online / Public COLA Registry by filling out the form. "Trouble Logging On" section provides links for lost/forgotten password, expired password, and forgotten User ID issues. "Select a Subject" section with checkboxes:
> - I filed an e-application and it's no longer in my in-box
> - I'm having trouble uploading label images and/or attachments
> - How do I add/modify/delete my user and/or company information?
> - I'm experiencing problems searching the Public COLA Registry
> - I have a question regarding my label application
> - Other: [text field]
>
> "Comments" section with large text area. "Your Contact Information" section with fields for: Name, E-mail Address, Phone Number, Fax Number, TTB ID Number.]*

##### 3.3.3.1 Report Problems with the Public COLA Registry

Follow these steps to report a problem with the Public COLA Registry:

1. From the Public COLA Registry, select the **Contact Us** link from the menu box. The Contact Us page displays. See Figure 9.

2. Select one or more subject areas.

   ►Note: If your problem is not listed, enter the problem in the Other field.

3. Enter Comments (if any).

4. Enter the Name.

5. Enter the E-mail Address.

6. Enter the Phone Number.

7. Enter the Fax Number.

8. Enter the TTB ID Number (if any).

9. Select the **Submit** button to submit your e-mail problem report to ALFD.

10. Select the **Close** button to close the Contact Us page.

11. Select the **Clear and Start Over** button to reset all data fields.

#### 3.3.4 Public COLA Registry Manual

The Public COLA Registry Manual menu option displays a new browser window with the Public COLA Registry Online Help.

#### Figure 10: Public COLA Registry Online Help

> *[Screenshot: A help window titled "COLAs Online - Public COLA Registry Online Help" with three tabs at top: Contents, Index, Search. Left sidebar shows expandable tree menu:
> - COLAs Online
>   - Public COLA Registry (selected)
>   - Introduction
>   - System Capabilities
>   - System Functions
>   - Help Facilities
>   - Glossary
>
> Main content area shows "COLAs Online" header, then "Public COLA Registry" title with "Welcome to the Public COLA Registry Online Help." text. Below is the circular TTB seal/logo showing scales of justice with "TOBACCO TAX AND TRADE BUREAU" text around the perimeter. At bottom: "Updated: 6/11/2015" and "More:" section with arrow link to "Introduction".]*

#### 3.3.5 Download Public COLA Registry Manual

The Public COLA Registry Manual menu option displays the Public COLA Registry User Manual in PDF format.

#### Figure 11: Public COLA Registry User Manual

> *[Screenshot: Adobe PDF viewer showing the user manual. Left panel shows Bookmarks tree with expandable sections: Table of Contents, List of Figures, List of Tables, 1 INTRODUCTION, 2 SYSTEM CAPABILITIES, 3 SYSTEM FUNCTIONS, 4 HELP FACILITIES, Appendix A DEFINITION OF TERMS, INDEX. Main view shows the manual's title page with:
>
> "U.S. Department of the Treasury
> Alcohol and Tobacco Tax and Trade Bureau (TTB)
> 1310 G Street NW., Box 12
> Washington, D.C. 20005
>
> COLAs Online 3.11.3 Public COLA Registry User Manual"
>
> Below is the circular TTB seal/logo, then:
> "Prepared by:
> Office of the Chief Information Officer
> TTB RFC# TTB-2015-0124-MOD1"
>
> PDF toolbar shows page 1/50, 100% zoom, and various PDF tools.]*

#### 3.3.6 COLAs Online Logon

The COLAs Online Logon menu option displays the TTB Online Portal page, to allow access for registered COLAs Online users only.

#### Figure 12: TTB Online Portal

> *[Screenshot: Same as Figure 4 - TTBONLINE.GOV portal page with login section for registered users. Contains User Name and Password fields, COLAs Online and Formulas Online buttons, links for password recovery, processing times, and application status checks.]*

### 3.4 Search the Registry

This section discusses all of the basic information for searching in the system. This section includes the following information:

- **Public COLA Registry Basic Search** – See Section 3.4.1
- **Product/Class Type Lookup** – See Section 3.4.2
- **Origin Code Lookup** – See Section 3.4.3
- **Public COLA Registry Advanced Registry Search** – See Section 3.4.4
- **Vendor Code Lookup** – See Section 3.4.5
- **Search Results COLAs** – See Section 3.4.6
- **COLA Detail** – See Section 3.4.7

#### 3.4.1 Public COLA Registry Basic Search

The Public COLA Registry Basic Search page allows you to search for approved, expired, revoked, and surrendered COLAs.

#### Figure 13: Public COLA Registry Basic Search

> *[Screenshot: Same as Figure 5/7 - The COLA Registry Basic Search interface with all search fields: Date Completed (From/To), Product Name with Brand Name/Fanciful Name/Either radio buttons, Product Class/Type range with lookup button, Origin Code with lookup button, and Clear/Search buttons.]*

##### 3.4.1.1 Search for COLA (Basic)

Follow these steps to perform a basic search for a COLA:

►Note: Enter one or more fields of search criteria. Public searches process a great deal of data; therefore entering more search criteria will produce faster results.

1. Enter Date Completed time frame (From Date and To Date).

   ►Note: The format is MM/DD/YYYY. Select the 📅 icon to display a pop-up calendar to find the correct date.

   ►Note: The Date Completed range is defaulted from the first of the previous month to the current date. These values can be modified before submitting the search. The Date Completed range must be less than or equal to 15 years.

   ►Note: If a value is entered in the Date Completed (From) field a value must be entered in the Date Completed (To) field.

   ►Note: Because of changes made to the COLA database in 1996, searches for data prior to 1996 may not produce a complete result set.

2. Enter the Product Name if applicable.

3. Choose the **Brand Name**, **Fanciful Name** or **Either** radio option to search.

   ►Note: Certain generic searches, especially searches on Product Name/Fanciful Name without date parameters, can take several minutes to process. Whenever possible, a date range should be supplied.

4. Select the **Lookup Class Type** button to search for Product/Class Type. See Section 3.4.2.

5. Enter the Product Class Type range in the fields provided if applicable.

6. Select the **Lookup Origin** button to search for an Origin Code. See Section 3.4.3.

7. Enter the Origin Code value in the field provided if applicable.

8. Select the **Search** button to view your search results. See Section 3.4.6.

   ►Note: Search results are limited to a maximum of 500 items.

9. Select the **Clear and Start Over** button to reset all data fields to perform a new search.

►Note: To perform a wildcard search, enter a "%" at the beginning or end of the search criteria value.

#### 3.4.2 Product/Class Type Lookup

The Product/Class Type Lookup page allows you to search for product/class type codes and descriptions to be used to search for COLAs.

#### Figure 14: Product/Class Type Lookup

> *[Screenshot: A popup window titled "Product Class/Type Lookup" with TTB header banner. Contains "Search for Class/Type by:" section with note about wildcard character "%". Two search fields:
> - Product Class/Type Code: [text input]
> - Product Class/Type Description: [text input]
>
> "Show All Codes" button on the right. Bottom buttons: Close, Clear and Start Over, Search.]*

##### 3.4.2.1 Search for Product/Class Type

Follow these steps to search for Product/Class Type:

1. Select the **Lookup Class Type** button. The Product Class/Type Lookup page displays. See Figure 14.

2. Enter search criteria value(s) in the appropriate fields. The following fields are available:
   - Product Class/Type Code
   - Product Class/Type Description

   ►Note: To perform a wildcard search, enter a "%" at the beginning or end of the search criteria value.

3. Select the **Search** button. The search results based on the value entered display at the bottom of the page.

   ►Note: Search results are limited to a maximum of 500 items.

4. To view all product class/type codes, select the **Show All Codes** button. The product class/type codes display at the bottom of the page. See Figure 15.

#### Figure 15: Show All Codes (Product Class/Type Codes)

> *[Screenshot: Search Results table showing Class/Type codes and descriptions:
>
> | Class/Type Code | Description |
> |-----------------|-------------|
> | 0 | ADMINISTRATIVE WITHDRAWAL |
> | 00 | ADMINISTRATIVE WITHDRAWAL |
> | 000 | ADMINISTRATIVE WITHDRAWAL |
> | 100 | STRAIGHT WHISKY |
> | 101 | STRAIGHT BOURBON WHISKY |
> | 102 | STRAIGHT RYE WHISKY |
> | 103 | STRAIGHT CORN WHISKY |
> | 104 | RUM LEMON FLAVORED |
> | 105 | RUM CHERRY FLAVORED |
> | 106 | RUM CHOCOLATE FLAVORED |
> | 107 | RUM MINT FLAVORED |
> | 108 | RUM PEPPERMINT FLAVORED |
> | 109 | OTHER STRAIGHT WHISKY |
> | 110 | WHISKY BOTTLED IN BOND (BIB) |
> | 111 | BOURBON WHISKY BIB |
> | 112 | RYE WHISKY BIB |
> | ... | (continues) |]*

5. Select the **Close** button to return to the Search page.

►Note: To perform another search, select the **Clear and Start Over** button to reset all the fields and repeat Steps 2 and 3.

#### 3.4.3 Origin Code Lookup

The Origin Code Lookup page allows you to search origin codes and descriptions to be used to search for COLAs.

#### Figure 16: Origin Code Lookup

> *[Screenshot: A popup window titled "Origin Lookup" with TTB header banner. Contains "Search for Origin by:" section with note about wildcard character "%". Two search fields:
> - Origin Code: [text input]
> - Origin Description: [text input]
>
> "Show All Codes" button on the right. Bottom buttons: Close, Clear and Start Over, Search.]*

##### 3.4.3.1 Search for Origin Code

Follow these steps to search for an Origin Code:

1. Select the **Lookup Origin** button. The Origin Code Lookup page displays. See Figure 16.

2. Enter search criteria value(s) in the appropriate fields. The following fields are available for the search:
   - Origin Code
   - Origin Description

   ►Note: To perform a wildcard search, enter a "%" at the beginning or end of the search criteria value.

3. Select the **Search** button. The search results based on the value entered will appear at the bottom of the page.

   ►Note: Search results are limited to a maximum of 500 items.

4. To view all origin codes, select the **Show All Codes** button. The origin codes display at the bottom of the page. See Figure 17.

#### Figure 17: Show All Codes (Origin Codes)

> *[Screenshot: Search Results table showing Origin codes and descriptions:
>
> | Origin Code | Description |
> |-------------|-------------|
> | 00 | AMERICAN |
> | 01 | CALIFORNIA |
> | 02 | NEW YORK |
> | 03 | NEW JERSEY |
> | 04 | ILLINOIS |
> | 05 | VIRGINIA |
> | 06 | MICHIGAN |
> | 07 | WASHINGTON |
> | 08 | GEORGIA |
> | 09 | OHIO |
> | 10 | ALABAMA |
> | 11 | ARIZONA |
> | 12 | ARKANSAS |
> | 13 | COLORADO |
> | 14 | CONNECTICUT |
> | 15 | DELAWARE |
> | 16 | FLORIDA |
> | ... | (continues with all US states and foreign countries) |]*

5. Select the **Close** button to return to the Search page.

►Note: To perform another search, select the **Clear and Start Over** button to reset all the fields and repeat Steps 2 and 3.

#### 3.4.4 Public COLA Advanced Registry Search

The Public COLA Registry Advanced Search page allows you to search for approved, revoked, expired, and surrendered COLAs with advanced search criteria values compared to the basic search.

#### Figure 18: Public COLA Registry Advanced Search (Top)

> *[Screenshot: Top portion of Advanced Search page. Same TTB header and menu box as Basic Search. "Search for COLAs" section with note about generic searches. Shows "Basic Search | Advanced Search" tabs with Advanced Search selected. "Basic and Advanced Search Criteria" section with wildcard note. Contains:
> - Date Completed: From 7/01/2013 To 08/05/2013 (with calendar icons)
> - Product Name: [text field] with Brand Name / Fanciful Name / Either radio buttons
> - Product Class/Type: with radio options for "Show Codes (with description)" / "Show Descriptions (with code)" / "Enter Code Manually"
> - Instructions for multiple selection: "To select multiple values, press and hold the Ctrl key and use the mouse to select the values. To deselect a value, press and hold the Ctrl key and use the mouse to deselect the value. To select all the values within a range, select the first value in the range, then press and hold the Ctrl and Shift keys, and select the last value in the range."
> - Multi-select dropdown showing: "--Select One or More--", "ALE - 902", "ALE - 90..." (scrollable list)]*

#### Figure 19: Public COLA Registry Advanced Search (Bottom)

> *[Screenshot: Bottom portion of Advanced Search page continuing from Figure 18. Shows:
> - Origin Code: with multi-select instructions
> - Multi-select dropdown showing: "--Select One or More--", "ALABAMA - 10", "ALASKA - 46", "ALBANIA - 60", "ALGERIA - 61", "AMERICAN - 00", "ANGUILLA (BWI) - 7Q", "ANTIGUA AND BARBUDA - 4Y", "ARGENTINA - 62", "ARIZONA - 11" (scrollable list)
> - Lookup Origin> button
> - Received Code: (Check all that apply) with checkboxes:
>   - 000 - FRONT DESK (PAPER)
>   - 001 - ELECTRONIC SUBMISSION
>   - 002 - MAIL (PAPER)
>   - 003 - OVERNIGHT (PAPER)
> - TTB ID: [text field] to [text field] (range)
> - Serial #: [text field] to [text field] (range)
> - Plant Registry/Basic Permit/Brewer's No.: [text field] with note "Search Results will only include data after 04/26/2003"
> - Vendor Code: [text field] with note "Search Results will only include data prior to 04/26/2003" and Lookup Vendor Code> button
> - Bottom buttons: Clear and Start Over, Search]*

##### 3.4.4.1 Search for COLA (Advanced)

Follow these steps to perform an advanced search for a COLA:

1. Select the **Advanced Search** link on the Public COLA Registry Basic Search page. The Public COLA Registry Advanced Search page displays. See Figure 18 and Figure 19.

2. Enter Date Completed time frame (From Date and To Date).

   ►Note: The format is MM/DD/YYYY. Select the 📅 icon to display a pop-up calendar to find the correct date.

   ►Note: The Date Completed range is defaulted from the first of the previous month to the current date. These values can be modified before submitting the search. The Date Completed range must be less than or equal to 15 years.

   ►Note: Entering the same date in the "To" and "From" date fields will perform a search for that date only.

   ►Note: Because of changes made to the COLA database in 1996, searches for data prior to 1996 may not produce a complete result set.

3. Enter the Product Name if applicable.

4. Choose the **Brand Name**, **Fanciful Name** or **Either** radio option to search.

   ►Note: Certain generic searches, especially searches on Product Name/Fanciful Name without date parameters, can take several minutes to process. Whenever possible, a date range should be supplied.

5. Select the method to choose Product Class/Types - either by code selection, by description selection, or by entering the code manually. Depending on the method selected, choose the Product Class/Type(s) from the choice box or enter the Product Class/Type value(s) in the field provided if applicable. If necessary, select the **Lookup Class Type** button to search for product/class types. See Section 3.4.2.

6. Select the Origin Code(s) from the choice box if applicable. Select the **Lookup Origin** button to search for an origin code. See Section 3.4.3.

   ►Note: To select multiple values, press and hold the **Ctrl** key and use the mouse to select the values. To deselect a value, press and hold the **Ctrl** key and use the mouse to deselect the value. To select all the values within a range, select the first value in the range, then press and hold the **Ctrl** and **Shift** keys, and select the last value in the range.

7. Select the Received Code(s) if applicable.

8. Enter the TTB ID value(s) if applicable.

9. Enter the Serial # value(s) if applicable.

10. Enter the Plant Registry/Basic Permit/Brewer's No. value in the field provided if applicable.

11. Select the **Lookup Vendor Code** button to search for a Vendor Code. See Section 3.4.5.

    ►Note: Searches by Vendor Code will only return results for records filed before April 2003.

12. Enter the Vendor Code value in the field provided if applicable.

13. Select the **Search** button to view your search results. See Section 3.4.6.

    ►Note: Search results are limited to a maximum of 500 items.

14. Select the **Clear and Start Over** button to reset all data fields to perform a new search.

►Note: To perform a wildcard search, enter a "%" at the beginning or end of the search criteria value.

#### 3.4.5 Vendor Code Lookup

The Vendor Code Lookup page allows you to search for the Vendor Code, Vendor Name, and/or for Plant Registry/Basic Permit/Brewer's No. to be used in search for COLAs. Vendor Code searches will only return results prior to April 2003.

#### Figure 20: Vendor Code Lookup

> *[Screenshot: A popup window titled "Vendor Code Lookup" with TTB header banner. Contains "Search for Vendor Code by:" section with note about wildcard character "%". Three search fields:
> - Vendor Code: [text input]
> - Vendor Name: [text input]
> - Plant Registry/Basic Permit/Brewer's No.: [text input]
>
> Bottom buttons: Close, Clear and Start Over, Search.]*

##### 3.4.5.1 Search for Vendor Code

Follow these steps to search for a Vendor Code:

1. Select the **Lookup Vendor Code** button. The Vendor Code Lookup page displays. See Figure 20.

2. Enter search criteria value(s). The following fields are available for the search:
   - Vendor Code
   - Vendor Name
   - Plant Registry/Basic Permit/Brewer's No.

   ►Note: To perform a wildcard search, enter a "%" at the beginning or end of the search criteria value.

3. Select the **Search** button. The search results based on the value entered display at the bottom of the page.

   ►Note: Search results are limited to a maximum of 500 items.

4. Select the **Close** button to return to the Search page.

►Note: To perform another search, select the **Clear and Start Over** button to reset all the fields and repeat Steps 2 and 3.

#### 3.4.6 Search Results COLAs

The Search Results: COLAs page allows public users the ability to view their search results based on criteria entered and save the search results to a .csv file (viewable through Microsoft Excel or other associated application).

#### Figure 21: Search Results: COLAs (Top)

> *[Screenshot: Top portion of search results page. TTB header and COLA Registry branding with menu box. "Search Results: COLAs" section showing:
> - "Printable Version" link
> - "Save Search Results To File" link
> - "1 to 20 of 99 (Total Matching Records: 99) | Next >" pagination
>
> Results table with sortable column headers (underlined as links):
>
> | TTB ID | Permit No. | Serial Number | Completed Date | Fanciful Name | Brand Name | Origin | Class/Type |
> |--------|------------|---------------|----------------|---------------|------------|--------|------------|
> | 05332301000029 | AZ-I-15555 | 05LE02 | 08/03/2011 | | POM MALT | 81 | 977 |
> | 10044401000002 | DSP-FL-333 | 101112 | 03/01/2011 | | POM BRAND | 00 | 200 |
> | 10011101000001 | BW-OK-222 | 102342 | 05/03/2011 | | POM PEAR WINE | 04 | 80 |
> | 10211101000001 | BR-MA-CAP-15555 | 109999 | 05/19/2011 | | POM MALT | 21 | 83 |
> | 11000001000002 | BR-MA-CAP-15555 | 114444 | 01/11/2011 | | POM TASTY | 00 | 900 |
> | 11022201000001 | VA-I-15555 | 117894 | 01/13/2011 | | POM RED WINE | 56 | 979 |
> | 11022201000003 | BW-WA-333 | 113456 | 01/13/2011 | | POM WINE | 00 | 88 |
> | 11022201000004 | NY-P-1999 | 117777 | 01/13/2011 | | POM GERMAN WINE | 00 | 900 |
> | 11022201000005 | BWC-OH-444 | 117142 | 01/13/2011 | | POM PEACH MALT | 00 | 88 |]*

#### Figure 22: Search Results: COLAs (Bottom)

> *[Screenshot: Bottom portion of search results page continuing from Figure 21. Shows more result rows:
>
> | TTB ID | Permit No. | Serial Number | Completed Date | Fanciful Name | Brand Name | Origin | Class/Type |
> |--------|------------|---------------|----------------|---------------|------------|--------|------------|
> | 11013331000004 | BR-CA-STE-15555 | 110001 | 01/13/2011 | | POM FORMULA | 00 | 900 |
> | 11013331000007 | BR-MA-CAP-15555 | 110003 | 01/13/2011 | | POM FORMULA | 00 | 900 |
> | 11013331000008 | BW-NY-999 | 110003 | 01/14/2011 | | POM DOMESTIC WINE | 00 | 88 |
> | 11103331000002 | BW-OK-222 | 112342 | 04/13/2011 | | POM ROSE MALT | 37 | 80 |
> | 11103332000000 | TX-I-15555 | 1176666544 | 04/13/2011 | | POM DAISY MALT | 37 | 80 |
> | 11111111000001 | PR-W-444 | 112222 | 05/09/2011 | | POM FINE WINES | 01 | 80 |
> | 11116661000001 | PA-P-5555 | 112222 | 05/03/2011 | POM | POM MANGO WINE | 17 | 80 |
> | 11131111000001 | PR-W-111 | 113344 | 05/19/2011 | | POM JAPANESE WINE | 01 | 80 |
> | 11154441000001 | BW-WA-444 | 113333 | 06/14/2011 | | POM BRAND | 01 | 80 |
> | 11174441000001 | BW-OK-777 | 119999 | 06/23/2011 | POM | POM KIWI WINE | 14 | 80 |
>
> Below table: "Printable Version" link, pagination "1 to 20 of 99 (Total Matching Records: 99) | Next >", "New Search" button.
>
> Page footer includes disclaimer about TTB data accuracy, type size/characters per inch/contrasting background disclaimer, reference to Section V of TTB COLA Form 5100.31 Allowable Revisions, contact email, screen resolution recommendation, browser compatibility note, and full government warning.]*

##### 3.4.6.1 View Search Results COLAs

Follow these steps to view your search results:

1. Select the **Search Public COLA Registry** link from the menu box on any page.

2. Enter search criteria.

3. Select the **Search** button. The Search Results: COLAs page displays with search results based on the value entered. See Figure 21 and Figure 22.

   ►Note: Search results are limited to a maximum of 500 items.

4. To sort the search results, select on any column heading to sort on that attribute.

5. To view more search results, select the **Next** link.

6. To view the details of a COLA, select the **TTB ID** link. See Section 3.4.7.

7. To save your search results, select the **Save Search Results To File** link. See Section 3.4.6.2.

8. Select the **New Search** button to return to the Search page.

##### 3.4.6.2 Save Search Results COLAs

Follow these steps to save your search results to a .csv file:

1. Follow the steps in Section 3.4.6.1 View Search Results COLAs.

2. Select the **Save Search Results To File** link above the search results. See Figure 21. The File Download dialog displays.

3. Select the **Save** button or select the **Open** button.

   a. If you select the **Save** button: Save the file when prompted and then select the **Open** button. The search results display in the associated application (i.e., Microsoft Excel).

   ►Note: It is recommended you select the **Save** button in the File Download dialog, save the file in the Save As dialog, and then select the **Open** button in the Download Complete dialog to display the search results file in the associated application faster.

   b. If you select the **Open** button: The search results display in the associated application (i.e., Microsoft Excel).

   ►Note: Opening the search results directly without saving first may take longer to display the search results in the associated application.

►Note: Search results saved are limited to a maximum of 500 items returned from the search.

The following detail from the search results will be included in the file:

- TTB ID (►Note: TTB ID values will be enclosed in single quotes ('))
- Permit No.
- Serial Number
- Completed Date
- Fanciful Name
- Brand Name
- Origin
- Class/Type

#### 3.4.7 COLA Detail

The COLA Detail page allows you to view the details of an approved, expired, surrendered, or revoked COLA.

#### Figure 23: COLA Detail (Top)

> *[Screenshot: Top portion of COLA Detail page. TTB header and COLA Registry branding with menu box. "COLA Detail" title with:
> - TTB ID: ❓ 10207771000001 with "> Printable Version" link to the right
> - Status: ❓ SURRENDERED
> - Vendor Code: ❓ 13400
> - Serial #: ❓ 101234
> - Class/Type Code: ❓ DESSERT FLAVORED WINE
> - Origin Code: ❓ AMERICAN
> - Brand Name: ❓ POM WINERY
> - Fanciful Name: ❓ (empty)
> - Type of Application: ❓ LABEL APPROVAL
> - For Sale In: ❓ (empty)
> - Total Bottle Capacity: ❓ (empty)
> - Grape Varietal(s): ❓ (empty)
> - Wine Vintage: ❓ (empty)
> - Formula/SOP No.: ❓ (empty)
>
> Each field label has a ❓ icon indicating field-level help is available.]*

#### Figure 24: COLA Detail (Bottom)

> *[Screenshot: Bottom portion of COLA Detail page continuing from Figure 23. Shows:
> - Grape Varietal(s): ❓ (empty)
> - Wine Vintage: ❓ (empty)
> - Formula/SOP No.: ❓ (empty)
> - Lab No./Lab Date: ❓ (empty)
> - Approval Date: 07/26/2010
> - Qualifications: ❓ (empty)
> - Plant Registry/Basic Permit/Brewers No (Principal Place of Business): ❓
>   - BWH-MA-15555
>   - POM WINERY, LLC [with a small icon/button]
>   - 5555 KEARN RD
>   - NEEDHAM, MA 02494
> - Plant Registry/Basic Permit/Brewers No (Other): ❓ (empty)
> - Contact Information:
>   - JANE SMITH
>   - Phone Number: (202) 453-2000
>   - Fax Number: (empty)
>   - JANE.SMITH@TTB.GOV
>
> "Back" button at bottom. Footer with disclaimer, Department of Treasury logo, and legal notices.]*

##### 3.4.7.1 View COLA Detail

Follow these steps to view COLA details:

1. Select the **TTB ID** link. The COLA Detail page displays. See Figure 23 and Figure 24.

2. Use the scroll bar to view all the details of the COLA.

3. For e-filed applications, select the **Printable Version** link to view a printable version of an e-filed COLA. See Section 3.5.1.

   ►Note: e-filed COLAs are identified by a "001" in positions 6-8 of the TTB ID.

   ►Note: Older COLA applications may not have an available printable version. If you want to obtain a copy of the entire COLA, you will need to make a request under FOIA. For more information, go to http://www.ttb.gov/foia/index.shtml. Please include CFM ID/TTB ID number in your request.

4. For paper filed applications, select the **Printable Version** link to view a scanned image of a paper filed COLA. See Section 3.5.2.

5. Select the **Back** button to return to the search results page.

### 3.5 Printable Version of COLA

This section discusses all of the basic information for printing COLAs in the system. This section includes the following information:

- **Printable E-filed COLA** – See Section 3.5.1
- **Printable Paper Filed COLA** – See Section 3.5.2

#### 3.5.1 Printable E-filed COLA

The Printable E-filed COLA page provides you a printable version of an e-filed COLA.

#### Figure 25: Printable E-filed COLA (Top)

> *[Screenshot: Top portion of printable e-filed COLA showing TTB Form 5100.31. Header shows "OMB No. 1513-0020 (01/31/2009)" and "FOR TTB USE ONLY". Document title: "DEPARTMENT OF THE TREASURY, ALCOHOL AND TOBACCO TAX AND TRADE BUREAU, APPLICATION FOR AND CERTIFICATION/EXEMPTION OF LABEL/BOTTLE APPROVAL (See Instructions and Paperwork Reduction Act Notice on Back)".
>
> **PART I - APPLICATION**
>
> Form fields shown in a structured layout:
> - TTB ID: 09065001006688
> - 1. REP. ID. NO. (If any): CT 81, OR 85
> - 2. PLANT REGISTRY/BASIC PERMIT/BREWER'S NO. (Required): BW-VA-6666
> - 3. SOURCE OF PRODUCT (Required): ☑ Domestic ☐ Imported
> - 8. NAME AND ADDRESS OF APPLICANT AS SHOWN ON PLANT REGISTRY, BASIC PERMIT OR BREWER'S NOTICE. INCLUDE APPROVED DBA OR TRADENAME IF USED ON LABEL (Required): POM VINEYARDS LTD., 3777 FARRELLS CORNER RD, LINDEN VA 22642
> - 4. SERIAL NUMBER (Required): 090555
> - 5. TYPE OF PRODUCT (Required): ☑ WINE ☐ DISTILLED SPIRITS ☐ MALT BEVERAGE
> - 6. BRAND NAME (Required): POM VINEYARDS
> - 7. FANCIFUL NAME (if any): (empty)
> - 8a. MAILING ADDRESS, IF DIFFERENT: (empty)
> - 9. EMAIL ADDRESS: WINE@POMVINEYARDS.COM
> - 10. FORMULA/SOP NO. (if any): (empty)
> - 11. LAB. NO. & DATE / PREIMPORT NO. & DATE (if any): (empty)
> - 18. TYPE OF APPLICATION (Check applicable box(es)):
>   - a. ☑ CERTIFICATE OF LABEL APPROVAL
>   - b. ☐ CERTIFICATE OF EXEMPTION FROM LABEL APPROVAL "For sale in ___ only" (Fill in State abbreviation)
>   - c. ☐ DISTINCTIVE LIQUOR BOTTLE APPROVAL. TOTAL BOTTLE CAPACITY BEFORE CLOSURE (Fill in amount)
>   - d. ☐ RESUBMISSION AFTER REJECTION TTB ID No.___
> - 12. NET CONTENTS: 375 MILLILITERS
> - 13. ALCOHOL CONTENT: 13.8
> - 14. WINE APPELLATION IF ON LABEL: VIRGINIA
> - 15. WINE VINTAGE DATE IF ON LABEL: 2009
> - 16. PHONE NUMBER: (540) 364-1997
> - 17. FAX NUMBER: (540) 364-3333
> - 19. SHOW ANY WORDING (a) APPEARING ON MATERIALS FIRMLY AFFIXED TO THE CONTAINER (e.g., caps, capsules, corks, etc.) OTHER THAN THE LABELS AFFIXED BELOW, OR (b) BLOWN, BRANDED OR EMBOSSED ON THE CONTAINER (e.g., net contents, etc.). THIS WORDING MUST BE NOTED HERE EVEN IF IT DUPLICATES PORTIONS OF THE LABELS AFFIXED BELOW. ALSO, PROVIDE TRANSLATIONS OF FOREIGN LANGUAGE TEXT APPEARING ON LABELS.
>
> **PART II - APPLICANT'S CERTIFICATION**
> "Under the penalties of perjury, I declare, that all statements appearing on this application are true and correct to the best of my knowledge and belief; and, that the representations on the labels attached to this form, including supplemental documents, truly and correctly represent the content of the containers to which these labels will be applied. I also certify that I have read, understood and complied with the conditions and instructions which are attached to an original TTB F 5100.31, Certificate/Exemption of Label/Bottle Approval."
>
> - 20. DATE OF APPLICATION: (date field)
> - 21. SIGNATURE OF APPLICANT OR AUTHORIZED AGENT: (signature field)
> - 22. PRINT NAME OF APPLICANT OR AUTHORIZED AGENT: (name field)]*

#### Figure 26: Printable E-filed COLA (Bottom)

> *[Screenshot: Bottom portion of printable e-filed COLA showing:
>
> **PART III - TTB CERTIFICATE**
> "This certificate is issued subject to applicable laws, regulations and conditions as set forth in the instructions portion of this form."
>
> - 23. DATE ISSUED: 01/05/2010
> - 24. AUTHORIZED SIGNATURE, ALCOHOL AND TOBACCO TAX AND TRADE BUREAU: [signature graphic]
>
> **FOR TTB USE ONLY**
>
> | QUALIFICATIONS | EXPIRATION DATE (if any) |
> |----------------|--------------------------|
> | (empty) | (empty) |
>
> **STATUS:** THE STATUS IS APPROVED.
>
> **CLASS/TYPE DESCRIPTION:** TABLE WHITE WINE
>
> **AFFIX COMPLETE SET OF LABELS BELOW**
>
> Image Type: Brand (front)
> Actual Dimensions: 2.25 inches W X 3.25 inches H
>
> [Wine label image showing:
> - Decorative vine/leaf graphic at top
> - "2009 VIRGINIA SAUVIGNON BLANC"
> - "AVENIUS"
> - "ALC. 13.8% BY VOL."
> - "MADE AND BOTTLED BY"
> - "LINDEN VINEYARDS, LTD."
> - "LINDEN, VIRGINIA 22642"]
>
> [Second label/back label showing:
> - "GOVERNMENT WARNING: (1) ACCORDING TO THE SURGEON GENERAL, WOMEN SHOULD NOT DRINK ALCOHOLIC BEVERAGES DURING PREGNANCY BECAUSE OF THE RISK OF BIRTH DEFECTS. (2) CONSUMPTION OF ALCOHOLIC BEVERAGES IMPAIRS YOUR ABILITY TO DRIVE A CAR OR OPERATE MACHINERY, AND MAY CAUSE HEALTH PROBLEMS."
> - UPC barcode
> - "CONTAINS SULFITES"]
>
> Image Type: Back
> Actual Dimensions: 3.25 inches W X 3.25 inches H]*

##### 3.5.1.1 Print an E-filed COLA

Follow these steps to print an e-filed COLA:

1. Select the **TTB ID** link. The COLA Detail page displays. See Figure 23 and Figure 24.

2. Select the **Printable Version** link to view a printable version of an e-filed COLA. See Figure 25 and Figure 26.

   ►Note: e-filed COLAs are identified by a "001" in positions 6-8 of the TTB ID.

   ►Note: For existing COLA applications (before COLAs Online 3.5), the "FORMULA/SOP NO." Field is Block 10 and the "LAB. NO. & DATE / PREIMPORT NO. & DATE" Field is Block 11.

   For new COLA applications (COLAs Online 3.5), the "GRAPE VARIETAL(S)" Field is Block 10 and the "FORMULA" field is Block 11. The "FORMULA" field will display the value (if any) for the Company Formula Code or TTB Formula ID and/or the Lab Sample Number and Lab Date.

3. Select the 🖨️ icon from your web browser.

#### 3.5.2 Printable Paper Filed COLA

The Printable Paper Filed COLA page provides you a scanned image of a paper filed COLA.

#### Figure 27: Printable Paper Filed COLA

> *[Screenshot: Scanned image of a paper-filed TTB Form 5100.31. This is a scanned/photographed copy of an actual paper submission, showing:
>
> Header: "OMB No. 1513-0020 (03/31/2012)", "FOR TTB USE ONLY"
>
> **TTB ID:** 10005-003-006686
>
> Handwritten/typed form fields:
> - 1. REP. ID. NO. (If any): 209, OR 05
> - 2. PLANT REGISTRY/BASIC PERMIT/BREWER'S NO.: DSP-VA-15555
> - 3. SOURCE OF PRODUCT: ☑ Domestic ☐ Imported
> - 4. SERIAL NUMBER: YEAR: 10, [handwritten] 0 0 0 2
> - 5. TYPE OF PRODUCT: ☐ WINE ☑ DISTILLED SPIRITS ☐ MALT BEVERAGES
> - 8. NAME AND ADDRESS: Pom Creek Distilling Company, 37777 Richardson Lane Ste 222, Purcellville, VA 20132-3505, DBA: Pom Creek Distilling Company
> - 8a. MAILING ADDRESS: Pom Creek Distilling Company, 444 Dresden Ct., Purcellville, VA 20132-3060
> - 6. BRAND NAME: Pom Creek
> - 7. FANCIFUL NAME: Pom Gin
> - 9. E-MAIL ADDRESS: scott@pomcreek.com
> - 10. FORMULA/SOP NO.: 1
> - 11. LAB. NO. & DATE/PREIMPORT NO. & DATE: N/A
> - 12. NET CONTENTS: 750 ml
> - 13. ALCOHOL CONTENT: 50% ABV
> - 14. WINE APPELLATION: N/A
> - 15. WINE VINTAGE DATE: N/A
> - 16. PHONE NUMBER: 540-751-8888
> - 17. FAX NUMBER: 540-751-3333
> - 18. TYPE OF APPLICATION: ☑ a. CERTIFICATE OF LABEL APPROVAL
> - 19. [Container/materials wording]: None.
>
> **PART II - APPLICANT'S CERTIFICATION**
> - 20. DATE OF APPLICATION: 1/5/2010
> - 21. SIGNATURE: [handwritten signature]
> - 22. PRINT NAME: E. Harris, Vice President
>
> **PART III - TTB CERTIFICATE**
> - 23. DATE ISSUED: JAN 11 2010 (stamped)
> - 24. AUTHORIZED SIGNATURE: [signature]
>
> **FOR TTB USE ONLY**
> - QUALIFICATIONS: (empty)
> - EXPIRATION DATE: (empty)
>
> **AFFIX COMPLETE SET OF LABELS BELOW**
>
> [Attached gin label showing:
> - "POM GIN" in large letters
> - "DISTILLED FROM RYE"
> - "NATURALLY DISTILLED AND BOTTLED IN LOUDOUN COUNTY, VA FROM HIGHEST QUALITY INGREDIENTS"
> - "POM CREEK DISTILLING COMPANY, LLC PURCELLVILLE, VA"
> - "50% ALC. BY VOL."]
>
> Footer: "TTB F 5100.31 (05/2009) PREVIOUS EDITIONS ARE OBSOLETE"]*

##### 3.5.2.1 Print a Paper Filed COLA

Follow these steps to print a paper filed COLA:

1. Select the **TTB ID** link. The COLA Detail page displays. See Figure 23 and Figure 24.

2. Select the **Printable Version** link to view a scanned image of the paper filed COLA. See Figure 27.

3. Select the 🖨️ icon from your web browser.

---

## 4 Help Facilities

This section discusses the help facilities provided to users of the Public COLA Registry system.

### 4.1 Field Level Tool Tips

Tool tips are small rectangles of text that describes a field. Field level tool tips will be provided in the system when the user pauses with the cursor over any of the system field labels.

### 4.2 Public COLA Registry Online Help

The Public COLA Registry Online Help is available through the **Public COLA Registry Manual** link in the menu box.

### 4.3 Public COLA Registry User Manual

The Public COLA Registry User Manual is available (in PDF format) through the **Download Public COLA Registry Manual** link in the menu box.

### 4.4 ALFD Customer Service

If you need assistance, please contact ALFD Customer Service:

- **Phone:** (202) 453-2250 OR 1-866-927-ALFD (Toll Free)
- **Email:** alfd@ttb.gov

### 4.5 Definition of Terms

The most common Public COLA Registry terms (field names) used and their definitions can be found in Appendix A.

---

## Appendix A: Definition of Terms

This section provides the definitions of common terms used in the Public COLA Registry.

### A

**Alcohol Content**

An accurate statement of the alcohol content must appear on the brand label of all wine and distilled spirits products. This statement is optional for malt beverages, but if shown must be in the correct format.

- **Wine Labels** – When creating an eApplication please indicate the specific alcohol content or range of alcohol content as it appears on the label. If you are using "table wine" or "light wine" on your label to meet the alcohol content requirement, either indicate the alcohol content of the wine or enter "table" or "light" in this field.
- **Malt Beverage Labels** - When creating an eApplication please indicate the alcohol content as it appears on the label (if shown). If alcohol content is not shown on the label this field is optional.
- **Distilled Spirit Labels** - When creating an eApplication please indicate the alcohol content as it appears on the label.

**ALFD**

Advertising, Labeling and Formulation Division.

**Approved**

This status indicates a final action regarding a particular application. Applications enter this status when both the application and the labels meet all applicable requirements. At this point an application becomes a Certificate. This status authorizes the Certificate holder to either bottle or remove from Customs custody alcohol beverages that bear labels identical to those shown on the Certificate.

### B

**Brand Name**

This is the name under which a product is sold. If the product is not sold under a brand name, the name of the bottler, packer or importer becomes the brand name.

### C

**Capacity**

This is the actual volume of the container that is required on the COLA for Distinctive Liquor Bottles.

**Class/Type**

This code indicates the class and or type designation for a product. Each product has been assigned a unique class/type code.

**COLA**

Certificate of Label Approval.

**COLAs Online**

Certificate of Label Approval System.

### E

**e-filed**

Electronically filed.

**eApplication**

An electronically submitted COLAs application.

**Expired**

While generally "Approved" Certificates never expire, under certain limited conditions Certificates are given an expiration date by TTB at the time of approval. The status of an "Approved" Certificates changes to "Expired" when the expiration date is reached.

### F

**Fanciful Name**

This is a name that may be used in addition to a brand name to further identify a product and is required for malt beverage and distilled spirit specialty products that must be labeled with a statement of composition. It is optional for other products. Supply the Fanciful Name if one is used on the label.

**FAQs**

Frequently Asked Questions.

**FOIA**

Freedom of Information Act.

**FONL**

Formulas Online.

**Formula**

Corresponds with Item 11 on 5100.31 - The term "Formula" encompasses formulas, pre-import approval letters, lab analysis, and submissions formerly known as statements of process (SOP). A Formula is a quantitative list of ingredients and a step-by-step method of manufacture for alcohol beverage products (wine, distilled spirits, malt beverage) requiring approval from TTB prior to production or importation as per Industry Circular 2007-4. TTB's Regulatory Authority for such products may also be found at 27 CFR parts 4, 5, 7, 19, 24, 25, and 26. Please visit http://www.ttb.gov/formulation/index.shtml for more information.

For any domestic or imported alcohol beverage products that received TTB formula approval prior to January 10, 2011, please manually enter the TTB ID number, or TTB lab number in the Company Formula #/SOP# text box. A copy of the approved formula, or pre-import approval letter must accompany the label application.

If formula approval for any domestic or imported alcohol beverage product was obtained after January 10, 2011 please select the TTB Formula ID number (generated by Formulas Online) from the drop-down list of approved formulas. DO NOT submit your COLA application until AFTER you have obtained formula approval, if required.

### G

**Grape Varietals**

Grape Varietals are the names of the dominant grapes used in the wine. Cabernet Sauvignon, Chardonnay, Zinfandel, and Merlot are examples of grape varieties. A Grape Varietal designation on the label requires an appellation of origin and means that at least 75 percent of the grapes used to make the wine are of that variety, and that entire 75 percent were grown in the labeled appellation (except "Vitis labrusca" grapes, such as Concord, which require at least 51 percent).

### I

**IM**

Industry Member.

### N

**NRC**

National Revenue Center.

### O

**OCIO**

Office of the Chief Information Officer.

**OIM**

Online Industry Member.

**Origin**

This code indicates the country (or state for domestic products) of origin for each product. Each country has been assigned a unique origin code. Enter the origin code if you know it, or use the lookup feature to find it.

### P

**PCR**

Public COLA Registry.

**Permit Name**

The operating name and/or owner name associated with a Plant Registry/Basic Permit/Brewer's Number.

**PIA**

Privacy Impact Assessment.

**Plant Registry/Basic Permit/Brewer's No.**

This is a unique number that is assigned by TTB to each business location. Examples include BW-NY-123, DSP-KY-89, BR-WI-ABC-567 or VA-I-456.

When submitting an eApplication, please select the location(s) where this product will be bottled/imported. You may only file eApplication(s) for locations that appear in your "My Profile" section of COLAs Online.

Proprietors of domestic Distilled Spirits Plants and Breweries may obtain one COLA to cover multiple business locations if: the principle place of business is shown in the mandatory name and address statement on the label(s) AND the same label will be used for products bottled at each location.

A COLA must be obtained for each location where a domestic wine is actually bottled (i.e., one COLA may not cover multiple locations).

Beverage alcohol Importers may not use one COLA to cover multiple locations.

When searching from the COLAs Online search screen, you may only search for COLAs filed by the companies that appear in your "My Profile" section of COLAs Online. Either select one number, or you may select "any" if you are registered to file COLAs on behalf of multiple entities.

**Product Class/Type**

This code indicates the class and or type designation for a product. Each product has been assigned a unique class/type code. Enter the class/type code if you know it, or use the lookup feature to find it.

**Product Name**

You may search for COLAs by "Brand Name" OR "Fanciful Name" OR both if you select "Either."

The Brand Name is the name under which a product is sold. If the product is not sold under a brand name, the name of the bottler, packer or importer becomes the brand name.

The Fanciful Name is a name that may used in addition to a brand name to further identify a product and is required for malt beverage and distilled spirit specialty products that must be labeled with a statement of composition. It is optional for other products.

### R

**Received Code**

A three digit code number at the sixth, seventh and eighth positions within the TTB ID number that indicates how a label application was received. For instance, if the application was received electronically then the TTB ID # would contain the received code "001" at the sixth, seventh and eighth positions. Other receive codes used are "000" for hand delivered applications, "002" indicates that the application was received by regular USPS mail and "003" indicates that the application was received by an overnight delivery service such as UPS or FEDEX.

**Revoked**

"Approved" Certificates will change to this status when TTB rescinds approval because either the labeling laws or regulations have changed rendering the Certificate invalid or the Certificate was approved by TTB in error.

### S

**SDLC**

Systems Development Life Cycle.

**Serial Number**

This is a unique, sequential number assigned by the COLA holder. The first two digits reflect the calendar year the application was created. The remaining digits may be a combination of letters and numbers but may not exceed four characters in length.

When creating an eApplication you must assign a sequential and unique number to each application. COLAs Online automatically assigns the first two characters, which represent the current calendar year.

**Sulfite Analysis**

Any standard wine label that does not contain a sulfite declaration or contains a Sulfite-Free declaration must be submitted to either a TTB laboratory or a TTB-certified laboratory for analysis. The results of this analysis must be included with the COLA.

**Surrendered**

"Approved" Certificates will change to this status when the Certificate holder voluntarily communicates to TTB that they no longer need the Certificate. Generally "Approved" Certificates do not expire, however, TTB encourages all industry members to surrender obsolete Certificates either by written communication for paper filed applications or electronically if applications were e-filed.

### T

**TTB**

Alcohol and Tobacco Tax and Trade Bureau.

**TTB ID**

This is a unique, 14 digit number assigned by TTB to track each COLA. The first 5 digits represent the calendar year and Julian date the application was received by TTB. The next 3 digits tell how the application was received (001 = e-filed; 002 & 003 = mailed/overnight; 000 = hand delivered). The last 6 digits is a sequential number that resets for each day and for each received code.

If you know the TTB ID number, this is the best way to search for individual COLAs. The TTB ID number for eApplications is supplied to the submitter in the "Application Submitted" confirmation message. The TTB ID number can be found in the upper left-hand corner of paper COLAs.

**Type of Application**

A Certificate of Label Approval authorizes a product to be sold in interstate commerce and must be obtained BEFORE a domestic product is bottled or BEFORE an imported product is removed from Customs' custody.

A Certificate of Exemption authorizes a product to be sold in the state where it was bottled and must be obtained BEFORE a product is bottled.

When completing an eApplication, select Certificate of Label Approval if this alcohol beverage will be sold within the state where the bottler is located and/or in interstate commerce (i.e., in states other than where the bottler is located).

When completing an eApplication, select Certificate of Exemption from Label Approval if you will only sell this alcohol beverage intrastate (i.e., only within the state where the bottler is located), and you wish to be exempted from the labeling requirements of the Federal Alcohol Administration Act.

Products approved under a Certificate of Exemption MUST be labeled "For sale in (state where bottling takes place) only."

►Note: TTB does not issue Certificates of Exemption for Malt Beverages or for products imported in bottles.

**Type of Product**

Select either Wine, Distilled Spirit or Malt Beverage.

If you are unsure of the classification of a product, please contact the Alcohol Labeling & Formulation Division Customer Service Team at 1-866-927-ALFD or by e-mail at alfd@ttb.gov.

►Note: Sake is classified as wine for labeling purposes.

**Type of Submission**

If Distinctive Liquor Bottle is selected, enter the total bottle capacity before closure.

### V

**Vendor Code**

This code was used in the past to identify organizations who were submitting COLAs. The Vendor Code is no longer in use, but may be used to search for certain historical COLA records. Plant Registry/Basic Permit/Brewer's No. is used to identify the business locations for which the COLA applications are filed.

**Vendor Name**

No longer in use. See "Vendor Code" for details.

---

## Index

### C
- COLA Detail - Section 3.4.7
  - View COLA Detail - Section 3.4.7.1
- Contact Us - Section 3.3.3
  - Report Problems with the Public COLA Registry - Section 3.3.3.1

### H
- Help Facilities - Section 4
  - ALFD Customer Service - Section 4.4
  - Field Level Tool Tips - Section 4.1
  - Public COLA Registry Online Help - Section 4.2
  - Public COLA Registry User Manual - Section 4.3

### M
- Menu Options - Section 3.3
  - COLAs Online FAQs - Section 3.3.2
  - COLAs Online Logon - Section 3.3.6
  - Contact Us - Section 3.3.3
  - Download Public COLA Registry Manual - Section 3.3.5
  - Public COLA Registry Manual - Section 3.3.4
  - Search Public COLA Registry - Section 3.3.1

### O
- Origin Code Lookup - Section 3.4.3
  - Search for Origin Code - Section 3.4.3.1

### P
- Printable E-filed COLA - Section 3.5.1
  - Print an E-filed COLA - Section 3.5.1.1
- Printable Paper Filed COLA - Section 3.5.2
  - Print a Paper Filed COLA - Section 3.5.2.1
- Printable Version of COLA - Section 3.5
- Privacy Act Considerations - Section 2.2
- Product/Class Type Lookup - Section 3.4.2
  - Search for Product/Class Type - Section 3.4.2.1
- Public COLA Advanced Registry Search - Section 3.4.4
  - Search for COLA (Advanced) - Section 3.4.4.1
- Public COLA Registry
  - Access the Public COLA Registry - Section 3.2.1
  - General Description - Section 2.1
  - Getting Started - Section 3.2
  - Help Facilities - Section 4
  - Menu Options - Section 3.3
  - Privacy Act Considerations - Section 2.2
  - Search The Registry - Section 3.4
  - System Basics - Section 3.1
  - System Capabilities - Section 2
  - System Functions - Section 3
- Public COLA Registry Basic Search - Section 3.4.1
  - Search for COLA (Basic) - Section 3.4.1.1

### S
- Search Results COLAs - Section 3.4.6
  - Save Search Results COLAs - Section 3.4.6.2
  - View Search Results COLAs - Section 3.4.6.1
- Search The Registry - Section 3.4
  - COLA Detail - Section 3.4.7
  - Origin Code Lookup - Section 3.4.3
  - Product/Class Type Lookup - Section 3.4.2
  - Public COLA Advanced Registry Search - Section 3.4.4
  - Public COLA Registry Basic Search - Section 3.4.1
  - Search Results COLAs - Section 3.4.6
  - Vendor Code Lookup - Section 3.4.5

### T
- Terms - Appendix A
- TTB Online Portal Page - Section 3.2

### V
- Vendor Code Lookup - Section 3.4.5
  - Search for Vendor Code - Section 3.4.5.1

---

*Source: COLAs Online 3.11.3 Public COLA Registry User Manual, TTB, June 11, 2015*
