#!/usr/bin/env python3

import psycopg2


DBNAME = "news"  # database name


def get_popular_titles():
    """Prints three most popular articles of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # counting views that had status 200
    c.execute("select articles.title, count(*) as views "
              "from articles, log "
              "where log.path like concat('%', articles.slug, '%') "
              "and log.status = '200 OK' "
              "group by articles.title "
              "order by views desc limit 3")
    results = c.fetchall()
    text_file = open("text.txt", "a+")  # append to text file
    text_file.write("The three most popular articles of all time are:\n\n")
    # for loop to print each article
    for title, views in results:
        text_file.write("\"" + title + "\"" + " - " + str(views) + " views\n")
    text_file.write("\n")
    text_file.close()
    db.close


def get_popular_authors():
    """Prints the most popular article authors of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # counting views that had status 200
    c.execute("select authors.name, count(*) as num "
              "from articles, authors, log "
              "where articles.author = authors.id "
              "and log.path like concat('%', articles.slug, '%') "
              "and log.status = '200 OK' "
              "group by authors.name order by num desc")
    results = c.fetchall()
    text_file = open("text.txt", "a+")  # append to text file
    text_file.write("The most popular authors of all time are:\n\n")
    # for loop to print each author
    for name, num in results:
        text_file.write("\"" + name + "\"" + " - " + str(num) + " views\n")
    text_file.write("\n")
    text_file.close()
    db.close


def createview_total_request():
    """Creates view for total request of articles."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # counting all requests status 200 and 404
    c.execute("create view total_request as select cast(time as date), "
              "count(*) as num "
              "from log "
              "group by cast(time as date) "
              "order by cast(time as date)")
    db.commit()
    db.close()


def createview_bad_request():
    """Creates view for bad request of articles."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # counting only status 404
    c.execute("create view bad_request as select cast(time as date), "
              "count(*) as num "
              "from log "
              "where status = '404 NOT FOUND' "
              "group by cast(time as date) "
              "order by cast(time as date)")
    db.commit()
    db.close()


def get_error_days():
    """Prints days with request with more than 1% bad requests."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    # dividing views of bad requests and total request to get percentage
    c.execute("select bad_request.time, "
              "(bad_request.num * 1.0 / total_request.num) as errors "
              "from bad_request, total_request "
              "where bad_request.time = total_request.time "
              "and (bad_request.num * 1.0 / total_request.num) > 0.01")
    results = c.fetchall()
    text_file = open("text.txt", "a+")  # append to text file
    text_file.write("Day(s) where more than 1 percent of requests were errors:"
                    "\n\n")
    for time, errors in results:
        text_file.write(time.strftime('%B %d, %Y') + " - " +
                        str(errors * 100)[:3] + "% errors\n")
    text_file.write("\n")
    text_file.close()
    db.close()


get_popular_titles()
get_popular_authors()
createview_total_request()
createview_bad_request()
get_error_days()
