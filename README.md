## Live Dashboard
https://ecommerce-discount-analysis-dashboard.streamlit.app

# E-Commerce Discount Analysis

A data analysis project studying discount patterns across Indian e-commerce platforms.

## Overview
This project scrapes, cleans and analyses product discount data from Flipkart and Shopsy to understand how discounts vary across categories and platforms.

## Data Collection
- Scraped using Python (Selenium + BeautifulSoup)
- Platforms: Flipkart and Shopsy
- Categories: Mobiles, Laptops, Headphones
- Total products: 386

## Key Findings
- Headphones have highest average discount (63%)
- Flipkart offers higher discounts than Shopsy
- Budget products get more discounts than premium ones
- Average customer savings: Rs 6,420

## Tools Used
- Python, Selenium, BeautifulSoup
- Pandas, Matplotlib, Seaborn, Plotly
- Scikit-learn (Linear Regression)
- Jupyter Lab

## Project Structure
- web_scraping/ — scraper notebooks
- data_cleaning/ — cleaning notebook
- EDA/ — analysis and charts
- dashboard/ — interactive Plotly charts
- model_building/ — prediction model
