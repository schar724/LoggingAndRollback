# LoggingAndRollback
This is a database management logging and rollback system simultor based off of an RDBMS. A random failure is triggered to simulate a failure in processing a transaction. When a transaction fails
the database is restored to its last stable version before the failed transaction.

## Design Choices
The primary design choice of this project was the structure of the log_entry. <br/>
<br/>
`log_entry = [transaction_id, table, attribute, before_image, after_image, status, timestamp, user_id] ` <br/>
<br/>
My aim for this data structure was to keep it as close to something that would be useful in a real DBMS as possible. Because of this choice, 'table' and 
'user_id' are set as default placeholders. This simulator only has one table and no user_id, however, if this simulator were to be expanded it would almost 
certainly call for these properties. <br/>
The database being written to a .csv file is mimicking the database persisting in secondary memory. With this, the final status of a transaction is not set to 
'COMMITTED' until the writing of the .csv has returned without throwing any errors. <br/>
All data structures are arrays or subarrays.

## Process Description
There are 2 main processes in this simulation: 

### 1) Transaction Processing
  Transaction processing starts with creating an entry in the logs. This includes setting the before and after images, setting a time stamp etc.  
Once the transaction has been processed, the log status is changed from "PENDING" to "COMMITTED". If a failure is detected, the rollback process is triggered.

### 2) Rollback Process
  If the transaction fails, the database is restored to its last stable version. This happened by iterating through the logs to find the "FAILED" transaction. The before_image is taken from this log and used to restore the database to its former stable version. Once the database has been written to a 'secondary memory'(ie. a csv), the status of the transaction is updated to "ROLLEDBACK". The DB_Logs are also exported to a .csv file for review.

## References
  All of this work is my own with the exception of standard file I/O which was either provided for me or found at: <br/>
  https://ioflood.com/blog/python-write-to-csv/ <br/>
  https://timestamp.online/article/how-to-get-current-time-in-python<br/>
