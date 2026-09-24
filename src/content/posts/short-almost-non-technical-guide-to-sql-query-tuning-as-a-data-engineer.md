---
title: "Short, almost non-technical guide to SQL query tuning as a Data Engineer"
subtitle: "It's not all about those fancy details."
seoTitle: "SQL Query Tuning for Data Engineers: Non-Technical Guide"
seoDescription: "A non-technical walkthrough of SQL query tuning for data engineers, covering early filtering, data reduction, partition usage, and avoiding unnecessary..."
datePublished: 2024-06-19T21:57:26.989Z
dateUpdated: 2026-03-02T10:53:09.520Z
cover: "/images/short-almost-non-technical-guide-to-sql-query-tuning-as-a-data-engineer/cover.jpg"
coverCredit:
  name: "Laura Ockel"
  url: "https://unsplash.com/@viazavier"
series: "practical-sql"
canonical: "https://www.notjustsql.com/p/short-almost-non-technical-guide"
hashnodeCuid: "clxmdj51p000209l773oe53wx"
---

So I spend quite a bit of time optimizing SQL data processing pipelines in BigQuery. Scale-wise, I might have an occasional encounter with a 10TB table. I have limited knowledge on what it does 'under the hood', but I find that there's a couple of simple, common sense things you can do from the start.

So here's my thinking when I'm trying to optimize such a problematic query.

## Work with less

The simplest and most efficient optimization is to work with less data from the beginning. Perhaps you don't need that much data for the task you're performing.

Say you're processing month-over-month calculations. Do you really need that 3-year old data processed in this query? If not, filter those rows out.

How about the columns? Do you really need those? Keep only what you need.

## Do less work

Another big trick is to ensure there is less work do be done. So, can you rewrite the problem you're solving in a way that makes it easier to find the answer (even for you as a human with a pen & paper / Excel )?

For example, I'd always try to limit the number of column I aggregate by, keeping only the essential. I wouldn't need the customer's country and city when aggregating their transactions, I can always look up that later.

Or take Window Functions. They take quite a toll on the performance at these high volumes. So I would use them sparingly. Check out [this example](/practical-bigquery-filling-in-missing-data) of how I've replaced multiple WINDOW function calls with just a single one + PIVOT.

Also, aim to reduce the number of rows that you are working with as early as possible - that is, push aggregation as early as possible.

## Is there any repetitive work involved?

Is there any part of the processing that you see is done multiple times? It doesn't need to be identical, but can you find a way to make the computation happen just once? Can you re-purpose a staging table to to serve multiple needs at the same time?

In a more practical fashion, a normal (non-recursive) CTE in BigQuery is evaluated once per each each call, so you're effectively doing that work over and over again.

## Can you split things up?

When combining multiple big tables and are doing a lot of operations on this data, things are bound to get ugly.

One way to work around that is to split the process into logical steps and components.

Extract big steps into a separate staging table that is as barebones as possible but is properly partitioned and clustered (on indexed, depending on your platform).

## Is there any underlying problem making the data that big?

I’ve recently was struggling with optimizing something that produced a 17TB table, only to realise that the data sources are nowhere that big - and a bad join made the data volume to explode.

So maybe performance is not your main problem to fix?

## Check for yourself

Pick a representative data slice. Turn off query caching in your window. Try out different approaches and work out which one is the best.

Check for different data volumes. Do you findings till hold? As learned multiple times on my own skin, test your assumptions and pick a best approach based on empirical results.

## Think about maintainability

While this is second-to-last, it should rank closer to the top in terms of importance. Is whatever you’ve achieved there understood by your peers in the team, or whoever might come to replace you? Will they be able to maintain, extend or fix your solution should the conditions change?

No one likes black boxes, so make sure to do document the ‘what’ and ‘why’ of your work, ensuring your actions have a positive net impact on the process in its lifetime.

## In lieu of a conclusion: invest your time wisely

Trying to optimize something can be interesting. Time will fly by. Don't get yourself sucked in and keep an eye on the end target. Is all this effort on optimization worth it? Don't spent days of working to save 5$ in processing costs.

Perhaps you should prioritize improving a scheduled query running every 2 hours than a vastly bigger one that is used for yearly reporting?

After all, the smaller one runs 12 \* 365 = 4380 times a year, so a small saving here might mean a big difference in the grand scheme of things.
