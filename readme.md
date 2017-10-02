# Logs Analysis Project

logs_analysis is a reporting tool written in python that connects to a database and uses SQL queries to analyze the information in it and answer questions about the site's user activity.The database contains newspaper articles, as well as the web server log for the site.

### Tables
logs_analysis use a PostgreSQL database: **news**.
The database includes three tables:
  - The **authors** table includes information about the authors of articles.
  - The **articles** table includes the articles themselves.
  - The **log** table includes one entry for each time a user has accessed the site.

### Description of the column names

Table *log*

 | Column | Type |
 | ------ | ------ |
 | path   | text |
 | ip     | inet |
 | method | text |
 | status | text |
 |time   | timestamp |
 | id | integer - PRIMARY KEY |

Table *authors*

 | Column | Type |
 | ------ | ------ |
 | name   | text |
 | bio    | text  |
 | id     | integer - PRIMARY KEY|

Table *articles*

 | Column | Type |
 | ------ | ------ |
 | author | integer |
 | title  | text |
 | slug   | text -  UNIQUE CONSTRAINT |
 | lead   | text |
 | body   | text |
 | time   | timestamp |
 | id     | integer - PRIMARY KEY |

##### Foreign-keys :
- **articles**(*author*) REFERENCES **authors**(*id*)

### Views

- **populars** : Includes the total views of each article.
This view is a result of a join between **articles** and a **select**. The *select* will return how many times the URLs was accessed successfully ( *status='200 OK'*) ordered by the most access.
    ```
        create view populars as
            select author,title, views
            from articles, (select path, count(*) as views
            from log where status='200 OK'
            group by path order by views DESC) as subq
            where path like '%' || slug || '%')
    ```
- **requests** : Includes how many times a user try to access the site each day.
    ```
        create view requests as
            select date(time) as day,count(*) as t_request
            from log
            group by day
            order by day
    ```
- **fails** : Includes how many times a user fails to access the site each day.
    ```
        create view fails as
            select date(time) as day,count(*) as f_request
            from log
            where status like '4%' or status like '5%'
            group by day
            order by day
    ```

### How to use it
The program run from the command line. It won't take any input from the user.
```sh
$ python logs_analysis.py
```
It will connect to a [PostgreSQL] database.
[Download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
To load the data use the command:
```
$ psql -d news -f newsdata.sql.
```
### Program's design
The program uses the psycopg2 module to connect to the database.
```
import psycopg2
```
It print out the answers to 3 questions. Includes one function for each question:
```
def popular_3_articles()
def popular_article_authors()
def lead_to_errors()
```


License
----

MIT


**Free Software**

   [PostgreSQL]: <http://www.postgresqltutorial.com/install-postgresql/>
