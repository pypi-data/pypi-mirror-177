def upload_s3(full_path, model):
    return model.save(full_path)


def download_model_s3(kmeans_model, full_path):
    return kmeans_model.load(full_path)


def s3_full_path(base_url, dir_path, date, model_name):
    return base_url.format(dir_path, date, model_name)


def download_from_s3(session, s3_path):
    df = session.read.csv(s3_path, inferSchema=True)
    df.printSchema()
    df.show(10)


def spark_session(spark_session, app_name):
    return spark_session.builder.config("spark.driver.extraClassPath", "/usr/share/java/postgresql-jdbc.jar").appName(
        app_name).getOrCreate()


def set_hadoop_s3(sc, accessKeyId, secretAccessKey):
    hadoopConf = sc._jsc.hadoopConfiguration()
    hadoopConf.set('fs.s3a.access.key', accessKeyId)
    hadoopConf.set('fs.s3a.secret.key', secretAccessKey)
    hadoopConf.set('fs.s3a.endpoint', 's3-ap-northeast-2.amazonaws.com')
    hadoopConf.set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')

def uppsert_opensearch(username, password, df, index_name, select_columns, url):
    print('uppsert_opensearch')
    df.show(10)
    df.select(select_columns).write.format('org.elasticsearch.spark.sql') \
        .option("es.nodes",
                url) \
        .option("es.port", 443) \
        .option("es.nodes.wan.only", "true") \
        .option("es.net.http.auth.user", username) \
        .option("es.net.http.auth.pass", password) \
        .option("es.write.operation", "index") \
        .option("es.batch.size.bytes", "100mb") \
        .option("es.batch.size.entries", 10000) \
        .option("es.batch.write.retry.wait", "30s") \
        .option("es.mapping.id", "id") \
        .option("es.resource", "{index}/_doc".format(index=index_name)) \
        .mode("append") \
        .save()

