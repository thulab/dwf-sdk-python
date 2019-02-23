__prefix__ = '----LOG of Test Framework----'
__except__ = '<Except>'
__assert__ = '<Assert>'
__info__ = '<Info>'
__warning__ = '<Warn>'

import traceback
import sys

__tb__ = sys.exc_info()[2]

'''
    Check the cases and do all.
    Args:
        tester - a unittest instance of unittest.TestCase
        cases - the cases defined as instances of TestCase
'''


def check_and_do_cases(tester, cases):
    count = 0
    success = 0
    for member in dir(cases):
        if member.startswith('testcase_'):
            test_func_name = getattr(cases, member).template
            count += 1
            try:
                if test_func_name not in dir(tester):
                    msg = 'No matched test function found for %s!' % (test_func_name)
                    tester.assertTrue(False, 'Template name may be wrong! \n %s' % msg)
                try:
                    before_test(tester, getattr(cases, member).name, test_func_name)
                except Exception as e:
                    msg = 'Error in before_test for case %s of %s: ' % \
                          (getattr(cases, member).name, test_func_name)
                    print_log(msg=msg, level=__warning__, exception=e)
                msg = 'Run the case %s of %s...' % (getattr(cases, member).name, test_func_name)
                print_log(msg=msg)

                getattr(tester, test_func_name)(getattr(cases, member).data)

                msg = 'Good! Finish the case %s of %s.' % (getattr(cases, member).name, test_func_name)
                print_log(msg=msg)
                success += 1
            except AssertionError as e:
                msg = 'Error in case %s of %s: ' % (getattr(cases, member).name, test_func_name)
                print_log(msg=msg, level=__assert__, exception=e)
            except Exception as e:
                msg = 'Error in case %s of %s: ' % (getattr(cases, member).name, test_func_name)
                print_log(msg=msg, level=__except__, exception=e)
            try:
                after_test(tester, getattr(cases, member).name, test_func_name)
            except Exception as e:
                msg = 'Error in after_test for case %s of %s: ' % (getattr(cases, member).name, test_func_name)
                print_log(msg=msg, level=__warning__, exception=e)

    counting = '\nPassed Cases:\t%d. \n' \
               'Failed Cases:\t%d. \n' \
               % (success, count - success)
    if count != success:
        tester.assertTrue(False, 'Found error in cases. \n %s \nPlease check the error log! \n ' % counting)
    else:
        if count == 0:
            msg = 'Sorry! No cases are found! \n %s' % counting
        elif count == 1:
            msg = 'Congratulations! Only one case is found. It is OK. \n %s' % counting
        else:
            msg = 'Congratulations! All %d cases are OK. \n %s' % (count, counting)
        print_log(msg=msg)


def print_log(msg, level=__info__, exception=None):
    if exception is not None:
        print('%s %s %s' % (__prefix__, level, msg), exception)
        traceback.print_exc()
    else:
        print('%s %s %s' % (__prefix__, level, msg))


'''
    Do something before the case.
    Args:
        tester - a unittest instance of unittest.TestCase
        cases - the cases defined as instances of TestCase
'''


def before_test(tester, case_name, test_func_name):
    tester.prepare_data()


'''
    Do something after the case.
    Args:
        tester - a unittest instance of unittest.TestCase
'''


def after_test(tester, case_name, test_func_name):
    for instance in reversed(tester.to_be_deleted):
        try:
            tester.test_db_session.delete(instance)
            tester.test_db_session.commit()
        except Exception as e:
            print('%s %s Happened for deleting %s for case %s of %s: ' %
                  (__prefix__, __except__, instance, case_name, test_func_name), e)
