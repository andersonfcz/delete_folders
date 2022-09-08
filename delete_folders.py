from datetime import date
from shutil import rmtree
from getopt import getopt, GetoptError
from stat import S_IWRITE
from sys import exit, argv
from os import chmod, scandir

def parse_args(argv):
    arg_days = ""
    arg_path = ""
    arg_help = "Usage: {0} -d <days> -p <path>".format(argv[0])
    
    try:
        opts, _ = getopt(argv[1:], "hd:p:", ["help", "days=", "path="])
    except GetoptError:
        print(arg_help)
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            exit()
        elif opt in ("-d", "--days"):
            arg_days = arg
        elif opt in ("-p", "--path"):
            arg_path = arg

    if not arg_days or not arg_path:
        print(arg_help)
        exit(2)

    return arg_days, arg_path

# Return true if folder prefix is a valid date and is older than defined number of days
def should_delete_folder(folder_prefix, days):
    try:
        folder_date = date.fromisoformat(folder_prefix)
        diff = date.today() - folder_date
        return diff.days > int(days)
    except:
        return False

#Function to handle rmtree fail to delete folders if contain readonly files
def delete_readonly_folders(func, path, _):
    chmod(path, S_IWRITE)
    func(path)


def delete_folders(days, path):
    try:
        #Walks through every object in given path.
        for entry in scandir(path):
            #Test if object's name begins with a valid date and is older than defined number of days
            if entry.is_dir() and should_delete_folder(entry.name[:10], days):
                rmtree(entry.path, ignore_errors=False, onerror=delete_readonly_folders)
                print("Removed ", entry.path)
    except OSError as err:
        print(err)
        exit(2)

if __name__ == "__main__":
    days, path = parse_args(argv)
    delete_folders(days,path)
