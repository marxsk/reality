# coding=utf-8
from pprint import pprint
from sets import Set

def csvPrint(fields, record):
    values = []
    for f in fields:
        values.append(unicode(record.get(f, '')))

    print(u'Ā'.join(values))

def printAdv(records, output_type):
    if output_type == 'csv':
        fields = Set([])
        for record in records:
            fields = fields.union(record.keys())
        sorted_fields = sorted(fields)

        print (u'Ā'.join(sorted_fields))
        for record in records:
            csvPrint(sorted_fields, record)
    else:
        for record in records:
            pprint(record)

def renameKey(dic, oldKey, newKey):
    if oldKey in dic:
        dic[newKey] = dic[oldKey]
        dic.pop(oldKey)