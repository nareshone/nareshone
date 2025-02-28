GRP_075_BDS_Assignment
----------------------

Tools used
----------
Oracle VM Virtualbox Manager -> used to create multiple nodes to communicate each other in the cluster. (For 8 nodes, created 8 new instances (m1,m2…m8) with 1 core, 1gb ram, 8gb harddisk)
OS -> Ubuntu 18.04 
HDFS -> To load data in hdfs file system.
Hive -> To create relation tables for the given data file.
Mysql db -> Hive metastore
Spark -> To query the hive tables.
---------------------------------------------------

check the configuration to setup the single node, 2 nodes, 4 nodes and 8 nodes cluster in GRP_075_Main_Document.docx file.

----------------------------------------------------
DDLs/DMLs to load data and read data using hive are present in the GRP_075_DDL_DML.txt file.

-----------------------------------------------------

Used spark scala code to read data from the cluster. Spark scala code present in GRP_075_Spark.scala file.

-----------------------------------------------------