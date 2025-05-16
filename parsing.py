import requests
from bs4 import BeautifulSoup

def parse(letter):
    
    """
    Основная функция для парсинга списка сотрудников ОмГТУ по первой букве фамилии
    :param letter: первая буква фамилии (кириллица)
    """

    alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 
                'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 
                'Щ', 'Э', 'Ю', 'Я']

    # Индекс буквы в алфавите для формирования URL
    letter_index = alphabet.index(letter)
    
    url = f'https://omgtu.ru/ecab/persons/index.php?b={letter_index}'
    
    response = requests.get(url)
    
    # Проверка успешности GET запроса
    if response.status_code != 200:
        print(f"Ошибка при запросе страницы: {response.status_code}")
        return
    
    # Объект BS для парсинга
    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        # Ищем все div-элементы с именами сотрудников
        people = soup.find_all('div', class_='person__name')
    except Exception as e:
        print("Не удалось выполнить парс. Возможно поменялась ссылка либо структура страницы.")

    # Открытие файла для записи результатов
    with open("staff_list.txt", "w", encoding="utf-8") as file:
        for person in people:
            # Ищем тег <a> с именем сотрудника
            name_tag = person.find('a')
            if name_tag:
                full_name = name_tag.text.strip()
                # Запись в файл
                file.write(full_name + '\n')
                print(full_name)

if __name__ == '__main__':
    first_letter = input("Введите букву фамилии для парса: ").upper()
    
    if first_letter not in 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ':
        print("Ошибка: введена некорректная буква. Используйте буквы русского алфавита.")
    else:
        parse(first_letter)
