
# OTA Yellow Tickets

This project aims to read a parquet file from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page, perform aggregation and visualization.

Aggregation is done via both pandas and PostgreSQL query, visualization is done via mathplotlib.




## Installation

Ensure you have properly install Python >=3

```bash
  cd ota_yellowtickets
  python3 -m venv venv
  pip install -r requirements.txt
```

## Setup Database

```bash
  Download and install PostgreSQL from https://www.postgresql.org/download/
  This installer comes with pgAdmin
  Once installed, open pgAdmin and there will be a default server
  Within the default server, create a database called "ota"
```

## Running the application
This repository comes with default input file in app/storage/input which is downloaded from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

This will run in approx 50 to 70 seconds on machine with high-end CPU and RAM

```bash
  python3 main.py
```

## Results

Once the application is done running, you will see the output files in app/storage/ouput, there will be 2 files:

csv file - this contains the aggregated result

png file - this contains the visualization result


You can also check the pgAdmin -> ota database -> trip_data table, this contains the filtered data which is passenger_count > 0

Now to query the same aggregated result as the csv file in app/storage/output, we need to run the aggregate.sql query in pgadmin

There will be 2 queries:

check date difference - to check the difference betwenn tpep_pickup_datetime and tpep_dropoff_datetime, this is to check that the pickup date and dropoff date happened within the same day or within 24 hours, meaning we are safe to assume that the total amount is wihin that day

AGGREGATE BY pickup date - i only used tpep_pickup_datetime for aggregation since i assumed the same day pickup and dropoff, the result of this query will be the same as the csv file in app/storage/output