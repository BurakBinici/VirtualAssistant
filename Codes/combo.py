import openpyxl


data = openpyxl.load_workbook("./ExcelFiles/known_words.xlsx")

suffix_sheet = data['suffixes']
bad_state_sheet = data['bad_state']
designer_sheet = data['designer']
good_state_sheet = data['good_state']
goodbye_sheet = data['goodbye']
greet_sheet = data['greet']
howareyou_sheet = data['howareyou']
negative_sheet = data['negative']
positive_sheet = data['positive']
thank_sheet = data['thank']
weather_sheet = data['weather']


def get_column(sheet, char='A'):
    array = []
    for row in sheet.iter_rows(min_row=1, values_only=True):
        col_data = row[sheet[f"{char}1"].column - 1]
        array.append(col_data)
    return array


def create_combo(words, suffixes):
    array = []
    for word in words:
        array.append(word)
        for suffix in suffixes:
            new_word = word + suffix
            array.append(new_word)
    return array


def write_file(array, file_name, path='./Texts/Excel/', ext='.txt'):
    try:
        if file_name[-4:] != ext:
            file_name = file_name + ext
        with open(f"{path}/{file_name}", "w", encoding="utf-8") as file:
            for element in array:
                file.write(element+"\n")
        print(f"{file_name} dosyası başarıyla yazıldı.")
    except Exception as e:
        print(f"{file_name} dosyasına yazarken bir hata ile karşılaşıldı! {e}")


suffixes = get_column(suffix_sheet)
bad_states = get_column(bad_state_sheet)
designer = get_column(designer_sheet)
good_states = get_column(good_state_sheet)
goodbyes = get_column(goodbye_sheet)
greets = get_column(greet_sheet)
howareyous = get_column(howareyou_sheet)
negatives = get_column(negative_sheet)
positives = get_column(positive_sheet)
thanks = get_column(thank_sheet)
weathers = get_column(weather_sheet)

bad_state_combos = create_combo(bad_states, suffixes)
designer_combos = create_combo(designer, suffixes)
good_state_combos = create_combo(good_states, suffixes)
goodbye_combos = create_combo(goodbyes, suffixes)
greet_combos = create_combo(greets, suffixes)
howareyou_combos = create_combo(howareyous, suffixes)
negative_combos = create_combo(negatives, suffixes)
positive_combos = create_combo(positives, suffixes)
thank_combos = create_combo(thanks, suffixes)
weather_combos = create_combo(weathers, suffixes)

write_file(bad_state_combos, "bad_state")
write_file(designer_combos, "designer")
write_file(good_state_combos, "good_state")
write_file(goodbye_combos, "goodbye")
write_file(greet_combos, "greet")
write_file(howareyou_combos, "howareyou")
write_file(negative_combos, "negative")
write_file(positive_combos, "positive")
write_file(thank_combos, "thank")
write_file(weather_combos, "weather")

