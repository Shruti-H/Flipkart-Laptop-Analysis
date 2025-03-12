# Flipkart Laptop Analysis

## 📌 Overview
This project involves **web scraping** laptop listings from **Flipkart** using Selenium and BeautifulSoup, followed by **data analysis** to derive meaningful insights. The analysis explores pricing, ratings, specifications, and trends in the laptop market.

## 📂 Project Structure
```
📁 FLIPKART
├── 📂 Data                 # Scraped laptop data stored as CSV
│   ├── flipkart_laptops_full.csv
│
├── 📂 Logs                 # Logs for web scraping
│   ├── flipkart_scraper_YYYYMMDD.log
│
├── 📂 Scripts              # Contains web scraping and analysis scripts
│   ├── flipkart_scraper.py      # Selenium-based web scraper
│   ├── Flipkart_DA.ipynb        # Data analysis notebook
│
└── README.md               # Project documentation (this file)
```

## 🛠 Web Scraping with Selenium & BeautifulSoup
The **flipkart_scraper.py** script is used to scrape laptop listings from Flipkart.

- Uses **Selenium WebDriver** to navigate Flipkart pages.
- Extracts details like **laptop name, price, ratings, processor, RAM, storage, screen size, and more**.
- Saves the data into **Data/flipkart_laptops_full.csv**.
- Logs errors and progress in **Logs/**.

### 🔹 How to Run the Scraper
#### 1️⃣ Install Dependencies
```bash
pip install selenium beautifulsoup4 pandas
```

#### 2️⃣ Download & Set Up WebDriver
Ensure you have **ChromeDriver** installed and update the path in `flipkart_scraper.py`.

#### 3️⃣ Run the Scraper
```bash
python Scripts/flipkart_scraper.py
```

The scraped data will be saved in `Data/flipkart_laptops_full.csv`.

---

## 📊 Data Analysis
The analysis is conducted in **Flipkart_DA.ipynb**, using Pandas and Matplotlib..

### 🔍 Key Questions Answered
1. **Which brands dominate the listings?** *(Intel vs AMD comparison)*
2. **What are the most common RAM & storage configurations?**
3. **How does laptop price vary with RAM size & processor generation?**
4. **What are the most expensive & budget-friendly laptops?**
5. **Which laptops have the highest & lowest ratings?**
6. **What features are common in highly-rated laptops?**

### 📈 Visualizations
- **Bar charts,line charts, scatter plots, and pie charts** are used to display insights.
- **Correlation analysis** helps identify trends.

---

## 🚀 How to Run the Analysis
#### 1️⃣ Install Dependencies
```bash
pip install pandas numpy matplotlib
```
#### 2️⃣ Open Jupyter Notebook
```bash
jupyter notebook
```
#### 3️⃣ Run the `Flipkart_DA.ipynb` notebook.

---

## 🔥 Key Insights
- **Intel dominates the processor market**, followed by AMD.
- **Most laptops have 8GB or 16GB RAM and SSD storage.**
- **Higher processor generations correlate with higher prices (but weakly).**
- **Budget-friendly laptops mostly belong to ASUS & Primebook.**
- **Highly-rated laptops tend to have SSDs, backlit keyboards, and longer battery life.**

---

## 📌 Future Scope
- Expand scraping to **other e-commerce sites** (Amazon, Croma, etc.).
- Perform **sentiment analysis** on customer reviews.
- Build a **laptop recommendation system** using scraped data.

---

## 🌟 Contributions
Feel free to fork this repo, suggest improvements, or add new analysis! 🎉

