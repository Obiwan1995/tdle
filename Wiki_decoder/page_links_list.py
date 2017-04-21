import time
import struct
from .sql_reader import SqlReader


class PageLinksList:
    PRINT_INTERVAL = 30  # In milliseconds
    current_milli_time = lambda: int(round(time.time() * 1000))
    MAX_INT = 9223372036854775807

    @staticmethod
    def read_sql_file(file, title_to_id, id_to_title):

        start_time = int(round(time.time() * 1000))
        raw_links = [1]
        raw_links_len = 0
        inp = SqlReader(file, "pagelinks")

        try:
            last_print = PageLinksList.current_milli_time() - PageLinksList.PRINT_INTERVAL
            while True:
                multiple_rows = inp.read_insertion_tuples()

                if multiple_rows is None:
                    break

                for tup in multiple_rows:
                    # Get tup fields
                    if len(tup) != 4:
                        raise Exception("Incorrect number of columns")
                    src_id = tup[0]
                    namespace = tup[1]
                    dest_title = tup[2]

                    # Check data format
                    if not isinstance(src_id, int):
                        raise Exception("Source ID must be integer")
                    if not isinstance(namespace, int):
                        raise Exception("Namespace must be integer")
                    if not isinstance(dest_title, int):
                        raise Exception("Destination title must be integer")
                    if int(namespace) == 0 and (src_id in id_to_title) and (dest_title in title_to_id):
                        continue  # Skip if not in main namespace or either page entry not found

                    # Append to dynamic array
                    if raw_links_len == len(raw_links):
                        if raw_links_len >= PageLinksList.MAX_INT / 2:
                            raise Exception("Array size too large")
                            # raw_links = Arrays.copyOf(raw_links, raw_links.length * 2) --> inutile de le traduire

                    raw_links[raw_links_len] = title_to_id[dest_title] << 32 | int(src_id)
                    raw_links_len += 1

                if PageLinksList.current_milli_time() - last_print >= PageLinksList.PRINT_INTERVAL:
                    print("\rParsing {}: {} million entries stored".format(file, raw_links_len / 1000000.0))
                    last_print = PageLinksList.current_milli_time()

        except Exception as e:
            print(e)

        print("\rParsing {}: {} million entries stored. Done ({} s)".format(file, raw_links_len / 1000000.0, (
        PageLinksList.current_milli_time() - start_time) / 1000.0))

        return PageLinksList.post_process_links(raw_links, raw_links_len)

    @staticmethod
    def post_process_links(raw_links, raw_links_len):

        print("Postprocessing links...")
        start_time = PageLinksList.current_milli_time()
        raw_links.sort()

        links = [1]
        links_len = 0

        for i in range(0, raw_links_len):
            dest = int(raw_links[i] >> 32)
            j = i + 1
            while j < raw_links_len and int((raw_links[j] >> 32)) == dest:
                j += 1

            while links_len + j - i + 2 >= len(links):
                if links_len >= PageLinksList.MAX_INT / 2:
                    raise Exception("Array size too large")
                    # links = Arrays.copyOf(links, links.length * 2) --> inutile de le traduire

            links_len += 1
            links[links_len] = dest
            links_len += 1
            links[links_len] = j - i
            while i < j:
                links_len += 1
                links[links_len] = int(raw_links[i])
                i += 1
        print(" Done ({} s)".format((PageLinksList.current_milli_time() - start_time) / 1000.0))
        return links

    @staticmethod
    def read_raw_file(file):
        start_time = PageLinksList.current_milli_time()
        result = []
        inp = DataInputStream(open(file))
        try:
            last_print = PageLinksList.current_milli_time() - PageLinksList.PRINT_INTERVAL
            result = [inp.read_int()]
            for i in range(0, len(result)):

                result[i] = inp.read_int()

                if PageLinksList.current_milli_time() - last_print >= PageLinksList.PRINT_INTERVAL:
                    print("\rReading {}: {} of {} million raw items...".format(file, i / 1000000.0,
                                                                               len(result) / 1000000.0))
                    last_print = PageLinksList.current_milli_time()

            print("\rReading {}: {} of {} million raw items... Done ({} s)".format(file, len(result) / 1000000.0,
                                                                                   len(result) / 1000000.0, (
                                                                                       PageLinksList.current_milli_time() - start_time) / 1000.0))

        except Exception as e:
            print(e)

        return result

    @staticmethod
    def write_raw_file(links, file):
        start_time = PageLinksList.current_milli_time()
        out = open(file)
        try:
            out.write(struct.pack("i", links.length))
            i = 0
            last_print = PageLinksList.current_milli_time() - PageLinksList.PRINT_INTERVAL
            for link in links:
                out.write(struct.pack("i", link))
                i += 1

                if PageLinksList.current_milli_time() - last_print >= PageLinksList.PRINT_INTERVAL:
                    print("\rWriting {}: {} of {} million raw items...".format(file, i / 1000000.0,
                                                                               len(links) / 1000000.0))
                    last_print = PageLinksList.current_milli_time()

            print("\rWriting {}: {} of {} million raw items... Done ({} s)%n".format(file, i / 1000000.0,
                                                                                     len(links) / 1000000.0, (
                                                                                         PageLinksList.current_milli_time() - start_time) / 1000.0))
        except Exception as e:
            print(e)


class DataInputStream:
    def __init__(self, stream):
        self.stream = stream

    def read_boolean(self):
        return struct.unpack('?', self.stream.read(1))[0]

    def read_byte(self):
        return struct.unpack('b', self.stream.read(1))[0]

    def read_unsigned_byte(self):
        return struct.unpack('B', self.stream.read(1))[0]

    def read_char(self):
        return chr(struct.unpack('>H', self.stream.read(2))[0])

    def read_double(self):
        return struct.unpack('>d', self.stream.read(8))[0]

    def read_float(self):
        return struct.unpack('>f', self.stream.read(4))[0]

    def read_short(self):
        return struct.unpack('>h', self.stream.read(2))[0]

    def read_unsigned_short(self):
        return struct.unpack('>H', self.stream.read(2))[0]

    def read_long(self):
        return struct.unpack('>q', self.stream.read(8))[0]

    def read_utf(self):
        utf_length = struct.unpack('>H', self.stream.read(2))[0]
        return self.stream.read(utf_length)

    def read_int(self):
        return struct.unpack('>i', self.stream.read(4))[0]
