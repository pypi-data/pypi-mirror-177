import cx_Oracle
from django.db import connection


def update_consumed_limit_from_lms_views(national_id, limit_from_workflow):
    count = 0
    loanAmount = 0
    if limit_from_workflow:
        for data in limit_from_workflow['data']:
            if data['loanAccountNo']:
                current_bal = check_in_local_views(data['loanAccountNo'])
                if current_bal:
                    # count += 1
                    loanAmount += abs(current_bal)
                else:
                    count += 1
                    loanAmount += data['loanAmount']
            else:
                count += 1
                loanAmount += data['loanAmount']

    return loanAmount, count



def check_in_local_views(loan_acct_num):
    cursor = connection.cursor()
    cursor.execute('''select CURRENT_BAL from fec_dbsync_generalaccount where LOAN_ACCT_NUM = "''' + loan_acct_num + '"')
    rows = cursor.fetchall()

    if rows and rows[0]:
        return rows[0][0]
    return None

def check_in_remote_views(loan_acct_num):
    remote_connection = cx_Oracle.connect('robo_mobile/robomobile_2018@10.30.11.128:1521/LMSUAT2')
    cursor = remote_connection.cursor()
    cursor.execute("select CURRENT_BAL from custom.robo_gam_view where LOAN_ACCT_NUM = '" + loan_acct_num + "'")
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

def get_int(input_value):
    if isinstance(input_value, str):
        if check_int(input_value):
            return int(input_value)
    return 0

def check_int(input_value):
    if isinstance(input_value, str):
        if input_value[0] in ('-', '+'):
            return input_value[1:].isdigit()
        return input_value.isdigit()
    return False
