from datetime import datetime


class Lesson:
    __current_string = ''

    def __init__(self, string_to_parse):
        self.discipline = ''
        self.room = ''
        self.building = '0'
        self.groups = [Lesson.get_course(string_to_parse[:6].strip())]
        self.__current_string = string_to_parse[6:].strip()
        self.is_dop = False
        self.subgroup = 0

        self.__get_one_more_group_if_have()
        self.__split_cabinet_room_from_str() \
            .__get_attr_from_discipline(). \
            __split_room()

    def __get_one_more_group_if_have(self):
        """
        Если у одной дисциплины две группы
        :return: Lesson
        """

        if self.__current_string[0].isdigit():
            group_to_add = self.__current_string[:6].strip()
            self.groups.append(Lesson.get_course(group_to_add))
            self.__current_string = self.__current_string[6:].strip()
        return self

    def __split_cabinet_room_from_str(self):
        """
        Что бы корректно получить строки ищем начало кабинета в строке (используя пробел)
        :return:
        """
        place_space_from_end = self.__current_string.rfind(" ")
        if place_space_from_end != -1:
            self.discipline = self.__current_string[:place_space_from_end + 1].strip()
            self.room = self.__current_string[place_space_from_end + 1:].strip()
        return self

    def __split_room(self):
        """
        Разделение кабинета на номер и корпус
        :return:
        """
        if "/" in self.room:
            self.building, self.room = self.room.split("/")
        self.room = self.room.replace("'", "")
        return self

    def __get_attr_from_discipline(self):
        """
        Получаем ифнормацию о дисуиплине: ДОП?, Подгруппа?
        :return:
        """
        discipline = self.discipline.replace('[СДО]', '').replace("[]", '')

        if Lesson.has_numbers(discipline):
            if discipline[1] == 'О':
                self.subgroup = 0
            else:
                self.subgroup = discipline[1]

            discipline = discipline[4:]
        if 'ДОП' in discipline:
            discipline = discipline.replace("ДОП", '').strip()
            self.is_dop = True
        self.discipline = discipline
        return self

    @staticmethod
    def has_numbers(inputString):
        return any(char.isdigit() for char in inputString)

    @staticmethod
    def get_course(group_name):
        group_data = {"group": group_name, 'year': "2222", "course": "0"}
        today = datetime.now()
        year_end = today.year
        year_start = year_end - 10
        for i in range(year_start, year_end, 1):
            year = str(i)
            if (year[-1] == group_name[1]):
                course = year_end - i + 1
                group_data = {"group": group_name, "year": year, "course": course}
        return group_data
