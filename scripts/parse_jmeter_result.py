
import sys

with open(f'../data/jmeter_result_table_{sys.argv[1]}.csv', 'r') as jmeter_input, open(f'../data/parsed_jmeter_result_table_{sys.argv[1]}.csv', 'w') as output:
    for r in jmeter_input.readlines():
        if 'closed_loop_test' not in r:
            output.write(r)


with open(f'../data/parsed_jmeter_result_table_{sys.argv[1]}.csv', 'r') as jmeter_log, open(f'../data/log_db_time_{sys.argv[1]}.csv', 'r') as db_log:
    
    
    
    
    jmeter_log = jmeter_log.readlines()
    db_log = db_log.readlines()
    jmeter_log_fixed = []

    diff = 0
    for i in range(0, max(len(jmeter_log), len(db_log))):
        if '/index' in jmeter_log[i].split(',')[1] and '/index' not in db_log[i-diff].split(',')[2]:
            diff += 1
            print(jmeter_log[i].split(',')[1], db_log[i-diff-1].split(',')[2], i+1)
        else:
            jmeter_log_fixed.append(jmeter_log[i])


    log = zip(jmeter_log_fixed, db_log)

    count = 0
    tot_server = 0
    tot_db = 0
    for x in log:
        count += 1
        tot_server += (int(x[0].split(',')[0]) / 1000) - float(x[1].split(',')[1])
        tot_db += float(x[1].split(',')[1])
        print(round((int(x[0].split(',')[0]) / 1000) - float(x[1].split(',')[1]), 3), x[1].split(',')[2], end='')

    print('Average response time server: ', round(tot_server/count, 3))
    print('Average response time db: ', round(tot_db/count, 3))