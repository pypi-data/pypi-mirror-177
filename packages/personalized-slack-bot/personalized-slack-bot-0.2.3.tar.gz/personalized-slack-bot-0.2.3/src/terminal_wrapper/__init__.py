from optparse import OptionParser

# Parser Build
parser = OptionParser()
parser.add_option("-m", "--message", dest="MES", help="Message text")
parser.add_option("-p", "--pid", dest="PID", help="Process ID")
parser.add_option("-d", "--date", dest="DAT", help="Date")
parser.add_option("-t", "--time", dest="TME", help="Time as hour.")
parser.add_option(
    "-r",
    "--removeall",
    dest="RMA",
    help="Removes all current active tasks of called function's category.",
    action="store_true",
)
parser.add_option("-f", "--fromtimed", dest="FRT")

(options, args) = parser.parse_args()
options = vars(options)
