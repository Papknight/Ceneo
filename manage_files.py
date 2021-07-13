import pandas as pd
from datetime import datetime


def delete_date(filename: str, date: str) -> None:
    df = pd.read_csv(filename, sep=';')
    df = df.loc[df['Data'] != date]
    df.to_csv(filename, sep=';', index=False)
    return None


def change_status(filename: str) -> None:
    df = pd.read_csv(filename, sep=';')
    for d in df['Data'].unique():
        print(d)
    dates = [datetime.strptime(date, '%d.%m.%Y') for date in df['Data'].unique()]
    dates.sort(reverse=True)
    dates_dict = {}
    for i in range(len(dates)):
        if i == 0:
            status = '0'
        elif i == 1:
            status = '-1'
        else:
            status = ''
        dates_dict[datetime.strftime(dates[i], '%d.%m.%Y')] = status

    for date in dates_dict:
        df.loc[df['Data'] == date, 'Aktualny'] = dates_dict[date]

    df.to_csv(filename, sep=';', index=False)

    return None


if __name__ == '__main__':
    filename = 'Raport Ceneo.csv'
    # delete_date(filename, '14.05.2021')
    # change_status(filename)


    # with open(filename, 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    #
    # new_lines = []
    # for line in lines:
    #     if line[:22] == '0;14.05.2021;81812965;':
    #         print(line)
    #     if line[-3:] == ';\n':
    #         new_lines.append(f'{line[:-3]}\n')
    #     else:
    #         new_lines.append(line)
    #
    # with open('Raport ceneo 2.csv', 'w', encoding='utf-8') as nf:
    #     for nl in new_lines:
    #         nf.write(nl)
