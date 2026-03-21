import re

from src.read_files import read_excel


def physical_transactions():
    excel_data = read_excel('../data/operations.xlsx')

    phys_faces = []
    phys_transactions = []

    not_phys_transactions = []
    not_phys_description = ['Перевод', 'Закрытие', 'Пополнение',
                            'На р/с', 'Линзомат', 'Вывод средств', 'Аренда', 'АО']
    not_phys_patterns = []

    for desc in not_phys_description:
        not_phys_patterns.append(rf'{desc}\s\w')

    for transaction in excel_data:
        for pattern in not_phys_patterns:
            if len(re.findall(pattern, transaction['Описание'])):
                not_phys_transactions.append(transaction)


    for transaction in excel_data:
        if transaction['Категория'] == 'Переводы' and transaction not in not_phys_transactions:
            description = transaction['Описание']
            name = ''
            surname = ''
            if len(description.split(' ')) > 1:
                name = description.split(' ')[0]
                surname = description.split(' ')[1]

            if len(surname) > 2 and description.find(' ') > 0:
                description = name + ' ' + surname[0] + '.'
            if description not in ['Аренда', 'Инвесткопилка']:
                phys_faces.append(description)

    for transaction in excel_data:
        if transaction['Описание'] in phys_faces:
            phys_transactions.append(transaction)

    return phys_transactions
