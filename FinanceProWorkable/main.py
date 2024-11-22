# version 0.5.0

import sys
import os
import shutil

# Словарь для функции man по командам
man_dict = {"man": "Чтобы подробнее узнать о команде, напишите : man name_of_function",

"help": """Выводит инструкцию по приложению
Использование: help""",

"start": """Начало работы с файлом
Использование: start group year month""",

"end": """Конец работы с файлом
Работает, если было использована команда start
Использование: end""",

"add": """Добавить новый элемент в файл
Работает, если до этого была использована команда start
Использование: add sum reason comment""",

"close": """Закрывает программу
Использование: close""",

"show": """Отображает элементы файла, если не указано число, отображает последний. Если написать all, покажет все.
Использование: show num""",

"rmlast": """Удаляет последний жлемент в файле.
Использование: rmlast""",

"count": """Считает общее изменение денег в файле.
Использование: count""",

"stats": """Считает все доходы и расходы по категориям.
Использование: stats category  Если category не указан, то выведет все""",

"rmdir": """Удаляет папку вместе с содержимым.
Использование: rmdir path""",

"rmf": """Удаляет файл.
Использование: rmf path""",

"sts": """Показывает текущий статус работы.
Использование: sts""",

"list": """Выводит содержимое директории.
Использование: list path""",

"clear": """Очищает консоль, отоброжает приложение, в котором вы работаете.
Использование: clear""",

"version": """Отображает версию приложения.
Использование: version""",
 
}

def hlp(): # Выводит список всех команд
    print("Поддерживаемые команды:\n", '\n'.join(sorted([
    "help        -- вывод инструкции",
    "start       -- начало работы",
    "add        -- добавить элемент",
    "end         -- конец работы",
    "man         -- мануал по команде",
    "show        -- отображает последние записи в файлах",
    "rmlast      -- удаляет последние элементы файла",
    "count       -- считает сумму всех расходов и доходов в файле",
    "stats       -- отображает расходы и доходы по группам",
    "rmdir       -- удаляет папку",
    "rmf         -- удаляет файл",
    "sts         -- отображает статус работы",
    "close       -- закончить работу программы",
    "list        -- отображает файлы и директории",
    "clear       -- очищает консоль",
    "version     -- отображает версию приложения"])).strip(), '\n')
    
    
def man(name = "man"): # Выводит гайд по команде
    if name in man_dict:
        print(man_dict[name], '\n')
    else:
        print("Такой команды не существует. Воспользуйтесь командой instruction, чтобы увидеть список команд")
        

def version():
    print("FinancePro version 0.5.0")


def close(): # Выход из программы
    ans = input("Вы уверены, что хотите выйти? [Y/N]\n").upper()
    if ans == "Y":
        print("Спасибо за пользование нашим приложением! Ждем вас снова!")
        sys.exit()
    else:
        print("Выход отменен")
        
        
def ls(line):
    if len(line.split()) < 2:
        for i in sorted(os.listdir("files")):
            print(i)
    elif len(line.split()) > 2:
        print("Syntax Error. Use man list")
    else:
        if line.split()[1].startswith(".."):
            print("У вас нет прав доступа!")
            return 0
        try:
            for i in sorted(os.listdir(f'files/{line.split()[1]}')):
                print(i)
        except FileNotFoundError:
            print("Такой папки не существует")
        except WindowsError:
            print("Ошибка!")
        
        
def add(inp, work_file): # Добавить строку в файл
    add_line = inp.split()
                
    if len(add_line) < 3: # Проверка на правильный синтаксис
        print("Syntax Error. Use man add\n")
                    
    else:
        num = add_line[1]
                
        for index in range(len(num)): # Проверяем введена ли сумма
                        
            if index == 0 and num[index] not in "-0123456789":
                        print("Syntax Error. Use man add\n")
                        break
                        
            elif index > 0 and num[index] not in "0123456789":
                print("Syntax Error. Use man add\n")
                break
                        
        else:
            add_line[2].upper()
            work_file.write(" ".join(add_line[1:])) # Записываем в файл
            work_file.write('\n')
            
            
def show(inp, work_file): # Отобразить содержимое файла
    show = inp.split()
                
    if len(show) > 2: # Проверка на синтаксис
        print("Syntax Error. Use man show")
                    
    elif len(show) == 2: # Если есть второй элемент
                    
        if show[1] == "all": # Если all
            work_file.seek(0)
            file_show = work_file.readlines()
                        
            if len(file_show) > 0: # Проверка на длину
                for i in file_show:
                    print(i, end='')
                                
        else: # Если второй элемент число или другое слово
            for char in show[1]: # Проверка на число
                if char not in "0123456789": 
                    break
                            
            else: # Выводим содержимое
                work_file.seek(0)
                file_show = work_file.readlines()
                            
                if len(file_show) > 0: # Проверка на длину
                                
                    if len(file_show) <= int(show[1]): # Если длина меньше или равна требуемой
                        for i in file_show:
                            print(i, end='')
                                
                    else: # Если длина больше
                        for i in file_show[-int(show[1]):]:
                            print(i, end="")
                
                return 0
                            
            work_file.seek(0)
            file_show = work_file.readlines()
            counter = 0
            for line in file_show:
                if line.split()[1].lower() == inp.split()[1].lower():
                    print(line, end='')
                    counter += 1
            else:
                if counter == 0:
                    print(f"Нет информации по запросу '{inp.split()[1]}'")
                                        
    else: # Если только одно слово
        work_file.seek(0)
        file_show = work_file.readlines()
        if len(file_show) > 0:
            print(file_show[-1], end='')
    
                               
        
def count(work_file): # Считает общую сумму в файле
    work_file.seek(0)
    file_show = work_file.readlines()
    main_sum = 0
    plus_sum = 0
    minus_sum = 0
    for line in file_show:
        line = line.split()
        num = int(line[0])
        main_sum += num
        minus_sum += num if num <= 0 else 0
        plus_sum += num if num > 0 else 0
    print(f"Общий доход: {plus_sum}")
    print(f"Общий расход: {minus_sum}")
    print(f"Итоговая сумма: {main_sum}\n")
   
    
def stats(inp, work_file): # Ститает сумму по одноименным групам
    if len(inp.split()) > 2: # Проверка на синтаксис
        print("Syntax Error. Use man stats")
        return 0
    
    elif len(inp.split()) == 1: # Если не введен желаемый класс
        a = "all"
        
    else:
        a = inp.split()[1] # Сохраняем желаемый класс
    
    work_file.seek(0)    
    file_show = work_file.readlines()
    sums = dict() # Словарь значений
    
    for line in file_show: # Считаем значения для каждого класса
        line = line.split()
        sums[line[1]] = sums.get(line[1], 0) + int(line[0])
        
    if a == "all": # Отображаеи все
        for key in sums:
            print(f"{key}: {sums[key]}")
        print('\n')
            
    else: # Отображаем желаемый
        if a in sums:
            print(f"{a}: {sums[a]}")
        else:
            print("Информация не найдена\n")
    
        
def start(group, year, month):
    cls_flag = False
    try:
        os.makedirs(f"files/{group}/{year}")
    except FileExistsError:
        pass
    
    work_file = open(f"files/{group}/{year}/{month.upper()}{year}.txt", "a+", encoding="utf-8")
        
    while True:
        print(">>>", end="")
        inp = " ".join(input().split())
            
        if inp == "end": # end
            print("Файл успешно сохранен\n")
            break
            
        elif inp == "close": # close
            cls_flag = True
            print("Файл успешно сохранен")
            break
            
        elif inp.startswith("man ") or inp == 'man': # man
            man(inp.split()[1]) if len(inp.split()) > 1 else man()
                
        elif inp.startswith("start"): # start
            print("Снаяала закройте текущий файл, чтобы открыть другой!\n")
                
        elif inp == "help": # help
            hlp()
                
        elif inp.startswith("rmf") or inp.startswith("rmdir"): # rmdir and rmf
            print("Снаяала закройте файл!\n")
            
        elif inp == 'version':
            version()
        
        elif inp == "sts": #sts
            print(f"Вы работаете с файлом {group}/{year}/{month.upper()}{year}.txt")
                
        elif inp.startswith("add ") or inp == 'add': # add sum reason comment
            add(inp, work_file)
            
        elif inp.startswith("show ") or inp == 'show': # show
            show(inp, work_file=work_file)
                            
        elif inp == "rmlast": # rmlast
            work_file.seek(0)
            file_show = work_file.readlines() # Считываем все строки
                
            if len(file_show) > 0: # Если строк больше 0, улаляем последнюю, иначе ничего не делаем
                file_show.pop()
                work_file.close()
                    
                work_file = open(f"files/{group}/{year}/{month.upper()}{year}.txt", "w", encoding="utf-8") # Перезаписываем файл целиком
                if len(file_show) > 0:
                    for i in range(len(file_show)):
                        work_file.write(file_show[i])
            work_file.close()
            work_file = open(f"files/{group}/{year}/{month.upper()}{year}.txt", "a+", encoding="utf-8")
        
        elif inp == "count": # count
            count(work_file=work_file)
            
        elif inp.startswith("stats ") or inp == 'stats': # stats
            stats(inp, work_file=work_file)
            
        elif inp == "clear":
            clear()
            print(f"На данный момент открыт файл {group}/{year}/{month.upper()}{year}.txt")
            
        elif inp.startswith('list ') or inp == 'list': # list
            ls(inp)
            
        elif inp == "":
            pass    
            
        else:
            print("Function is not found")
                            
    work_file.close()                            
    if cls_flag:
        close()
            

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Вы работаете в "FinancePro"')
    

def main():
    print('Добро пожаловать в "FinancePro"')
    print("Воспользуйтесь командой help, чтобы увидеть список команд")
    try:
        os.makedirs('files')
    except FileExistsError:
        pass
    while True:
        print(">>>", end="")
        line = " ".join(input().split())
        
        if line == "close": # close
            close()
            
        elif line.startswith("man ") or line == 'man': # man
            man(line.split()[1]) if len(line.split()) > 1 else man()
            
        elif line == "help": # help
            hlp()
            
        elif line == 'version':
            version()
            
        elif line == "sts": # sts
            print("Ни один файл пока не открыт")
            
        elif (line == "end" or line == "add" or line == "show" or line == "rmlast" or line == "count" or line == "stats"
              or line.startswith('add ') or line.startswith('show ') or line.startswith('stats ')):
            print("Вы не работаете ни с одним файлом!") # end, add, show, rmlast, count, stats
            
        elif line.startswith("rmdir ") or line == "rmdir": # rmdir
            if len(line.split()) != 2:
                print("Syntax Error. Use man rmdir")
            else:
                if line.split()[1].startswith('..'):
                        print("У вас нет прав доступа!")
                else:
                    print("Вы уверены, что хотите удалить папку? Все содержимое будет потеряно [Y/N]")
                    if input().lower() == 'y':
                        shutil.rmtree(f"files/{line.split()[1]}", ignore_errors=True)  
            
        elif line.startswith("rmf ") or line == 'rmf': # rmf
            if len(line.split()) != 2:
                print("Syntax Error. Use man rmf")
            else:
                if line.split()[1].startswith(".."):
                    print("У вас нет прав доступа!")
                else:
                    try:
                        os.remove(f"files/{line.split()[1]}")
                    except FileNotFoundError:
                        print("File not found!")
                
        elif line.startswith("start ") or line == 'start': # start
            words = line.split()
            if len(words) != 4:
                print("Syntax Error. Use man start")
            else:
                start(words[1], words[2], words[3])
                
        
        elif line.startswith('list ') or line == "list":
            ls(line)
            
        elif line == "clear":
            clear()
            print("Вы не работаете ни с одним файлом в данный момент.")
            
        elif line == "":
            pass
                
        else:
            print("Function is not found")
    
    
if __name__ == "__main__":
    main()