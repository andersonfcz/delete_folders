import sys, getopt


def parseArgs(argv):
    arg_days = ""
    arg_path = ""
    arg_help = "Usage: {0} -d <days> -p <path>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hd:p:", ["help", "days=", "path="])
    except getopt.GetoptError:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit()
        elif opt in ("-d", "--days"):
            arg_days = arg
        elif opt in ("-p", "--path"):
            arg_path = arg
    
    if not arg_days or not arg_path:
        print(arg_help)
        sys.exit(2)

    return arg_days, arg_path

if __name__ == "__main__":
    print(parseArgs(sys.argv))
