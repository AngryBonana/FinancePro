import sys
import os, stat
import shutil


man_dict = {"man": "To now more about the command, write: man name_of_function",

"help": """Show the instruction and list of commands.
Using: help""",

"start": """Open the file.
Using: start group year month""",

"end": """Close the opened file.
Works only if you open the file
Using: end""",

"add": """Add new element in file.
Works only if you open the file
Using: add sum category comment""",

"close": """Close programm.
Using: close""",

"show": """Show last element. If an argument is num show last num elements.
If an argument is word show all elements with this category.
If an argument is 'all' show all elements.
Using: 'show num', 'show category', 'show all', 'show'""",

"rmlast": """Delete last element in file.
Using: rmlast""",

"count": """Count income/expenses in file.
Using: count""",

"stats": """Count income/expenses by categories.
Using: 'stats category'  If category is empty show all categories""",

"rmdir": """Remove directory.
Using: rmdir path""",

"rmf": """remove file.
Using: rmf path""",

"sts": """Show oppened file.
Using: sts""",

"list": """Show list of dirs and files.
Using: list path""",

"clear": """Clear console.
Using: clear""",

"version": """Show version of programm.
Using: version""",
 
}


def make_clear(line): # Форматирует полученную команду в кортеж
    line = line.lower().split()
    return tuple(line)


def version(): # Show version of a programm
    print("FinancePro version 1.0")


def hlp(): # Выводит список всех команд
    print("Supported Commands:\n", '\n'.join(sorted([
    "help        -- an instruction output",
    "start       -- open the file for work",
    "add         -- add an element in file",
    "end         -- close the file",
    "man         -- a manual for command",
    "show        -- show last strings in file",
    "rmlast      -- remove the last string in file",
    "count       -- calculates the sum of all expenses and income in the file",
    "stats       -- displays expenses and income by groups",
    "rmdir       -- remove a directory",
    "rmf         -- remove a file",
    "sts         -- show status of work",
    "close       -- close the programm",
    "list        -- show directories and files",
    "clear       -- clear console",
    "version     -- show a version of the programm"])).strip(), sep="")
    
    
def close(): # Выход из программы
    ans = input("Are you sure that you want to exit? [Y/N]\n").upper()
    if ans == "Y":
        print("Thanks for using FinancePro!")
        sys.exit()
    else:
        print("Stop exiting.")


def man(name = "man"): # Выводит гайд по команде
    if name in man_dict:
        print(man_dict[name])
    else:
        print("Command doesn't exist! Use 'help' to see commands.")
        
        
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('You work with "FinancePro".')
    print("Use 'help' to see commands.")
    
    
def ls(path):
    if ".." in path:
        print("You don't have access rights!")
        return
    try:
        for i in sorted(os.listdir(path)):
            print(i)
    except FileNotFoundError:
        print("The directory doesn't exist!")
    except WindowsError:
        print("Error!")
        
        
def rmf(path):
    if ".." in path:
        print("You don't have access rights!")
        return
    check = input("Are you sure? Data will be disappear [Y/N]\n").upper()
    if check != "Y":
        print("Stop deleting!")
        return
    try:
        os.remove(path)
        print("The file was deleted!")
    except FileNotFoundError:
        print("The file is not founded!")


def remove_readonly(func, path, exc_info):
        "Clear the readonly bit and reattempt the removal"
        # ERROR_ACCESS_DENIED = 5
        if func not in (os.unlink, os.rmdir) or exc_info[1].winerror != 5:
            raise exc_info[1]
        os.chmod(path, stat.S_IWRITE)
        func(path)


def rmdir(path):
    if ".." in path:
        print("You don't have access rights!")
        return
    check = input("Are you sure? Data will be disappear [Y/N]\n").upper()
    if check == "Y":
        shutil.rmtree(path, onerror=remove_readonly)
        print("Directory was deleted!") 
    else:    
        print("Stop deleting!")    


def show(filename, num = 1):
    filename.seek(0)
    lines = filename.readlines()
    length = len(lines)
    if length == 0:
        print("File is empty")
        return
    if num == "all" or int(num) >= length:
        for i in lines:
            print(i, end="")
    else:
        for i in lines[- int(num):]:
            print(i, end="")
            
            
def show_pattern(filename, pattern):
    filename.seek(0)
    lines = filename.readlines()
    if len(lines) == 0:
        print("File is empty")
        return
    counter = 0
    for i in lines:
        if pattern == i.split()[1]:
            print(i, end="")
            counter += 1
    else:
        if counter == 0:
            print("No such lines")
            

def rmlast(file, file_name):
    file.seek(0)
    lines = file.readlines()
    length = len(lines)
    if length == 0:
        print("File is empty")
    else:
        file.close()
        with open(file_name, "w", encoding="utf-8") as file:
            length -= 1
            if length != 0:
                for i in lines[:-1]:
                    file.write(i)
        
        file = open(file_name, "a+", encoding="utf-8")
        return file


def count(file):
    file.seek(0)
    lines = file.readlines()
    length = len(lines)
    if length == 0:
        print("File is empty")
        return
    summary = 0
    for i in lines:
        num = float(i.split()[0])
        summary += num
    print(f"Income/Expenses: {summary}")


def stats(file, pattern = None):
    file.seek(0)
    lines = file.readlines()
    if len(lines) == 0:
        print("File is empty")
        return
    
    if pattern is None:
        stats_dict = dict()
        for i in lines:
            key = i.split()[1]
            num = float(i.split()[0])
            stats_dict[key] = stats_dict.get(key, 0) + num
        for key in sorted(stats_dict):
            print(f"{key}: {stats_dict[key]}")
            
    else:
        pattern = pattern.lower()
        summary = 0
        for i in lines:
            if i.split()[1] == pattern:
                num = float(i.split()[0])
                summary += num
        print(f"{pattern}: {summary}")


def start(path):
    file_name = path
    dir_name = os.path.dirname(file_name)
    
    os.makedirs(dir_name, exist_ok=True)
    
    file =  open(file_name, "a+", encoding="utf-8")
    
    while True:
        line = make_clear(str(input(">>>")))
        
        length = len(line)
        if length == 0:
            continue
    
        first_word = line[0]
            
        match first_word:
                
            case "help":
                hlp()
                    
            case "man":
                if length == 1:
                    man()
                elif length == 2:
                    man(line[1])
                else:
                    print("Bad Syntax! Use pattern:'man name_command'!")

            case "sts":
                print(f"Open file '{file_name.lstrip('data/')}'")
                    
            case "clear":
                clear()
                print(f"Open file '{file_name.lstrip('data/')}'")
                    
            case "list":
                if length == 1:
                    ls("data")
                elif length == 2:
                    ls(f"data/{line[1]}")
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                    
            case "version":
                if length == 1:
                    version()
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                        
            case "rmf" | "rmdir":
                print("Close file to do this!")
                    
            case "start":
                print("Close openned file before!")
                    
            case "end":
                print("File was succesfully saved and closed!")
                file.close()
                break
                
            case "close":
                file.close()
                print("File was succesfully saved and closed!")
                close()
                break
                
            case "add":
                if length >= 2 and line[0]:
                    line_list = list(line)
                    line_list[2] = line_list[2].lower()
                    try:
                        float(line_list[1])
                    except ValueError:
                        print("Wrong sum!")
                        continue
                    file.write(" ".join(line_list[1:]))
                    file.write("\n")
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                        
            case "show":
                if length == 1:
                    show(file)
                elif length == 2 and (line[1].isdigit() or line[1] == "all"):
                    show(file, line[1])
                elif length == 2:
                    show_pattern(file, line[1])
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                        
            case "rmlast":
                if length == 1:
                    file = rmlast(file, file_name)
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                        
            case "count":
                count(file)
                
            case "stats":
                if length == 1:
                    stats(file)
                elif length == 2:
                    stats(file, pattern=line[1])
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                    
            case _:
                print("Commant doesn't exist!")
                    
        
    file.close()    
                            

def main():
    
    try:
        os.makedirs('data')
    except FileExistsError:
        pass
    
    while True:
        line = make_clear(str(input(">>>")))
        
        length = len(line)
        if length == 0:
            continue
        
        first_word = line[0]
        
        match first_word:
            
            case "help":
                hlp() if length == 1 else print("Bad Syntax! Use 'man' to know, how to use command!")
                
            case "man":
                if length == 1:
                    man()
                elif length == 2:
                    man(line[1])
                else:
                    print("Bad Syntax! Use pattern:'man name_command'!")
                    
            case "end" | "add" | "show" | "rmlast" | "count" | "stats":
                print("You don't work with any file now. Use 'start' to start work")
                
            case "sts":
                print("No open files right now.")
                
            case "close":
                close()
                
            case "clear":
                clear()
                print("No open files right now.")
                
            case "list":
                if length == 1:
                    ls("data")
                elif length == 2:
                    ls(f"data/{line[1]}")
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                    
            case "version":
                if length == 1:
                    version()
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                    
            case "rmf":
                if length == 2:
                    rmf(f"data/{line[1]}")
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
            
            case "rmdir":
                if length == 2:
                    rmdir(f"data/{line[1]}")
                else:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                    
            case "start":
                if length != 4:
                    print("Bad Syntax! Use 'man' to know, how to use command!")
                    continue
                group = line[1]
                
                year = line[2]
                if not year.isdigit() or len(year) != 4:
                    print("Wrong year error!")
                    continue
                
                month = line[3].upper()
                if month not in ("JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"):
                    print("Bad month error!")
                    continue
                
                path = f"data/{group}/{year}/{group}_{month}_{year}.txt"
                start(path)
                
                    
            case _:
                print("Commant doesn't exist!")
                        
                
if __name__ == "__main__":
    print('Welcome to "FinancePro".')
    print("Use 'help' to see commands.")
    main()