
def imprime():
    print("Imprimiendo la función imprime")


def generate_series(start, stop, interval):
    return pandas.date_range(start,stop-timedelta(days=1),freq=interval)
    
def tablesUnion(datesList, table_dir, date_format = "%d/%m/%Y", date_split="/"):
    '''Devuelve el dataframe formado por la union de todos los datos en el path table_dir para todas las fechas en la lista datesList.
    Si todas las tablas están vacías, devuelve null'''
    error = "Error a unir datos de la tabla "+table_dir+" para las fechas: "
    cont_error = 0
    print(datesList)

    for fecha in datesList:
        print(fecha)
        try:
            date_items = fecha.strftime(date_format).split(date_split)
            print(table_dir+"/YEAR="+str(date_items[-1]) + (str("/MONTH=") + str(int(str(date_items[-2]))) if len(date_items)>1 else '') + (str("/DAY=") + str(int(str(date_items[-3]))) if len(date_items)>2 else '') + "/")
            new_df = spark.read.parquet(table_dir+"/YEAR="+str(date_items[-1]) + (str("/MONTH=") + str(int(str(date_items[-2]))) if len(date_items)>1 else '') + (str("/DAY=") + str(int(str(date_items[-3]))) if len(date_items)>2 else '') + "/")
            try:
                df = df.union(new_df)
            except Exception as e:
                if "is not defined" in str(e) or "referenced before" in str(e):
                    df = new_df
                else:
                    raise Exception(e)
        except Exception as e:
            error += (str(fecha)+", ")
            cont_error+=1
    if cont_error > 0:
        print(str(error))
    try:
        return df
    except Exception as e:
        return None

def S3_to_RS(s3_path, redshift_schema,redshift_table, format_conn,rs_url,tempdir, datesList, date_format="%d/%m/%Y"):
    join = tablesUnion(datesList, s3_path, date_format)

    try:
        df_rs=spark.read.format(format_conn) \
            .option("url", rs_url) \
            .option("query", "SELECT * FROM " + redshift_schema + "." + redshift_table) \
            .option("tempdir", tempdir) \
            .option("forward_spark_s3_credentials", "true") \
            .load()
        # cast data to db schemas
        for i in range(len(join.schema.names)):
            join = join.withColumnRenamed(join.schema.names[i],df_rs.schema.names[i])

        for i in join.dtypes:
            try:
                if 'decimal' in i[1]:
                    join = join.withColumn(i[0],join[i[0]].cast('float'))
            except Exception as e:
                print(e)
        join.write.format(format_conn) \
            .option("url", rs_url) \
            .option("dbtable", redshift_schema + "." + redshift_table) \
            .option("tempdir", tempdir) \
            .option("forward_spark_s3_credentials", "true") \
            .option("tempformat", "CSV") \
            .option("csvnullstring", "") \
            .mode('append').save()
    except Exception as e:
        if "'NoneType' object has no attribute" in str(e):
            print("No hay datos en S3 para añadir a RS desde "+s3_path)
            sys.exit(0)
        else:
            raise Exception(e)
    
def imprime():
    print("Imprimiendo la función imprime")