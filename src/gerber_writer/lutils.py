# adf
import inspect    # for debug reporting

debug = False
def report_with_line(s):
    if debug:
        print(f'line {inspect.currentframe().f_back.f_lineno} {s}')


def isreal(x):
    return isinstance(x, float) or isinstance(x, int)
