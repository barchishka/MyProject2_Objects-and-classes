# Студенты
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def __str__(self):
        output = f'Имя: {self.name}' \
                 f'\nФамилия: {self.surname}' \
                 f'\nСредняя оценка за домашние задания: {average_grade(self.grades)}' \
                 f'\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}' \
                 f'\nЗавершенные курсы: {", ".join(self.finished_courses)}'
        return output

    # Оценки лекторам
    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) \
                and course in lecturer.courses_attached \
                and course in self.courses_in_progress \
                and 0 < grade <= 10:

            lecturer.grades.append(grade)
        else:
            return 'Ошибка'

    def __lt__(self, other_student):
        if isinstance(other_student, Student):
            return average_grade(self.grades) < average_grade(other_student.grades)
        else:
            return None


# Преподаватели
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


# Лекторы
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = []
        self.courses_attached = []

    def __str__(self):
        output = f'Имя: {self.name}' \
                 f'\nФамилия: {self.surname}' \
                 f'\nСредняя оценка за лекции: {average_grade(self.grades)}'
        return output

    def __lt__(self, other_lecturer):
        if isinstance(other_lecturer, Lecturer):
            return average_grade(self.grades) < average_grade(other_lecturer.grades)
        else:
            return None


# Эксперты (проверяющие)
class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

    def __str__(self):
        output = f'Имя: {self.name}' \
                 f'\nФамилия: {self.surname}'
        return output

    # Оценки студенту
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) \
                and course in self.courses_attached \
                and course in student.courses_in_progress:

            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


# Расчет среднего значения оценок:
def average_grade(all_grades):
    if type(all_grades) is dict:
        amount_grades = []
        for grades in all_grades.values():
            for grade in grades:
                amount_grades.append(grade)
        return average_grade(amount_grades)
    elif type(all_grades) is list and all_grades[0] is not None:
        average = round(sum(all_grades) / len(all_grades), 2)
        return average
    else:
        return "Ошибка! Оценки хранятся не в словаре и не в списке, или список состоит из вложенных списков"


# Расчет среднего значения оценок:
def average_course_grade(all_students, current_course):
    all_course_grades = []
    for current_student in all_students:
        if current_course in current_student.grades.keys():
            for every_grade in current_student.grades.get(current_course):
                all_course_grades.append(every_grade)
        else:
            print(f'Курс {current_course} отсутствует у студента {current_student.name} {current_student.surname}')
    return average_grade(all_course_grades)


# Расчет среднего значения оценок:
def average_lecturers_grade(all_lecturers):
    all_lecturers_grades = []
    for current_lecturer in all_lecturers:
        for every_grade in current_lecturer.grades:
            all_lecturers_grades.append(every_grade)
    return average_grade(all_lecturers_grades)


student_1 = Student('Roy', 'Eman', '21')
student_1.courses_in_progress += ['Python', 'Git']
student_1.finished_courses += ['Введение в программирование']
student_1.grades['Git'] = [6, 5, 10, 8]
student_1.grades['Python'] = [4, 6, 8, 10, 7]

student_2 = Student('Mark', 'Aurelius', '25')
student_2.courses_in_progress += ['Python', 'Git']
student_2.finished_courses += ['Введение в программирование']
student_2.grades['Git'] = [4, 5, 10, 7]
student_2.grades['Python'] = [6, 3, 9, 2, 10]

student_list = [student_1, student_2]


lecturer_1 = Lecturer('Pavel', 'Volya')
lecturer_1.courses_attached += ['Python']
lecturer_1.courses_attached += ['Git']

lecturer_2 = Lecturer('Dima', 'Sorokin')
lecturer_2.courses_attached += ['Python']
lecturer_2.courses_attached += ['Git']

lecturer_list = [lecturer_1, lecturer_2]


cool_reviewer = Reviewer('Serge', 'Gorely')
cool_reviewer.courses_attached += ['Python']

cool_reviewer_2 = Reviewer('Edgar', 'Poe')
cool_reviewer_2.courses_attached += ['Git']


print('Результат оценок: ')
# Выставление оценки экспертом студента:
cool_reviewer.rate_hw(student_1, 'Python', 1)
cool_reviewer.rate_hw(student_1, 'Python', 1)
print(f'- Оценки экспертом студента {student_1.grades}')


# Выставление оценки студентом_1 лектору:
student_1.rate_lecturer(lecturer_1, 'Python', 5)
student_1.rate_lecturer(lecturer_1, 'Python', 8)
print(f'- Оценки студентом_1 лектора {lecturer_1.grades}')

# Выставление оценки студентом_2 лектору:
student_2.rate_lecturer(lecturer_1, 'Python', 7)
student_2.rate_lecturer(lecturer_2, 'Python', 7)
print(f'- Оценки студентом_2 лектора {lecturer_1.grades}')


print(lecturer_1)
print()
print(lecturer_2)
print()

print(cool_reviewer)
print()

print(student_1)
print()
print(student_2)
print()

print('Cредний балл студентов по курсу Git: ')
print(average_course_grade(student_list, 'Git'))

print('Cредний балл студентов по курсу Python: ')
print(average_course_grade(student_list, 'Python'))

print('Средний балл лекторов по курсу: ')
print(average_lecturers_grade(lecturer_list))
