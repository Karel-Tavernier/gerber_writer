# adf
import inspect    # for debug reporting
def report_with_line(s):
    print('line {} {}'.format(inspect.currentframe().f_back.f_lineno , s))
