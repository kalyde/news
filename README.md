# Log Analysis Project
news is a reporting tool that prints out reports in plain text based on that data in the database.

## Install
To load the data, download newsdata.zip file use the command `psql -d news -f newsdata.sql`

## Usage
Run the python `news.py` file and it will export a **text.txt** file with the results.

## Views
Two views were created to find the percentage of requested errors on each day.

##### bad_request view
`create view bad_request as select cast(time as date), count(*) as num
    from log
    where status = '404 NOT FOUND'
    group by cast(time as date)
    order by cast(time as date);`

##### total_request view
`create view total_request as select cast(time as date), count(*) as num
    from log
    group by cast(time as date)
    order by cast(time as date);`

## License

The content of this repository is licensed under a [Creative Commons Attribution License](https://creativecommons.org/licenses/by/4.0/).