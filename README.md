## Inspiration
This project was inspired by the vast amount of data available in the [NYC Open Data](https://opendata.cityofnewyork.us/). We started with the idea of trying to understand the satisfaction of people within the neighborhood, we wanted to understand how sustainability indicators impacted people. 

We live in NYC and we all have had experiences wit
## What it does
**Summary: We allow you to compare the sustainability of a building in New York to a group of its peers, creating an overall rank and a comparison by individual indicators.**

Our project is able to lookup addresses in NYC, with an active autocomplete feature. Once you have selected a building, we present overview facts about the property: building usage, square footage, energy star score, and number of 311 complaints (NYC system of building complaints for residential buildings). 

We give the option to compare the building to similar building cohorts in NYC either buildings of same usage and size or buildings in the same neighborhood. Within these cohorts we provide a number of graphs to understand where the building falls within the the distribution of GHG emissions intensity (intensity is per square foot), Water usage intensity, Electricity usage intensity, Natural Gas usage intensity, energy star score, and number of 311 complaint if residential.

We also provide scores for all the buildings within the cohort using an aggregate indicator of sustinability.
## How we built it
Our database is in MySQL. Our web framework is Django. On frontend, we use Django, Bootstrap and JQuery.

For data, it is all taken from [NYC Open Data](https://opendata.cityofnewyork.us/). We use [NYC geosearch](https://geosearch.planninglabs.nyc/) for autocomplete of addresses. 

We used R for creating the mathematical and statistical sub-indicators that are processed into the absolute score and then the relativistic rank.
## Challenges we ran into
We pivoted thrice.

First pivot, we were originally thinking of doing a securitized masters, and we had already done a lot of math but we found that someone had already done the same thing and was funded by a VC.

Next, we wanted to pivot to doing a LEED dashboard (a sustainability and tax credit scheme), however, we realized it would be hard to do what we wanted and automatically score buildings for LEED because of lack of training data and complex indicators.

Then, we pivoted to our current idea.
## Accomplishments that we're proud of
First hackathon, so we are very happy to complete a product. Pretty happy with the data structure design.
## What we learned
Learned a lot about the process of ideation, and how to research effectively before deciding on an idea.

We also learned a lot about sustainability indicators and tax credits.
## What's next for Building Rank
We want to add a view for contractors, to view buildings in the bottom of their cohorts and their contact information and key area of improvement needed, so it can be a business development tool for the contractors. 
