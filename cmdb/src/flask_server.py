#!/usr/bin/python3
import pymysql
from flask import Flask, request, abort, jsonify
import textwrap
import json

def sql_query(query):
    query_results = []
    con = pymysql.connect( host="localhost", user="user1", passwd="user1", db="historical" )
    with con:
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            row_data = ""

            #print ("{0}\t {1}\t {2}".format(row[0], row[1], row[2]))
            for item in row:
                row_data = row_data + str(item) + ","
            query_results.append(row_data)

    con.close()
    return(query_results)


def build_sql_results_html(query_string):
    sql_results = ""
    #query_string = "SELECT filer, path, access_or_modify,\
    #SUM(005_day_data+010_day_data+015_day_data+020_day_data+025_day_data+030_day_data+035_day_data+040_day_data+045_day_data+050_day_data+055_day_data+060_day_data+065_d
    #ay_data+070_day_data+075_day_data+080_day_data+085_day_data+090_day_data+095_day_data+100_day_data+105_day_data+110_day_data+115_day_data+120_day_data+125_day_data+130_da
    #y_data+135_day_data+140_day_data+145_day_data+150_day_data+155_day_data+160_day_data+165_day_data+170_day_data+175_day_data+180_day_data) \
    #AS TOTAL FROM volume_usage WHERE access_or_modify = 'MODIFIED' GROUP BY filer, path, access_or_modify HAVING TOTAL > 0 AND TOTAL < 10000001"

    print ("Query String: " + query_string)
    
    query_string_parts = query_string.split(" ")
    print (query_string_parts)
    my_table_headers = []
    print (my_table_headers)
   
    if (query_string_parts[0] == "show"):
        print ("verb is show")
        for noun in query_string_parts:
            print ("looping string query parts")
            if (noun != 'show'):
                print (noun)
                my_table_headers.append(noun.upper())
                   
    print ("query_string parts select? "+ query_string_parts[1])

    if (query_string_parts[1].lower() == "select"):
        print ("verb is select")
        query_string_select = query_string.split(",")
        for column in query_string_select:
            if ("select" in column):
                my_string = column.replace("select ","",1)
                my_table_headers.append(my_string)          
            elif ("sum" in column):
                my_table_headers.append("TOTAL")
                break  
            elif ("as" in column):
                break
            elif ("from" in column):
                break
            elif ("where" in column):
                break
            elif ("having" in column):
                break
            elif ("group" in column):
                break           
            else:
                my_table_headers.append(column)
                
                
    print ("table headers: ", my_table_headers)
    print (my_table_headers)
    

    sql_results = sql_results + "<h2>SQL Results:</h2>"
    query_string_display = textwrap.wrap(query_string, width=80)
    wrapped_str = ""
    for line in query_string_display:
        wrapped_str = wrapped_str + line + "\n"
        
    sql_results = sql_results + "<p><p><b>For mySQL query:</b><p>" + str(wrapped_str) + "<p><p>"
    sql_results = sql_results + '<table style="width:100%" border="1"><tr>'
    
    for column in my_table_headers:
        sql_results = sql_results + "<th><b><u>" + column.upper() + "</u></b></th>"
    
    return(sql_results)

#print ("================= Starting Flask - init values ==========================")
#head = Node()

app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/do_sql_query' , methods=['POST'])
def do_sql_query():
    #if request.is_json == True:
    #print ("do_sql_query....")
    #sql_query_test = request.get_json()
    #print ("sql query sent to this server was: ")
    if request.is_json == True:
        query_string_json  = request.data
        query_string_list = query_string_json.decode().split(":")
        query_string_list[1] = query_string_list[1].rstrip()
        query_string_list[1] = query_string_list[1].replace("\\n", "")
        query_string_list[1] = query_string_list[1].replace("\\", "")
        print (query_string_list)
        query_string = query_string_list[1]
        query_string = query_string[:-1] # drop last character which is "

        #print (query_string)

        query_string_list = query_string_json.decode().split(":")

    

    if query_string == "":
        return jsonify({"data" : "Error - no query string typed or pasted into ENTER MYSQL QUERY"})

    if ("SELECT " in query_string or "SHOW " in query_string):
        pass
    elif ("select " in query_string or "show " in query_string):
        pass
    else:
        return jsonify({"data" : "Error - SQL Query must start with SELECT"})

    query_string = query_string.strip('\n')
    query_string = query_string.strip('\t')
    query_string = query_string.lower()


    try:
        query_results = sql_query(query_string)
    except:
        #print ("SQL query may be malformed. Try again.")
        #return "<p><b>SQL query may be malformed. Try again.</b>"
        return jsonify({"data" : "SQL query may be malformed. Try again."})
        #return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    sql_results = build_sql_results_html(query_string)

    for item in query_results:
        fields = item.split(",")
        fields.pop()
        sql_results = sql_results + "<tr>"
        for column in fields:
            sql_results = sql_results + "<td>" + column.strip() + "</td>"
        sql_results = sql_results + "</tr>"

    #return app.send_static_file('query.html')
    #return app.send_static_file('index.html')
    #print (sql_results)
    #return("test 123 to sql output")
    #return ("<h1>Response from Flask</h1>")
    #return sql_results
    return jsonify({"data" : sql_results})
    #return json.dumps({success:'True', data':sql_results}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':

    #print send_search_request_to_splunk("test123")
    #exit (0)
    #print ("running....")




    # Will make the server available externally as well
    app.run(host='0.0.0.0')
    #print ("Exited...")



    #app.run(host='localhost', port=8000, debug=True, use_reloader=False)
    #print ("Exited...")
    
    