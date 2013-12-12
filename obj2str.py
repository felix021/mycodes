#coding:utf-8

#author: felix021
#date: 2013-12-12
#把Python中与json兼容的基础对象dump出来，尽量兼容json。

legal_types = set([int, long, float, list, dict, tuple, str, unicode, bool, type(None)])
rep_groups  = [('\\', '\\\\'), ('"', '\\"'), ('\r', '\\r'), ('\n', '\\n'), ('\t', '\\t')]

def obj2str(obj, encoding='utf-8'):
    otype = type(obj)
    if otype not in legal_types:
        raise Exception('unknown type: ' + str(otype))
    if obj is None:
        return 'null'
    if obj is True:
        return 'true'
    if obj is False:
        return 'false'
    if otype in [int, long, float]:
        return str(obj)
    if otype in [list, tuple]:
        return '[%s]' % ', '.join([obj2str(x) for x in obj])
    if otype is dict:
        return '{%s}' % ', '.join(\
            ['%s: %s' % (obj2str(k), obj2str(v)) for k, v in obj.iteritems()])
    if otype is unicode:
        obj = obj.encode(encoding)
    for pat, rep in rep_groups:
        obj = obj.replace(pat, rep)
    return '"' + obj + '"'

if __name__ == "__main__":
    #test case
    obj = {
        '你': {
            '好': ['吗', '？'],
            2   : 1.5, 
            '1"2\\3\'': 1,
            "1'2\\3\"": ["\r\n", "\r", "\n", "\t"],
        },
        1: [True, False, None, 123456789012345678901234567890L]
    }

    ret = obj2str(obj)
    print ret
    if obj == eval(ret, {'true': True, 'false': False, 'null': None}):
        print 'ok!'
    else:
        print 'error!'
