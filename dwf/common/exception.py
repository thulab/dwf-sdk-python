#
# DataWay SDK
# Author: peizhongyi(peizhyi@gmail.com)
# Initial Date: 2018.06.16
#
# Title: DWFException
#
# Version 0.1
#


class DWFException(Exception):
    def __init__(self, status, msg):
        self.STATUS = status
        self.MSG = msg
        Exception.__init__(self, msg)


'''
Unknown Exceptions
'''
UNDEFINE = DWFException(1, '发现未定义异常')

'''
Exceptions for Parameters
'''
PARAM_LACK = DWFException(2001, '缺少参数')
PARAM_WRONG_TYPE = DWFException(2002, '参数类型错误')

'''
Exceptions for Database
'''
DATABASE_CONN_FAIL = DWFException(3001, '数据库连接错误')
NUM_RESULT_MISMATCH = DWFException(3002, '查询记录结果数不符合预期')
ILLEGAL_REPEATED_FILED = DWFException(3003, '字段不可重复')
NON_EXISTING_ALGORITHM = DWFException(3004, '算法不存在')
NON_EXISTING_DATA_PATTERN = DWFException(3005, '数据模式不存在')
NON_EXISTING_PACKAGE = DWFException(3006, '包不存在')

'''
Exceptions for Files
'''
FILE_NOT_EXIST = DWFException(4001, '文件不存在')
FILE_FORMAT_ERROR = DWFException(4002, '文件格式不符合预期')

'''
Exceptions for Development
'''
NOT_IMPLEMENTED = DWFException(5001, '方法未实现')

'''
Exceptions for Algorithms
'''
ALGORITHM_NAME_EXISTED = DWFException(6001, '算法重名')