# LandingLand

OA3801 Final Project

The files in this repository:
 - Executive summary 
 - Final Presentation
 - Raw sold data (csv)
 - Foley sold data (excel)
 - 3 Code files
    - LandProject.ipynb: identify hot pockets
    - Foley.ipynb: Prices the plots
    - foley_mail_names.py: parses the mailing labels
      
-------------------------------------------------------------------

Executive Summary: A Data-Driven Model for Land Acquisition Marketing

Introduction: The Policy Problem 

A land investor faces high direct-mail marketing costs and operational inefficiencies. To ensure profitability, the client must target only "hot markets" where land sells quickly and provide accurate, automated offer prices. This project addresses the challenge of how to precisely identify these markets from data and how to apply an accurate, automated valuation to parcels within them, thereby reducing marketing waste and increasing lead quality.

Approach and Key Findings 

To solve this problem, we developed and tested a multi-part system. Our key findings are:

 - Defining "Hot Markets": We successfully developed a data-driven definition for a target market: a 10-mile radius where 15 or more properties (2-5 acres) sold within 90 days.

 - Automated Pricing Model: We created an automated valuation model. The model establishes a base price per acre by averaging all comparable sales in the radius from the last year. It then applies weights to this price based on key land attributes (slope, wetland coverage, and road frontage) to devalue or increase the offer price.

 - Mailing List Automation: We found that owner name data was too complex for traditional parsing methods (e.g., string splitting). We successfully implemented an LLM API to dynamically handle complex names, providing an effective solution for formatting the mailing list.

Recommendations 

Based on these findings, we recommend any land investor to adopt this system with two key verification steps to ensure accuracy and limit risk:

 - Price Verification: Manually verify the automated pricing model's outputs against an open-source site like Zillow. This spot-check will ensure the automated prices are comparable to what has recently sold or is currently for sale in that market.

 - Data Quality Control: Implement a "confidence factor" for the LLM name-formatting tool. This rating will allow the team to manually review low-confidence results (e.g., under 70%) and spot-check data integrity before committing to a mailing.

Conclusion: A Call to Action 

Adopting this integrated model provides a clear benefit to any land investor by increasing the volume of high-quality leads, which will directly increase profit. The system saves money by eliminating mailings to undesirable areas. Furthermore, when interested sellers respond, the front-end work is already done; the investor knows they own land in a pre-vetted target area. This saves valuable time and money, solving the client's initial problem of marketing inefficiency.
