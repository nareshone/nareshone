//Tables and data loaded in hive using command line interface. Querying the hive tables using Sparksql
//importing libraries
import org.apache.spark.examples.sql.hive
import java.io.File
import org.apache.spark.sql.{Row, SaveMode, SparkSession}


object BDS_Assignment {

  case class Record(key: Int, value: String)

  def main(args: Array[String]): Unit = {

    val spark = SparkSession
      .builder()
      .appName("Spark Hive Example")
      .config("spark.sql.warehouse.dir", "/user/hive/bds")
      .enableHiveSupport()
      .getOrCreate()

    import spark.implicits._
    import spark.sql


    // Query to fetch the normalized data by joining all the child tables
    sql("select distinct cd.course_name, ud.university, dld.difficulty_level, cd.course_rating, cd.course_url, cd.course_description, cd.skills from bds.coursera_data cd
left outer join bds.difficulty_level_dim dld on cd.difficulty_level=dld.difficulty_id
left outer join bds.university_dim ud on cd.university=ud.university_id
").show()

    // Query to fetch record from coursera_data table using course_name value
    sql("select * from bds.coursera_data where course_name='Ruby on Rails: An Introduction'").show()


    // Query to fetch record from coursera_dim table using course_id value (It will be faster than the previous sql)
    sql("select * from bds.coursera_dim where course_id=1500").show()


    spark.stop()
    
  }
}