
import csv
from io import StringIO
from pathlib import Path
from typing import List

import pandas
import sqlalchemy
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from sqlalchemy import create_engine

from app.provider.config import ConfigProvider
from app.provider.file import FileProvider
from app.provider.timer import TimerProvider


def psql_insert_copy(table: pandas.io.sql.SQLTable, conn: sqlalchemy.engine.Engine, keys: List[str], data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join(['"{}"'.format(k) for k in keys])
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)
        

if __name__ == '__main__':
    timer = TimerProvider()
    timer.start()

    # get config
    config = ConfigProvider(path=Path('./config.ini'))

    # define input and output
    storage_path = Path(config.payload.get('APP', 'STORAGE_PATH'))
    input = FileProvider(path=Path(storage_path, 'input/yellow_tripdata_2024-01.parquet'))
    output_csv = FileProvider(path=Path(storage_path, 'output/test.csv'))
    output_plot = FileProvider(path=Path(storage_path, 'output/plot.png'))

    # connect to postgresql
    engine = create_engine(config.payload.get('DATABASE', 'URL'))

    # read parquet
    dataframe = pandas.read_parquet(input.payload, engine='pyarrow')

    # filter
    dataframe = dataframe[dataframe['passenger_count'] > 0]

    # save to database
    # approx 200 sec if no method
    # approx 37 secs if method provided with postgres COPY
    dataframe.to_sql(
        name="trip_data",
        con=engine,
        if_exists='replace',
        index=False,
        method=psql_insert_copy
    )

    # format datetime to date
    dataframe['pickup_date'] = dataframe['tpep_pickup_datetime'].dt.strftime('%Y/%m/%d')
    dataframe['dropoff_date'] = dataframe['tpep_dropoff_datetime'].dt.strftime('%Y/%m/%d')

    # filter columns
    dataframe = dataframe[['pickup_date', 'total_amount']]

    # aggregate
    dataframe = dataframe.groupby(by=['pickup_date']).agg({
        'total_amount': 'sum'
    }).reset_index()

    # save to csv
    dataframe.to_csv(output_csv.payload, encoding='utf-8')

    # create plot
    plt.figure(figsize=(15,5))
    plt.xlabel('Pickup dates')
    plt.ylabel('Total amount')
    plt.title('Yellow taxi trip total amount per day')

    plt.plot(dataframe['pickup_date'], dataframe['total_amount'])
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
   
    plt.savefig(output_plot.payload)

    timer.finish()
    timer.log()


    

