import time
import gzip
from sql_reader import SqlReader

current_milli_time = lambda: int(round(time.time() * 1000))


class PageIdTitleMap:
    PRINT_INTERVAL = 30

    @staticmethod
    def read_sql_file(file):
        start_time = int(round(time.time() * 1000))
        result = dict()
        with gzip.open(file, 'rt') as f:
            inp = SqlReader(f, "page")
            last_print = current_milli_time() + PageIdTitleMap.PRINT_INTERVAL
            try:
                while True:
                    multiple_rows = inp.read_insertion_tuples()
                    if multiple_rows is None:
                        break
                    for tup in multiple_rows:
                        if len(tup) != 15:
                            raise Exception("Incorrect number of columns")
                        namespace = tup[1]
                        idn = tup[0]
                        title = tup[2]

                        if not isinstance(namespace, int):
                            raise Exception("Namespace must be integer")
                        if not isinstance(idn, int):
                            raise Exception("ID must be integer")
                        if not isinstance(title, str):
                            raise Exception("Title must be string")
                        if namespace != 0:
                            continue
                        if title in result.keys():
                            raise Exception("Duplicate page title")

                        result[title] = idn

                    if int(round(time.time() * 1000)) - last_print >= PageIdTitleMap.PRINT_INTERVAL:
                        print("Parsing {}: {} million entries stored...".format(file, len(result) / 1000000))
                        last_print = current_milli_time()
            except Exception as e:
                print(e)
            print("Parsing {}: {} million entries stored... Done ({} s)".format(file, len(result) / 1000000, (
                current_milli_time() - start_time) / 1000))
            return result

    @staticmethod
    def read_raw_file(file):
        start_time = current_milli_time()
        result = dict()
        with open(file, 'r') as inp:
            last_print = current_milli_time() - PageIdTitleMap.PRINT_INTERVAL
            i = 0
            for line in inp:
                line = line.strip()
                result[line] = int(inp.readline())

                if current_milli_time() - last_print >= PageIdTitleMap.PRINT_INTERVAL:
                    print("Reading {}: {} million entries...".format(file, i / 1000000))
                    last_print = current_milli_time()
                i += 1

            print("Reading {}: {} million entries... Done ({} s)".format(file, len(result) / 1000000, (
               current_milli_time() - start_time) / 1000))
        return result

    @staticmethod
    def write_raw_file(id_by_title, file):
        start_time = current_milli_time()
        with open(file, 'w') as out:
            try:
                i = 0
                last_print = current_milli_time() - PageIdTitleMap.PRINT_INTERVAL
                for title in id_by_title.keys():
                    out.write(title + "\n")
                    out.write(str(id_by_title[title]) + "\n")
                    i += 1

                if current_milli_time() - last_print >= PageIdTitleMap.PRINT_INTERVAL:
                    print("Writing {}: {} million entries...".format(file, i / 1000000))
                    last_print = current_milli_time()

                print("Reading {}: {} million entries... Done ({} s)".format(file, i / 1000000, (
                    current_milli_time() - start_time) / 1000))
            except Exception as e:
                print(e)

    @staticmethod
    def compute_reverse_map(hmap):
        print("Creating reverse mapping...")
        start_time = current_milli_time()

        result = dict()
        for key in hmap.keys():
            result[hmap[key]] = key

        print("Done ({} s)".format((current_milli_time() - start_time) / 1000))
        return result
