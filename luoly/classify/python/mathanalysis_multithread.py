import sys

# data number for one set
one_set_sample = 12

# data number for phoneme
phoneme_num = 4


# calcAvg, return 12 avg
def calc_avg(datas):
    avgs = [0 for i in range(one_set_sample)]
    for i in range(one_set_sample):
        one_sum = 0
        valid_count = 0
        for j in range(len(datas)):
            if datas[j][i] < 5: # valid data
                continue
            one_sum += datas[j][i]
            valid_count += 1
        if valid_count == 0:
            continue
        avgs[i] = round(one_sum / valid_count, 2)
    return avgs

#calc every set variance, return 60
def every_set_variance(datas, avgs):
    variances = []
    for data in datas:
        one_set_sum = 0
        for i in range(one_set_sample):
            if data[i] < 5: # valid data
                continue
            one_set_sum += pow(data[i] - avgs[i], 2)
        variances.append(round(pow(one_set_sum, 0.5), 2))
    return variances

# calc trainData
def train_data(datas, avgs):
    train_data_values = []
    for data in datas:
        train_data_values.append([ round(data[i] - avgs[i], 2) for i in range(len(avgs))])
    return train_data_values

# compare .wav name
def cmd_func(a, b):
    return cmp(a, b)

# read file datas
def read_file(file_name):
    file = open(file_name)
    test_data = file.readlines()
    line_count = 1
    datas = []
    tmp = []
    merge_tmp = []
    for t_data in test_data:
        t_data = t_data.strip()
        tmp.append(t_data)
        if (line_count % 3 == 0):
            tmp.sort(cmp=cmd_func)
            tmp = str(tmp).strip()
            tmp = tmp.replace('[', '')
            tmp = tmp.replace(']', '')
            tmp = tmp.replace('"', '')
            tmp_new = tmp.split(", ")
            for i in range(len(tmp_new)):
                if i % (phoneme_num + 2) == 0 or i % (phoneme_num + 2) == 1:
                    continue
                merge_tmp.append(abs(float(tmp_new[i])))
            tmp = []
            datas.append(merge_tmp)
            merge_tmp = []
        line_count += 1
    file.close()
    return datas


def main():

    # human test data file
    h_test_file_name = sys.argv[1]
    h_datas = read_file(h_test_file_name)

    # machine test data file
    m_test_file_name = sys.argv[2]
    m_datas = read_file(m_test_file_name)

    #human new data file
    h_new_data_file_name = sys.argv[3]
    h_new_data_file = open(h_new_data_file_name, 'w')

    # machine new data file
    m_new_data_file_name = sys.argv[4]
    m_new_data_file = open(m_new_data_file_name, 'w')

    avg = calc_avg(h_datas)
    print avg
    calc_avg(m_datas)
    h_varainces = every_set_variance(h_datas, avg)
    m_variances = every_set_variance(m_datas, avg)
    #print avg
    #print m_avg
    #print h_varainces
    #print m_variances
    h_train_data = train_data(h_datas, avg)
    m_train_data = train_data(m_datas, avg)

    for h_d in h_train_data:
        h_new_data_file.write(str(h_d))
        h_new_data_file.write('\n')

    for m_d in m_train_data:
        m_new_data_file.write(str(m_d))
        m_new_data_file.write('\n')

    h_new_data_file.close()
    m_new_data_file.close()

if __name__ == '__main__':
    main()