# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pymongo import MongoClient


def predictWithPolyFunction(x, y):
    z = np.polyfit(x, y, 3)
    p = np.poly1d(z)
    fu_x = np.arange(1, 30, 1)
    fu_y = p(fu_x)
    return fu_y


def getPeriod1(y_pred):
    original_data = pd.DataFrame(y_pred)
    diff_1 = original_data.diff()
    median = original_data.median()

    candidate_indices = []
    for index, row in original_data.iterrows():
        if row[0] < median[0]:
            candidate_indices.append(index)

    possible_candidates = pd.DataFrame(columns=('og_index', 'diff1'))
    for index, row in diff_1.iterrows():
        if index in candidate_indices:
            possible_candidates.loc[possible_candidates.shape[0]] = {'og_index': index, 'diff1': row[0]}

    return int(possible_candidates.iloc[possible_candidates['diff1'].idxmin()]['og_index'])


def getPeriod2(y_pred):
    original_data = pd.DataFrame(y_pred)
    diff_1 = original_data.diff()
    maxnum = original_data.max()

    candidate_indices = []
    for index, row in original_data.iterrows():
        if row[0] < maxnum[0]:
            candidate_indices.append(index)

    possible_candidates = pd.DataFrame(columns=('og_index', 'diff1'))
    for index, row in diff_1.iterrows():
        if index in candidate_indices:
            possible_candidates.loc[possible_candidates.shape[0]] = {'og_index': index, 'diff1': row[0]}

    return int(possible_candidates.iloc[possible_candidates['diff1'].idxmax()]['og_index'])


def getPeriod3(y_pred):
    original_data = pd.DataFrame(y_pred)
    diff_1 = original_data.diff()
    median = original_data.median()

    candidate_indices = []
    for index, row in original_data.iterrows():
        if row[0] > median[0]:
            candidate_indices.append(index)

    possible_candidates = pd.DataFrame(columns=('og_index', 'diff1', 'diff1_abs'))
    for index, row in diff_1.iterrows():
        if index in candidate_indices:
            possible_candidates.loc[possible_candidates.shape[0]] = {
                'og_index': index, 'diff1': row[0], 'diff1_abs': abs(row[0])
            }

    return int(possible_candidates.iloc[possible_candidates['diff1_abs'].idxmin()]['og_index'])


def getPeriod4(y_pred):
    original_data = pd.DataFrame(y_pred)
    diff_1 = original_data.diff()
    diff_2 = diff_1.diff()
    period3 = getPeriod3(y_pred)

    candidate_indices = []
    for index, row in original_data.iterrows():
        if index > period3:
            candidate_indices.append(index)

    possible_candidates = pd.DataFrame(columns=('og_index', 'diff2'))
    for index, row in diff_2.iterrows():
        if index in candidate_indices:
            possible_candidates.loc[possible_candidates.shape[0]] = {'og_index': index, 'diff2': row[0]}

    return int(possible_candidates.iloc[possible_candidates['diff2'].idxmin()]['og_index'])


def verifyPeriod(index_1, index_2, index_3, index_4):
    if index_1 < index_2 < index_3 < index_4:
        return [1, 1, 1, 1]
    elif index_1 < index_2 < index_3:
        return [1, 1, 1, 0]
    elif index_1 < index_2 < index_4:
        return [1, 1, 0, 1]
    elif index_1 < index_3 < index_4:
        return [1, 0, 1, 1]
    elif index_2 < index_3 < index_4:
        return [0, 1, 1, 1]
    elif index_2 < index_3:
        return [0, 1, 1, 0]
    elif index_1 < index_2:
        return [1, 1, 0, 0]
    elif index_1 < index_3:
        return [1, 0, 1, 0]
    elif index_1 < index_4:
        return [1, 0, 0, 1]
    elif index_2 < index_4:
        return [0, 1, 0, 1]
    elif index_3 < index_4:
        return [0, 0, 1, 1]
    else:
        return [0, 0, 1, 0]


def getAllPeriod(num_y):
    x = np.arange(1, 30, 1)
    y = np.array(num_y)
    y_pred = predictWithPolyFunction(x, y)
    index_1 = getPeriod1(y_pred)
    index_2 = getPeriod2(y_pred)
    index_3 = getPeriod3(y_pred)
    index_4 = getPeriod4(y_pred)
    verify_list = verifyPeriod(index_1, index_2, index_3, index_4)
    index_list = [index_1, index_2, index_3, index_4]
    for i in range(4):
        if verify_list[i] == 0:
            index_list[i] = 99

    period_collection = []
    for i in range(29):
        if i == index_list[0]:
            period_collection.append("萌芽期")
        elif i == index_list[1]:
            period_collection.append("成长期")
        elif i == index_list[2]:
            period_collection.append("成熟期")
        elif i == index_list[3]:
            period_collection.append("衰退期")
        else:
            period_collection.append("")

    return period_collection


def connectDatabase():
    client = MongoClient('localhost', 27017)
    database = client['config']
    collection = database['yisuo_english_paper_done']

    return collection


def findKeywordsByThisField(field_require):
    collection = connectDatabase()
    articles = collection.find({'field': field_require})
    field_keyword_list = []
    i = 0
    for article in articles:
        keywords = article['keywords'].split('; ')
        if keywords != ['']:
            i = i + 1
            print('[' + str(i) + '] ' + str(keywords))
            field_keyword_list.extend(keywords)
        if len(field_keyword_list) > 50000:
            break

    return field_keyword_list


def countTechNumber(field, tech):
    collection = connectDatabase()
    years = [
        '1990-01-01', '1991-01-01', '1992-01-01', '1993-01-01', '1994-01-01', '1995-01-01', '1996-01-01',
        '1997-01-01', '1998-01-01', '1999-01-01', '2000-01-01', '2001-01-01', '2002-01-01', '2003-01-01',
        '2004-01-01', '2005-01-01', '2006-01-01', '2007-01-01', '2008-01-01', '2009-01-01', '2010-01-01',
        '2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01', '2017-01-01',
        '2018-01-01',
    ]
    tech_count = []
    for year in years:
        print(field + ':' + tech + ':' + year)
        this_year_count = 0
        articles = collection.find({'field': field, 'year': year})
        for article in articles:
            keywords = article['keywords'].split('; ')
            if tech in keywords:
                this_year_count = this_year_count + 1
        tech_count.append(this_year_count)
        print(this_year_count)

    return tech_count


def generateCSVFiles():
    fields = ['人工智能', '智能制造', '大数据', '云计算', '工业互联网', '网络安全', '集成电路', '物联网']
    list = []
    for field in fields:
        field_list = findKeywordsByThisField(field)
        list.append(field_list)

    count_list = []
    for i in range(8):
        count = {}
        for item in list[i]:
            count[item] = list[i].count(item)
        keyword_count = sorted(count.items(), key=lambda it: it[1], reverse=True)
        count_list.append(keyword_count)

        filename = '_tempfiles/' + str(i) + '_keywords.csv'
        writer = open(filename, 'w')
        i = 0
        for item in keyword_count:
            if (i < 8) and (item[0] != ''):
                writer.write(item[0] + ',' + str(item[1]) + '\n')
                i = i + 1

    return count_list


def readCSVFiles():
    result_list = []
    for i in range(8):
        filename = '_tempfiles/' + str(i) + '_keywords.csv'
        reader = open(filename, 'r')
        tuple_list = []
        for line in reader.readlines():
            item = line.split(',')
            k_tuple = (item[0], int(item[1][0]))
            tuple_list.append(k_tuple)
        result_list.append(tuple_list)
    return result_list


def collectTechNumber(order):
    print('collecting tech number...')
    fields = ['人工智能', '智能制造', '大数据', '云计算', '工业互联网', '网络安全', '集成电路', '物联网']
    keyword_count = readCSVFiles()
    this_field_number_collection = []
    for top in range(8):
        tech_num = countTechNumber(fields[order], keyword_count[order][top][0])
        this_field_number_collection.append(tech_num)

    return this_field_number_collection


def collectPeriodResult(this_field_number_collection):
    print('collecting period result...')
    this_field_period_collection = []
    for top in range(8):
        tech_period = getAllPeriod(this_field_number_collection[top])
        this_field_period_collection.append(tech_period)

    return this_field_period_collection


def generateYearSeries(start_year, year_num):
    print('generating year series...')
    year_list = []
    for i in range(year_num):
        year_list.append(i + start_year)

    return year_list


def generateTechSeries(order):
    print('generating tech series...')
    keyword_count = readCSVFiles()
    tech_list = []
    for top in range(8):
        tech = keyword_count[order][top][0]
        tech_list.append(tech)

    return tech_list


def generateResultByField(order):
    result_list = []

    year_list = generateYearSeries(1990, 29)
    tech_list = generateTechSeries(order)
    tech_num_list = collectTechNumber(order)
    period_list = collectPeriodResult(tech_num_list)

    result_list.append(year_list)
    result_list.append(tech_list)
    result_list.append(tech_num_list)
    result_list.append(period_list)

    print(result_list)
    return result_list


def writeResultList():
    fields = ['人工智能', '智能制造', '大数据', '云计算', '工业互联网', '网络安全', '集成电路', '物联网']
    for i in range(8):
        result_list = generateResultByField(i)
        result_str = str(result_list)
        result_str = result_str.replace('\'', '\"')
        result_str = result_str.replace(', ', ',')
        filename = '_tempfiles/' + str(i) + fields[i] + '_dbcontent.txt'
        writer = open(filename, 'w')
        writer.write(result_str)
        writer.close()


if __name__ == '__main__':
    generateCSVFiles()
    writeResultList()
