#!/usr/bin/env python3

# A reporting tool that prints out reports
# based on the data in the database news

import psycopg2


DBNAME = "news"


def popular_3_articles():
    """ Return the most popular three articles """
    try:
        database = psycopg2.connect(dbname=DBNAME)
        cursor = database.cursor()
        cursor.execute("select title, views from populars limit 3;")
        articles = cursor.fetchall()
        database.close()
        return articles
    except Exception:
        return []


def popular_article_authors():
    """ Return the most popular article authors """
    try:
        database = psycopg2.connect(dbname=DBNAME)
        cursor = database.cursor()
        cursor.execute(""" select name,sum(views) as tviews
                           from populars, authors
                           where id = author
                           group by id
                           order by tviews DESC;""")
        articles = cursor.fetchall()
        database.close()
        return articles
    except Exception:
        return []


def lead_to_errors():
    """ Return the days where more than 1% of requests lead to errors  """
    try:
        database = psycopg2.connect(dbname=DBNAME)
        cursor = database.cursor()
        cursor.execute(""" select day, percent from
                           (select requests.day,
                           round(f_request*100/t_request::numeric,2) as percent
                           from requests,fails
                           where requests.day=fails.day) as result
                           where percent >= 1;""")
        articles = cursor.fetchall()
        database.close()
        return articles
    except Exception:
        return []

print("\n\tInternal Reporting Tool\n")
# The most popular three articles
print("\n1. What are the most popular three articles of all time? \n")
for title, view in popular_3_articles():
    print("-\"" + title + "\" -> " + str(view) + " views\n")

# The most popular article authors
print("\n2. Who are the most popular article authors of all time? \n")
for name, tview in popular_article_authors():
    print("-" + name + " -> " + str(tview) + " views\n")

# Days where more than 1% of requests lead to errors
print("\n3. On which days did more than 1% of requests lead to errors?\n")
for day, error in lead_to_errors():
    print("-" + str(day) + " -> " + str(error) + "% errors\n")