# Swedish Company Reports Data Extraction

## Purpose

As economic historians we **LOVE** a historical data series.

We don't love digitizing these by hand, especially when the report format changes from year to year.

What can we do to solve this problem?

Make use of the new GPT-4V model from OpenAI - a model that uses computer vision as one of its core components in addition to taking natural language instruction.

The project involves passing the relevant parts of some PDF company reports to the GPT-4V API and then getting a structured JSON response back. Then we want to extract the relevant info from these JSON files and compile a time series that we can visualize.

## Planning

There are at least 3 steps:

1. Data ingestion: get the PDF documents and break them up into machine readable parts (the text that is contained in the PDF documents is not reliably split between book pages, not perfect) - better to just do the OCR again after splitting double pages.





The project involves ingesting some PDF documents downloaded from the [Historical Archives of the Swedish House of Finance](https://www.hhs.se/en/houseoffinance/data-center/historical-archives/). They require identification for access and with the handful of PDF documents that we want, we can just download them manually.
