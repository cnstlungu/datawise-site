---
title: "Converting JSON to BigQuery ARRAY and STRUCT"
seoTitle: "Convert JSON to BigQuery ARRAY and STRUCT Types"
seoDescription: "Learn how to convert JSON strings into BigQuery ARRAY and STRUCT types using JSON_VALUE and JSON_EXTRACT_ARRAY."
datePublished: 2022-12-20T22:36:52.136Z
dateUpdated: 2026-03-02T10:51:32.505Z
cover: "/images/converting-json-to-bigquery-array-and-struct/cover.jpg"
coverCredit:
  name: "Iza Gawrych"
  url: "https://unsplash.com/@ilmatar"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "clfmo7acj000009l6d2v6651z"
---

Earlier in 2022 BigQuery introduced native support for the [JSON datatype](https://docs.cloud.google.com/bigquery/docs/json-data). Previously, one would have had to store the JSON data in a string column. This new development opens the door to a lot of interesting use cases, given the widespread adoption and flexibility that this format allows.

Now, what are the trade-offs one would need to consider when choosing between storing the data using the JSON datatype versus the ARRAY and STRUCT data types commonly in BigQuery? I’ve recently come across [a great blog post](https://www.letmesqlthatforyou.com/2020/05/json-vs-structs-vs-columns-in-bigquery.html) comparing these approaches.

My takeaway is that if you’d be willing to give up a little bit on the flexibility of JSON and are not afraid of working with nested data, this might be an interesting choice. There is value to be found here in storage and querying cost savings as well as in easiness of accessing and exploring the data stored. Again, this might vary greatly based on one’s use case, data shape and size.

In this short article, we’re going to do a practical exercise of converting a JSON-containing string / JSON data type into classical BigQuery structures: ARRAYS and STRUCTS.

We’re going to transform this:

```json
{
    "teamName": "teamAlpha",
    "location": {
        "country": "USA",
        "state": "NY",
        "city": "New York"
    },
    "members": [
        {
            "memberName": "member1",
            "age": "25",
            "languageCode": "FR",
            "abilities": [
                "football",
                "cricket",
                "chess"
            ]
        },
        {
            "memberName": "member2",
            "age": "30",
            "languageCode": "EN",
            "abilities": [
                "ping-pong",
                "solitaire",
                "chess"
            ]
        },
        {
            "memberName": "member3",
            "age": "21",
            "languageCode": "DE",
            "abilities": [
                "football",
                "poker",
                "tennis"
            ]
        },
        {
            "memberName": "member4",
            "age": "26",
            "languageCode": "ES",
            "abilities": [
                "weightlifting",
                "cricket",
                "swimming"
            ]
        }
    ]
}
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/b116901eaf9ef92edf2b55148689834a)* 

into this:

![BigQuery result of JSON converted to nested STRUCT and ARRAY: one row with data.team\_name teamAlpha, data.location USA, NY, New York, and repeated data.members member1 to member4 with language\_code FR, EN, DE, ES, age, and an abilities array such as football, cricket, chess.](/images/converting-json-to-bigquery-array-and-struct/1.png)

For that, we’ll need to:

* extract the data using JSON\_VALUE and JSON\_EXTRACT ARRAY (with UNNEST)
    
* create a STRUCT for each JSON object and an ARRAY for each JSON array, and do so from outside to the inside
    
* nest the data, imitating the source and aliasing appropriately
    
* cast the attributes to the appropriate BigQuery datatype
    

```sql
DECLARE jsonstring DEFAULT """

{
    "teamName": "teamAlpha",
    "location": {
        "country": "USA",
        "state": "NY",
        "city": "New York"
    },
    "members": [
        {
            "memberName": "member1",
            "age": "25",
            "languageCode": "FR",
            "abilities": [
                "football",
                "cricket",
                "chess"
            ]
        },
        {
            "memberName": "member2",
            "age": "30",
            "languageCode": "EN",
            "abilities": [
                "ping-pong",
                "solitaire",
                "chess"
            ]
        },
        {
            "memberName": "member3",
            "age": "21",
            "languageCode": "DE",
            "abilities": [
                "football",
                "poker",
                "tennis"
            ]
        },
        {
            "memberName": "member4",
            "age": "26",
            "languageCode": "ES",
            "abilities": [
                "weightlifting",
                "cricket",
                "swimming"
            ]
        }
    ]
}

""";



WITH parsed_json AS 

(
SELECT PARSE_JSON(jsonstring) AS  jsondata 
)

SELECT 

  STRUCT(

    JSON_VALUE(jsondata, "$.teamName") AS team_name,

    STRUCT(

      JSON_VALUE(jsondata, "$.location.country") AS  name,
      JSON_VALUE(jsondata, "$.location.state") AS  state,
      JSON_VALUE(jsondata, "$.location.city") AS  city

          ) AS location,


    ARRAY(

      SELECT STRUCT(

      JSON_VALUE(member, '$.memberName') AS member_name,
      JSON_VALUE(member, '$.languageCode') AS language_code,
      CAST(JSON_VALUE(member, '$.age') AS INT64) AS age,
      ARRAY ( SELECT JSON_VALUE(ability) FROM UNNEST(JSON_EXTRACT_ARRAY(member, '$.abilities')) AS ability) AS abilities

      )

      FROM UNNEST(JSON_EXTRACT_ARRAY(jsondata, "$.members")) AS member

    ) AS members


  ) AS data


FROM parsed_json
```

*[View on GitHub Gist](https://gist.github.com/cnstlungu/cab85d88614398bc6ec30517e5147a18)* 

Notice how above, when extracting an array member (***ability***) from an attribute inside a struct that is inside another array (***members***), we’re using the unnested member as the input to the JSON\_VALUE function

```sql
FROM UNNEST(JSON_EXTRACT_ARRAY(jsondata, "$.members")) AS member

FROM UNNEST(JSON_EXTRACT_ARRAY(member, '$.abilities')) AS ability
```

If we were to save our results to a table, the schema would look as follows:

![BigQuery table schema of the nested result: a data RECORD holding team\_name STRING, a location RECORD (name, state, city), and a REPEATED members RECORD with member\_name, language\_code, age INTEGER and abilities as REPEATED STRING.](/images/converting-json-to-bigquery-array-and-struct/2.png)

Under the right conditions — the absence of a schema drift in the source, volumes big enough to be worth the hassle, multiple nested attributes with arrays, and users trained to interact with nested data — this structure would be more efficient for storage and querying while also allowing for more discoverability of the data. One would not need to study the JSON schema anymore to understand the shape of the data, a simple look at the above schema would suffice.

Thanks for reading!

---

*Enjoyed this? Here are some related articles you might find useful:*

- [Using ARRAY_AGG in BigQuery](/using-array-agg-in-bigquery)
- [UNNESTING ARRAYS in BigQuery](/unnesting-arrays-in-bigquery)
- [Leveraging ARRAYS in BigQuery for query performance](/leveraging-arrays-in-bigquery-for-query-performance)
- [Accessing ARRAY elements in BigQuery](/accessing-array-elements-in-bigquery)
