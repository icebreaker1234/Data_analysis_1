# Olist Brazilian E-Commerce Analytics Dashboard

An interactive Streamlit dashboard analyzing the Olist Brazilian e-commerce dataset — covering 99,441 customers and ~118,966 orders across 8 relational tables — to surface revenue trends, customer retention patterns, and product/category performance.

**🔗 Live Demo:** https://olist-data-analysis.streamlit.app/

## Overview

Olist's public dataset ships as 8 separate CSV files (orders, customers, order items, payments, reviews, products, sellers, and category translations). This project merges them into a single analysis-ready dataset and builds a dashboard on top of it to answer real business questions: Where is revenue coming from? Are customers coming back? Which products and categories are actually driving sales?

## Features

- **Geospatial revenue analysis** — choropleth maps of revenue and seller distribution by Brazilian state
- **Customer retention tracking** — repeat-purchase rate calculation (2.99% of ~99K customers are returning buyers)
- **Payment method breakdown** — order volume and share by payment type (credit card, boleto, voucher, debit card)
- **Product category analysis** — revenue treemaps and monthly trend lines for top categories
- **Review score trends** — average review score over time, filterable by state
- **Business insights summary** — translates the analysis into concrete recommendations (regional expansion, retention programs, cross-category bundling)

## Tech Stack

- **Python / Pandas** — merging 8 relational tables, cleaning, aggregation
- **Streamlit** — dashboard framework
- **Plotly** — interactive choropleth maps, treemaps, and time-series charts
- **Matplotlib** — supporting visualizations

## Data Source

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)

## Running Locally

```bash
git clone https://github.com/icebreaker1234/Data_Analysis_2.git
cd Data_Analysis_2
pip install streamlit pandas matplotlib plotly
streamlit run olist_analysis.py
```

Download the Olist dataset CSVs from Kaggle and place them in a `data/` folder before running (update file paths in the script if needed — they are not bundled in this repo due to size).

## Key Finding

Revenue is heavily concentrated in new-customer acquisition rather than repeat business — only ~3% of customers return for a second purchase. This points to an over-reliance on marketing spend for growth and an opportunity to invest in retention (loyalty programs, better post-purchase experience) rather than acquisition alone.
