#  Air Quality Data Visualization Dashboard

##  Project Overview

This project is an interactive **web-based data visualization dashboard** for analyzing air quality data in selected cities.  
The application enables users to explore and compare air pollution levels using dynamic charts and an interactive map.


##  Features

###  City Management
- City search with API-based autocomplete  
- Add multiple cities to the analysis  
- Remove individual cities dynamically  
- Manage selected cities via a sidebar menu  

###  Time Range Selection
- Select analysis range from **1 to 5 days**  
- Data is based on historical air quality measurements provided by the OpenWeather Air Pollution History API.  
- All visualizations update automatically when the range changes  

###  Visualizations
Users can enable or disable individual visualizations:

- **Line Chart** – hourly PM2.5 concentration over time  
- **Bar Chart** – average PM2.5 values by city  
- **Box Plot** – distribution and variability of PM2.5  
- **Histogram** – frequency distribution of PM2.5 values  
- **Interactive Map** – geographic visualization of selected cities  

###  Map Visualization
- Displays all selected cities  
- Marker size and color represent average PM2.5 concentration  
- Color scale reflects air quality levels based on WHO guidelines  

---

##  Data Source

The application uses data from the **OpenWeather API**:
- **Geocoding API** – for city search and coordinates  
- **Air Pollution History API** – for hourly PM2.5 measurements  


Each observation represents **one hour**, which allows the histogram to be interpreted as the *number of hours* with a given pollution level.

---

##  Technologies Used

- **Python**
- **Streamlit** – web application framework  
- **Plotly** – interactive visualizations  
- **Pandas** – data processing and aggregation  
- **OpenWeather API** – air quality and geolocation data  

---

## ▶️ Running Locally

This project uses the OpenWeather API.  
For security reasons, the API key is **not included in the repository** and must be provided as an environment variable.

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
#### Windows (PowerShell)
```bash
$env:OPENWEATHER_API_KEY="YOUR_API_KEY"
```
#### macOS / Linux
```bash
export OPENWEATHER_API_KEY="YOUR_API_KEY"
```

### 4. Run the application
```bash
streamlit run app.py
```
#### The application will be available at:
```bash
http://localhost:8501
```

## Live Demo

Check out the live version of the application: [Demo](https://air-quality-dashboard-bsjtg9urqmbcpkucapqu7r.streamlit.app/)

