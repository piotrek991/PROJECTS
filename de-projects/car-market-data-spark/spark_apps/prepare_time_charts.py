from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, LongType, TimestampType, DateType
from pyspark.sql.functions import *
from collections import OrderedDict
from datetime import datetime


def generate_case_statements(buckets_dict: dict, mod_dict: dict, val_diff: dict = None):
    try:
        inner_keys = set(buckets_dict.keys()).intersection(set(mod_dict.keys()))
        assert not set(buckets_dict.keys()).symmetric_difference(set(mod_dict.keys()))
    except AssertionError as e:
        print(f"one of columns is not declared either in mod_dict or buckets_dict")
    f_case_list = list()
    for key in inner_keys:
        buckets_dict_inner = buckets_dict[key]
        mod_value_inner = mod_dict[key]

        ord_dict = OrderedDict(sorted(buckets_dict_inner.items(), reverse=True))
        inner_case_statement = f"WHEN CAST(({key} / {mod_value_inner}) as INT) >= {{mod_val}} THEN '{{col_value}}'"
        inner_cast_statement_mod_val = f"WHEN CAST((({key} + ({{sub_diff}})) / {mod_value_inner}) as INT) >= {{mod_val}} THEN '{{col_value}}'"
        final_case_statement = str()
        for num, (mod, val) in enumerate(ord_dict.items()):
            if val_diff.get(key):
                final_case_statement = final_case_statement + inner_cast_statement_mod_val.format(mod_val=mod,
                                            col_value=val, sub_diff=val_diff.get(key)) + '\n'
            else:
                final_case_statement = final_case_statement + inner_case_statement.format(mod_val=mod, col_value=val) + '\n'
        final_case_statement = "CASE " + final_case_statement \
                               + f"ELSE NULL END as {key}_categorized"
        f_case_list.append(final_case_statement)
    return f_case_list


spark = SparkSession.builder.appName('time_analyze').getOrCreate()
spark.sparkContext.setLogLevel("WARN")
data_schema = StructType([
    StructField('el_id', LongType(), False)
    , StructField('notice_name', StringType(), False)
    , StructField('engine_capacity', StringType(), False)
    , StructField('engine_power', StringType(), False)
    , StructField('price_str', StringType(), False)
    , StructField('mileage', IntegerType(), False)
    , StructField('fuel_type', StringType(), False)
    , StructField('gearbox', StringType(), False)
    , StructField('production_year', IntegerType(), False)
    , StructField('when_added', TimestampType(), False)
    , StructField('ds1_rest', StringType(), False)
    , StructField('extract_date', DateType(), False)
])

data_df = spark\
    .read\
    .option("timestampFormat", "dd-MM-yyyy HH:mm:ss")\
    .option("dateFormat", "dd-MM-yyyy")\
    .schema(data_schema).csv('/opt/spark/data/cars_data_*.csv', header=True)

raw_transformed = data_df.withColumn("price_str", expr("trim(price_str)")) \
    .withColumn("engine_power", expr("substr(trim(engine_power), 1 ,length(trim(engine_power)) - 3)")) \
    .withColumn("engine_capacity", expr("replace(trim(engine_capacity), ' ', '')")) \
    .withColumn("engine_capacity", substr(col("engine_capacity"), lit(1), length(col("engine_capacity")) - 3)) \
    .withColumn("notice_name", expr("trim(notice_name)")) \
    .withColumn("brand", trim(regexp_extract(col("notice_name"), r'(^[\p{L}\-]+\s)', 1)))
### notices count per hour ###
day_time_analyse = raw_transformed.selectExpr("extract_date", "hour(when_added) as hour")\
    .groupBy(["extract_date", "hour"])\
    .count()\
    .withColumnRenamed("extract_date", "extract_date_j")
n_unique_dates = raw_transformed.select("extract_date").distinct()
temp_df = spark.createDataFrame([[(list(range(24)))]], ['num']) \
    .crossJoin(n_unique_dates) \
    .withColumn("num", explode("num"))
day_time_analyse = broadcast(day_time_analyse).join(temp_df
                                                    , (col("hour") == col("num"))
                                                    & (col("extract_date") == col("extract_date_j"))
                                                    , how="right") \
    .withColumn("hour", coalesce(col("hour"), col("num"))) \
    .withColumn("count", coalesce(col("count"), lit(0))) \
    .drop("num").groupBy("extract_date").agg(collect_list("count").alias("count")
                                             , collect_list("hour").alias("hour_list")
                                             )
### brand count ###
week_day_analyse = day_time_analyse\
    .withColumn("count", explode("count"))\
    .withColumn("day_of_week", date_format(col("extract_date"), "EEE"))\
    .drop("hour_list", "extract_date")\
    .groupBy("day_of_week").agg(sum("count").alias("total_notice_count"))

### all atributes count/avg ###
mods = {
    "engine_power": 100
    , "engine_capacity": 500
    , "production_year": 5
    , "price_str": 20000
    , "mileage": 50000
}
mod_diff = {
    "production_year": -2000
}
buckets = {
    "engine_power": {
        0: "low"
        , 1: "medium"
        , 2: "high"
        , 3: "very high"
    }
    , "engine_capacity": {
        0: "very small"
        , 1: "small"
        , 2: "medium"
        , 3: "bigger medium"
        , 4: "big"
        , 5: "very big"
        , 6: "huge"
    }
    , "production_year": {
        0: "2000s"
        , 1: "2005s"
        , 2: "2010s"
        , 3: "2015s"
        , 4: "2020s"
        , 5: "2025s"
    }
    , "price_str": {
        0: "20ks"
        , 1: "40ks"
        , 2: "60ks"
        , 3: "80ks"
        , 4: "100ks"
        , 5: "120ks"
        , 6: "140ks"
        , 7: "160ks"
        , 8: "180ks"
        , 9: "200ks"
        , 10: "200k+s"
    }
    , "mileage": {
        0: "50ks"
        , 1: "100ks"
        , 2: "150ks"
        , 3: "200ks"
        , 4: "250ks"
        , 5: "300ks"
        , 6: "300k+s"
    }
}
exclude_col = ["el_id", "notice_name", "when_added", "ds1_rest"]
bucket_col = set(mods.keys()).intersection(set(buckets.keys()))

s_exclude_col = set(exclude_col)
s_exclude_col.update(bucket_col)

cols_sel_onl = set(raw_transformed.columns).difference(s_exclude_col)
cols = list(map(lambda x: x + "_categorized", list(bucket_col)))

select_expr_dyn = generate_case_statements(buckets, mods, mod_diff)
select_expr_dyn_f = select_expr_dyn + list(cols_sel_onl)
print(f"select expr dyn_f {select_expr_dyn_f}")
group_by_dyn_f = cols + list(cols_sel_onl)

group_no_date = group_by_dyn_f.copy()
group_no_date.remove("extract_date")

categorized_data = raw_transformed.selectExpr(*select_expr_dyn_f).cube(*group_by_dyn_f).count()\
    .filter(col("extract_date").isNotNull())\
    .withColumn("raw_array", array(*group_no_date))\
    .withColumn("non_null", array_compact(col("raw_array")))\
    .filter(size(col("non_null")) == 1)\
    .select("*", posexplode("raw_array").alias("pos", "exploded_raw"))\
    .filter(col("exploded_raw").isNotNull())\
    .withColumn("col_list", lit(group_no_date))\
    .withColumn("dict_like", array(struct(lit("col_name").alias("attr_name"), element_at("col_list", col("pos") + lit(1)).alias("attr_val"))
                                   , struct(lit("group").alias("attr_name"), col("exploded_raw").alias("attr_val"))
                                   , struct(lit("group_count").alias("attr_name"), col("count").cast("string").alias("attr_val"))
                                   ))\
    .select("extract_date", "dict_like")
print("SAVING DATA")
categorized_data.repartition(4).write.partitionBy("extract_date").mode("overwrite").parquet(f"/opt/spark/data/data_cars_comb_{datetime.now().strftime('%Y%m%d')}")




