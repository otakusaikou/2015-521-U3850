#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
import numpy as np
import os
from subprocess import PIPE, Popen

# Define database information
database = "gis"
host = "localhost"
port = "5432"
user = "postgres"
password = "otaku"

# Build database connection
conn = psycopg2.connect(
    "dbname='%s' user='%s' host='%s' port='%s' password='%s'" % (
        database,
        user,
        host,
        port,
        password))

# Get cursor
cur = conn.cursor()


# Function for uploading shapefile to database
def uploadShp(shp_data):
    tbName = os.path.split(os.path.splitext(shp_data)[0])[1]
    # Drop old table
    cur.execute("DROP TABLE IF EXISTS %s;" % tbName)
    conn.commit()

    cmdStr = """shp2pgsql -s 3826 -c -D -I -W big5 %s %s |\
        psql -h %s -p %s -d %s -U %s""" % (
        shp_data,
        tbName,
        host,
        port,
        database,
        user)

    # Use subprocess to hide output messages
    Popen(cmdStr, shell=True, stderr=PIPE, stdout=PIPE).communicate()

    return tbName


def main():
    # Define source files
    ptSource = "../shp/Schools.shp"
    polySource = "../shp/Stown.shp"

    # Upload shapefiles to database
    ptName = uploadShp(ptSource)
    polyName = uploadShp(polySource)

    # Count number of schools in every town
    sql = """
        SELECT T.townname TOWNNAME, COUNT(S.id) NUM
        FROM %s T, %s S
        WHERE ST_Intersects(T.geom, S.geom)
        GROUP BY T.code, T.townname""" % (polyName, ptName)

    # Execute sql and get results
    cur.execute(sql)
    ans = np.array(cur.fetchall())
    townname = ans[:, 0]
    number = ans[:, 1].astype(int)

    print "Have most schools (%d schools):" % max(number)
    for town in townname[number == max(number)]:
        print " " + town

    print "Have least schools (%d schools)" % min(number)
    for town in townname[number == min(number)]:
        print " " + town

    # Drop tables and close connection to database
    cur.execute("DROP TABLE IF EXISTS %s;" % ptName)
    cur.execute("DROP TABLE IF EXISTS %s;" % polyName)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
