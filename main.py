"""The main file containing business logic"""
import sys
import re
import csv
import xml.etree.ElementTree as ET


def price_in_gp(raw_price: str) -> float:
    """Return the price given in any unit as the price in GP."""
    price_list = [int(s) for s in raw_price.split() if s.isdigit()]
    final_price = 0.0
    if len(price_list):
        price = price_list[0]
        unit = ''.join(re.findall('[a-zA-Z]+', raw_price))

        if unit == "gp":
            final_price = float(price)
        elif unit == "sp":
            final_price = float(price / 10)
        elif unit == "cp":
            final_price = float(price / 100)
        else:
            final_price = float(price)

    return final_price


def text_filter(data: str) -> str:
    """Replace newlines, tabs and strange apostrophes."""
    result = ''.join(data)
    result = result.strip()
    result = result.replace('\r\n', '')
    result = result.replace('\t', ' ')
    result = result.replace(chr(0x92), "'")
    return result


def fix_line_endings(filename: str) -> None:
    """Make sure no extranious newline characters exists"""
    with open(filename, 'r', encoding='iso-8859-1') as file:
        contents = file.read()
        contents = re.sub('\r\r\n', '\r\n', contents)
        print([i for i in contents.split('\n') if i])
        contents = '\n'.join([i for i in contents.split('\n') if i])

    with open(filename, 'w', encoding='iso-8859-1') as file:
        file.write(contents)


def read_xml(filename: str) -> list:
    """Parse the XML data into a list."""
    tree = ET.parse(filename)
    root = tree.getroot()
    items = root.findall('./item/category/*')
    rows = []

    for item in items:
        try:
            title = item.find('name').text
        except AttributeError:
            title = ''

        try:
            description = text_filter(
                ''.join(item.find('description').itertext())
                )
        except AttributeError:
            description = ''

        try:
            weight = item.find('weight').text
        except AttributeError:
            weight = ''

        try:
            price = price_in_gp(item.find('cost').text)
        except AttributeError:
            price = 0.0

        rows.append([title, description, weight, '1', price, ''])

    return rows


def write_csv(filename: str, headers: list, data: list) -> None:
    """Write the data as a CSV file to the file filename"""
    with open(filename, 'w', encoding='iso-8859-1') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    fix_line_endings(filename)


def convert_xml_to_csv(file_in: str, file_out: str) -> int:
    """Convert the data from XML to CSV"""
    headers = ['title', 'description', 'weight', 'qty', 'price', 'rarity']
    rows = read_xml(file_in)
    write_csv(file_out, headers, rows)

    return len(rows)


def main(*args) -> None:
    """Main entry point of the application"""
    if len(args) < 2:
        raise AttributeError(
            'The function main() requires at least two arguments.'
            )

    if args[0] == '' or args[1] == '':
        raise AttributeError('No filenames given.')

    num_items = convert_xml_to_csv(args[0], args[1])
    print(f'Converted {num_items} items.')


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError:
        print("Usage: $ python3 main.py file_a.xml file_b.csv")
