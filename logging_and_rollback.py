# Adv DB Winter 2024 - 1

import random
import copy
import csv
import datetime

data_base = []  # Global binding for the Database contents
'''
transactions = [['id1',' attribute2', 'value1'], ['id2',' attribute2', 'value2'],
                ['id3', 'attribute3', 'value3']]
'''
transactions = [['1', 'Department', 'Music'], ['5', 'Civil_status', 'Divorced'],
                ['15', 'Salary', '200000']]
DB_Log = [] # <-- You WILL populate this as you go


## Global Variables
transaction_num = 0

transaction_id_index = 0
transaction_attribute_index = 1
transaction_value_index = 2

log_transaction_id_index = 0
log_table_index = 1
log_attribute_index = 2
log_before_image_index = 3
log_after_image_index = 4
log_status_index = 5
log_timestamp_index = 6
log_user_id_index = 7

header_index = 0

def recovery_script(log:list): 
    '''
    Restore the database to stable and sound condition, by processing the DB log.
    '''
    print("Calling your recovery script with DB_Log as an argument.")
    print("Recovery in process ...\n")

    global data_base
    for entry in log:
        #Find the failed entry
        if entry[log_status_index] == 'FAILED':
            before_image = entry[log_before_image_index]
            instance_id = int(before_image[log_transaction_id_index])
            data_base[instance_id] = before_image
            if(export_to_csv()):
                entry[log_status_index] = 'ROLLEDBACK'

            break

    
    print("Recovery completed.\n")

def transaction_processing(index:int):
    '''
    1. Process transaction in the transaction queue.
    2. Updates DB_Log accordingly
    3. This function does NOT commit the updates, just execute them
    '''

    log_entry = create_log_entry(index)
    DB_Log.append(log_entry)
    process_transaction(index)

## Helper Functions 

def create_log_entry(transaction_id:int)->list:
    '''
    log_entry = [transaction_id, table, attribute, before_image, after_image, status, timestamp, user_id]
    '''
    global data_base
    instance_id, attribute, value, attribute_index = unpack_transaction(transaction_id)
    before_instance = copy.deepcopy(data_base[instance_id])

    return [transaction_id + 1, 'table', attribute, before_instance, get_updated_instance(before_instance, attribute_index, value), 'PENDING', datetime.datetime.now().isoformat(), 'user_id']

def get_transaction_id()->str:
    global transaction_num
    transaction_num += 1
    return f'T{transaction_num}'

def get_updated_instance(instance:list, attribute_index:int, value:str)->list:
    updated_instance = copy.deepcopy(instance)
    updated_instance[attribute_index] = value
    return updated_instance

def get_time_stamp()->str:
    '''
    Return a placeholder for the time stamp
    '''
    return '2024-01-01 12:00:00'

def process_transaction(index:int): 
    '''
    Commit the updates to the database
    '''
    instance_id, _, value, attribute_index = unpack_transaction(index)
    update_data_base(instance_id, attribute_index, value)
    
        
def update_data_base(instance_id:int, attribute_index:int, value:str):
    global data_base
    data_base[instance_id][attribute_index] = value

def update_DB_log(status:str, index:int):
    global DB_Log
    DB_Log[index][log_status_index] = status

def unpack_transaction(index:int)->object:
    '''
    Unpack all transaction information used in a log entry and database update
    '''
    global data_base

    transaction = transactions[index]
    instance_id = int(transaction[transaction_id_index])
    attribute = transaction[transaction_attribute_index]
    attribute_index = data_base[header_index].index(attribute)
    value = transaction[transaction_value_index]

    return instance_id, attribute, value, attribute_index
    
def export_to_csv():
    try:
        with open('./Employees_DB_ADV_After.csv', 'w') as file:
            writer = csv.writer(file)
            for row in data_base:
                writer.writerow(row)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return True

def export_DB_Log():
    with open('./DB_Log.csv', 'w') as file:
        writer = csv.writer(file)
        for row in DB_Log:
            writer.writerow(row)

#--------------------------------------------#

def read_file(file_name:str)->list:
    '''
    Read the contents of a CSV file line-by-line and return a list of lists
    '''
    data = []
    #
    # one line at-a-time reading file
    #
    with open(file_name, 'r') as reader:
    # Read and print the entire file line by line
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            line = line.strip().split(',')
            data.append(line)
             # get the next line
            line = reader.readline()

    size = len(data)
    print('The data entries BEFORE updates are presented below:')
    for item in data:
        print(item)
    print(f"\nThere are {size} records in the database, including one header.\n")
    return data

def is_there_a_failure()->bool:
    '''
    Simulates randomly a failure, returning True or False, accordingly
    '''
    value = random.randint(0,1)
    if value == 1:
        result = True
    else:
        result = False
    return result

def main():
    number_of_transactions = len(transactions)
    must_recover = False
    global data_base
    data_base = read_file('Employees_DB_ADV.csv')
    
    failure = False
    failing_transaction_index = None
    while not failure:
        # Process transaction
        for index in range(number_of_transactions):
            transaction_processing(index)
            print(f"\nProcessing transaction No. {index+1}.")    #<--- Your CODE (Call function transaction_processing)
            print("UPDATES have not been committed yet...\n")
            failure = is_there_a_failure()
            if failure:
                must_recover = True
                failing_transaction_index = index + 1
                update_DB_log('FAILED', index)
                print(f'There was a failure whilst processing transaction No. {failing_transaction_index}.')
                break
            else:
                if(export_to_csv()):
                    update_DB_log("COMMITTED",index)
                    
                print(f'Transaction No. {index+1} has been commited! Changes are permanent.')
        break
        
       
    if must_recover:
        #Call your recovery script
        recovery_script(DB_Log) ### Call the recovery function to restore DB to sound state
    else:
        # All transactiones ended up well
        print("All transaction ended up well.")
        print("Updates to the database were committed!\n")

    export_DB_Log()

    # print('The data entries AFTER updates -and RECOVERY, if necessary- are presented below:')
    print("\nData Base:")
    for item in data_base:
        print(item)

    print('\nDB_Log:')
    for item in DB_Log:
        print(item)

main()


