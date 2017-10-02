#!/usr/bin/env python3

# A reporting tool that prints out reports
# based on the data in the database news

import psycopg2


DBNAME = "news"


def popular_3_articles():
    """ Return the most popular three articles """
    statement="select title, views from populars limit 3;"
    print("\n1. What are the most popular three articles of all time? \n")
    for title, view in fetch_data(statement):
        print("-\"" + title + "\" -> " + str(view) + " views\n")

def popular_article_authors():
    """ Return the most popular article authors """
    statement=""" select name,sum(views) as tviews
                           from populars, authors
                           where id = author
                           group by id
                           order by tviews DESC;"""
    print("\n2. Who are the most popular article authors of all time? \n")
    for name, tview in fetch_data(statement):
        print("-" + name + " -> " + str(tview) + " views\n")


def lead_to_errors():
    """ Return the days where more than 1% of requests lead to errors  """
    statement=""" select to_char(day,'FMMonth FMDD, YYYY'), percent from
                           (select requests.day,
                           round(f_request*100/t_request::numeric,2) as percent
                           from requests,fails
                           where requests.day=fails.day) as result
                           where percent >= 1;"""
    print("\n3. On which days did more than 1% of requests lead to errors?\n")
    for day, error in fetch_data(statement):
        print("-" + str(day) + " -> " + str(error) + "% errors\n")


def fetch_data(statement):
    """ Connects to the database and performs the specified query (statement) """
    try:
        database = psycopg2.connect(dbname=DBNAME)
        cursor = database.cursor()
        cursor.execute(statement)
        articles = cursor.fetchall()
        database.close()
        return articles
    except Exception as e:
        print(e)
        return []


if __name__ == "__main__":
    print("\n\tInternal Reporting Tool\n")
    popular_3_articles()
    popular_article_authors()
    lead_to_errors()
