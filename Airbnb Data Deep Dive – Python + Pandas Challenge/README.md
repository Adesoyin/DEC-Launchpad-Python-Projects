# DEC-Launchpad-AirBNB Data Deep Dive
## Project Summary
Making data-driven decisions and recommending suitable homes or rooms to guests based on comfort preferences can be challenging when underlying data is unclean or poorly analyzed. This project leverages Airbnb data — a marketplace connecting property owners with guests seeking unique stays — to perform data cleaning, transformation, and analysis in Python. The goal was to extract insights and enhance decision-making accuracy by ensuring data quality and interpretability.

## Dataset
The [listings dataset](https://data.insideairbnb.com/united-kingdom/england/london/2025-06-10/visualisations/listings.csv) for London was used as the dataset simply due to its large dataset size and variety compared to other cities.

**Fields Description** 

| **Field**                          | **Meaning / Description**                              | **Missing (%)** | **Notes / Interpretation**                                              |
| ---------------------------------- | ------------------------------------------------------ | --------------- | ----------------------------------------------------------------------- |
| **id**                             | Unique identifier for each listing                     | 0.00            | Used as the primary key for the dataset.                                |
| **name**                           | Title or name of the Airbnb listing                    | 0.00            | Usually contains a short description of the property.                   |
| **host_id**                        | Unique identifier for the host                         | 0.00            | Used to link multiple listings under one host.                          |
| **host_name**                      | Name of the host                                       | 0.04            | Minimal missing values; could be anonymized.                            |
| **neighbourhood_group**            | Broader area or region grouping neighborhoods          | 100.00          | Entirely missing — might not be included in this city’s dataset.        |
| **neighbourhood**                  | Specific local area or community of the listing        | 0.00            | Useful for geographical or neighborhood-based analysis.                 |
| **latitude**                       | Latitude coordinate of the listing                     | 0.00            | Used for map visualization or spatial clustering.                       |
| **longitude**                      | Longitude coordinate of the listing                    | 0.00            | Used with latitude for location mapping.                                |
| **room_type**                      | Type of room offered (e.g., Entire home, Private room) | 0.00            | Key factor for pricing and guest preferences.                           |
| **price**                          | Price per night (in local currency)                    | 35.14           | Has missing values; critical for financial analysis and recommendation. |
| **minimum_nights**                 | Minimum nights required to book the listing            | 0.00            | Helps determine booking flexibility.                                    |
| **number_of_reviews**              | Total number of reviews received by the listing        | 0.00            | Indicates popularity and guest engagement.                              |
| **`last_review`**                    | Date of the most recent review                         | 26.04           | Missing for listings with no reviews. Should be converted to datetime.  |
| **reviews_per_month**              | Average number of reviews per month                    | 26.04           | Often missing for new or inactive listings.                             |
| **calculated_host_listings_count** | Number of listings owned by the same host              | 0.00            | Identifies multi-listing hosts (professionals vs individuals).          |
| **availability_365**               | Number of days in a year the listing is available      | 0.00            | Helps categorize hosts as active or occasional.                         |
| **number_of_reviews_ltm**          | Reviews received in the last 12 months                 | 0.00            | Measures recent listing performance and activity.                       |
| **license**                        | License or registration ID for the listing             | 100.00          | Often missing; depends on local regulations or dataset source.          |


## Data Ingestion
Requests would be used in extracting the dataset from the API link. Check the `airbnb_listings_london.csv` file to see output of the ingestion.

## Data Exploration & Cleaning
**Observation**
1. The dataset has 18 columns of which 6 are of type float64, 7 of type `int64`, and 5 columns are of type string. 
2. The number of rows are 96,651 and number of columns are 18. 
3. licence and neighbourhood group are null throughout the whole dataset giving 100% missing percentage. Hence, these columns would not be needed in the analysis. 
4. host name, last review and review/month has 26, 26 and 35 % missing percentage respectively which is over 10% recommended.
5. Last review comes as object/string data type which is supposed to be date datatype, likewise, 
6. There are no duplicated row in the dataset. The result of `data[data.duplicated()]` gave 0 value

## Data Cleaning

The `last_review` column, originally stored as a string, was converted to a date format to enable proper date-based operations and analysis.

The license field, which was completely empty, was dropped as it provided no analytical value. Although the neighbourhood_group column was also empty, an attempt was made to populate it using the Geopy library through reverse geocoding. However, this approach proved inefficient, as the process took hours without completing successfully. Instead, the unique neighbourhoods present in the dataset were extracted, and their corresponding districts (boroughs) were obtained online. A mapping dictionary was then created and merged with the dataset using the neighbourhood field as a key to derive the appropriate neighbourhood_group for each location.

The host_name field had approximately 26% missing values. Since this is an analytical project rather than a predictive one, deleting the column would have resulted in significant loss of valuable information. Given that all host_id values were present, unique pairs of non-missing host_id and host_name were extracted and used to populate missing host names by merging on host_id.

__It is important to note that imputing missing values using statistical measures such as mean or mode would introduce inaccuracies and compromise the integrity of the raw dataset. The goal here is not to artificially fill gaps but to preserve data integrity, as missingness itself may carry meaningful information for business insights.__

The string fields host_name and host_id were deduplicated before propagation, while the numeric field reviews_per_month had its missing values replaced with the `average value of 0.5.

`Although all records in the price column had valid non-zero values, about 31% of listings were not available to guests year-round. These unavailable listings were excluded from further analysis to maintain data consistency (see detailed output in airbnb.ipynb).

After cleaning, the dataset was reduced to 66,488 rows, representing a cleaner, more reliable dataset for subsequent analysis

## Data Enrichment
To better analyse the data and be able to make informed decisions, the dataset was more enriched;

1. By creating a field called `price_per_booking` which is gotten by multiplying the minimum night a guest can stay in a room by the list price. This would help to estimate the expected revenue from that room and ultimately, the total expected revenue in a year.

2. `availability_bucket` field created to categorize the Number of days in a year the listing is available for booking. This translates to that when the number of days the listing is available in a year is less than 100, we categorize it as a rare availability room , if between 100 and 300, it's counted as part time and any days above 300 makes the room always a full time listing. 

## Data Analysis

1. Top 10 most expensive neighborhoods based on `average price

An analy`sis of the ten most expensive neighbourhoods reveals a clear pricing gradient across London. Westminster, Kensington and Chelsea, Lambeth, and the City of London top the list, with `average minimum night p`rices ranging between `$340 and $380, highlighting their premium accommodation demand and central location appeal. `Camden and Islington` fall into a moderate pricing band of $218–$230, suggesting balanced demand with a mix of affordability and accessibility. In contrast, Brent, Richmond upon Thames, Wandsworth, and Hammersmith & Fulham maintain relatively lower rates between $165 and $200, reflecting more residential or suburban market dynamics compared to central zones.

2. Average availability and price across different room type

The analysis shows that, on `average, hotel rooms co`mmand the highest minimum night price at approximately $310, while shared rooms are the most affordable, averaging around $83 per night. Across all room types, `average annual availabi`lity falls within the 198 to 261-day range, classifying them as part-time listings throughout the year. Interestingly, while shared rooms are the cheapest option, they exhibit the highest availability, indicating that hosts may rely on extended listing periods to maintain competitiveness and occupancy.

3. Top host with the highest listings

To identify which host has the most listings and ensure data accuracy, two approaches were considered:

    1. Using calculated_host_listings_count – This field shows the number of listings Airbnb records for each host, but it is repeated or outdated across rows.

    2. Counting listings directly from the dataset – This method counts how many times each host_id appears, providing an actual total based on the data available.

Both values were compared side by side to confirm consistency and detect any discrepancies. This check ensures that host-level analyses, such as identifying top hosts or understanding listing distribution, are based on reliable and accurate data. For both methods, the host with the most listings is LuxurybookingsFZE with 495 listings while there are discrepancies in some other hosts count. check the output of the analysis on `airbnb.ipynb`

4. Price Distribution across Districts

The `average price per night` is highest in Central London ($291), followed by West London ($249) and South London ($237) — reflecting their proximity to key attractions and commercial areas. Prices gradually decline moving outward, with South West, North West, East, North, and South East London showing more affordable averages ranging between $125 and $172, indicating a clear price gradient from the city center to the outer districts.

5. Unreviewed Listings Analysis

To understand listing engagement levels, the ``last_review`` column was analyzed to identify properties that have never been reviewed by guests. Listings with missing values (NaN) in the `last_review` field were counted as unreviewed.

The calculation involved counting all missing `last_review` entries and determining their proportion relative to the total number of listings in the dataset.

This metric helps reveal the share of hosts or properties with little to no guest interaction (26%), which may indicate newly added listings, low visibility, or poor demand.

## Key Insights

**Central London dominates high-end pricing**
Premium neighbourhoods such as Westminster, Kensington and Chelsea, and City of London command the highest average nightly prices (ranging from $340–$380), reflecting their strong demand and central appeal. In contrast, suburban areas like Wandsworth and Brent show more moderate pricing below $200.

**Hotel rooms yield the highest nightly rates**
Among all room types, hotel rooms are the most expensive at an average of $310 per night, while shared rooms are the cheapest at around $83. Despite their lower price, shared rooms show the highest availability, suggesting they remain open longer to attract bookings.

**Top host dominates the listing market**
LuxurybookingsFZE is identified as the top host with 495 active listings, confirming consistency between actual counts and Airbnb’s recorded listing data. This highlights a small group of hosts holding significant market share within the London Airbnb ecosystem.

**Clear price gradient across London districts**
A distinct downward trend is observed in average prices from Central London ($291) toward outer districts like South East London ($125), reinforcing the relationship between location centrality and accommodation cost.

**Over one-fourth of listings remain unreviewed**
About 26% of listings have never received a guest review, indicating either newly created listings, underperforming hosts, or properties with limited visibility. This insight highlights potential areas for platform optimization and host performance improvement.



