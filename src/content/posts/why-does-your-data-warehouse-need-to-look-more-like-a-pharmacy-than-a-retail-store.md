---
title: "Why does your Data Warehouse need to look more like a pharmacy than a retail store?"
seoTitle: "Data Warehouse Governance: Control Access Like a Pharmacy"
seoDescription: "Uncontrolled self-service data access leads to conflicting metrics and siloed reporting. Data engineers should act as stewards, guiding consumers to..."
datePublished: 2024-04-15T21:06:33.789Z
dateUpdated: 2026-03-02T10:53:13.020Z
cover: "/images/why-does-your-data-warehouse-need-to-look-more-like-a-pharmacy-than-a-retail-store/cover.jpg"
coverCredit:
  name: "Nathaniel Yeo"
  url: "https://unsplash.com/@nathanielyeo"
series: "my-data-journey"
canonical: "https://www.notjustsql.com/p/why-does-your-data-warehouse-need"
hashnodeCuid: "clv1g3bul000j08l7axa6b486"
---

I was following a discussion about the “Self-Service paradox”. Then I've seen another LinkedIn post about the random 'one-off' requests.

And then memories just poured in.

When I just started working in Analytics a decade ago, I was pretty hyped up with this idea of data democratization. As an analyst with too much time on my hands, I thought: with the right infra in place, everyone interested can access all data in the org (minus sensitives of course) and uncover some “insights” that will help improve how things work. Data is fair game for everyone.

## The reality of data democratization

Time flies. I’ve picked up SQL and with a couple of years of experience, I was working as a Business Intelligence Developer, working across multiple business areas and industries. The reality struck me.

Even apparently (for my unprepared mind) straightforward things like revenue, there was not any consensus on how it should be calculated. One person might think of it as revenue once the order has been placed, another once it was paid for and yet another one it was handed out for delivery. Or delivered? You get the idea.

Then, I could get odd ‘one-off’ request asking for this or that piece of data. Aggregated at this level, filtering out X and Y. They’re all the same but equally different. People would build entire siloed ecosystems of their own, report packs, presentation decks, all sourced from ‘raw data’ provided by engineers. It became clear that this is not a sustainable track.

Why was this happening? Maybe the analyst wasn’t comfortable with SQL or with the self-service tools of the time like SSAS Cubes + Pivots in Excel. Perhaps there is no data dictionary in place so people don't know what these columns represent. And what are these huuuge integer keys for?

Does this amount include tax or not? How about shipping? What about returns?

Or maybe this data hasn't landed yet in the Data Warehouse and we are due to integrate it sometimes Q3 in 2 years. Or maybe they don't trust out transformations?

Without proper controls, this *free-for-all* leads to conflicting metrics, a skewed understanding of how good a company is doing and overall, and overall, different yardsticks doing the measurements.

With regards to the analogy I’ve used in the title, I believe that the we should treat our Data Warehouse more like a pharmacy and less like a retail store.

Surely, there are over-the-counter products, MDs and treatments. But every one of those comes with instructions and a number of dedicated professionals that can guide and help you when needed. And for some you need a prescription.

I'm very happy when someone uses the data that I help deliver. We have a duty to act as stewards and custodians for the data we are entrusted to process, including the Analytical products it is feeding. Not restrict and keep exclusive to our silos, but inform, educate, collaborate and build for better business outcomes.

*Found it useful? Check out to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
