---
title: "How ARRAY() can function as UNPIVOT and UNNEST as PIVOT?"
seoTitle: "ARRAY() vs UNPIVOT & UNNEST for PIVOT"
seoDescription: "Learn how to transform SQL data with ARRAY and UNNEST functions for tasks similar to UNPIVOT and PIVOT operations"
datePublished: 2025-02-13T15:38:58.356Z
dateUpdated: 2026-03-02T10:53:04.099Z
cover: "/images/how-array-can-function-as-unpivot-and-unnest-as-pivot/cover.jpg"
series: "bigquery-arrays-and-structs"
hashnodeCuid: "cm73i90ac000209jvb3927l3l"
---

I’ve come across this SQL transformation multiple times, and it’s an interesting two-way problem.

1️⃣ From columns to rows (ARRAY as UNPIVOT):  
We start with separate timestamps for different lifecycle events. To analyze events dynamically, we reshape them into an ARRAY&lt;STRUCT&gt;—essentially converting columns into rows, similar to UNPIVOT.

2️⃣ From rows back to columns (UNNEST as PIVOT):  
If we have an array of events, we may need to do the opposite — bringing individual event types back into separate columns, similar to PIVOT. We achieve this by UNNESTing the array and using conditional aggregation (aggregation function + CASE WHEN).
