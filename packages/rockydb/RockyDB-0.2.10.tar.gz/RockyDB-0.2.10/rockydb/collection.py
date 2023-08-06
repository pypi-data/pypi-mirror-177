from pathlib import Path
import json
import string
from rocksdict import (
    Rdict,
    Options,
    ReadOptions,
    WriteBatch,
    CompactOptions,
)
import random
from rockydb.index import Index
import rockydb.encoding as encoding
import os


class Collection:
    def __init__(self, db_path: str, name: str):
        self.db_path = db_path
        self.name = name
        self.path = self.db_path + name

        self.opt = Options(raw_mode=True)
        self.opt.increase_parallelism(os.cpu_count())
        self.opt.set_allow_mmap_reads(True)
        self.opt.set_write_buffer_size(0x10000000)

        self._create_dir(self.path, with_meta=True)
        self.collection = Rdict(path=self.path, options=self.opt)

        self.encoding_types = {
            str: 1,
            int: 2,
            float: 3,
            bool: 4,
            list: 5,
            1: str,
            2: int,
            3: float,
            4: bool,
            5: list,
        }

    def _create_dir(self, dir_path: str, with_meta: bool = False):
        if Path(dir_path).is_dir():
            return False

        # make directory
        db_path = Path(dir_path)
        db_path.mkdir(parents=True, exist_ok=True)

        # make meta file
        if with_meta:
            with open(dir_path + "/meta.json", "w") as f:
                json.dump([], f, indent=4)

        return True

    def _delete_old_logs(self):
        database_path = Path(self.path)
        database_files = list(database_path.iterdir())

        for filename in database_files:
            if filename.name[:7] == "LOG.old":
                filename.unlink()

    def _generate_id(self):
        characters = string.ascii_letters + string.digits
        doc_id = "".join(random.choice(characters) for _ in range(8))

        return doc_id

    def insert_object(self, document: object) -> str:
        document_dict = document.__dict__.copy()
        doc_id = self.insert(document_dict)

        return doc_id

    def insert(self, document: dict, wb: WriteBatch = None) -> str:
        # encoding method
        # collection_id/index_id/order_no/doc_id/col_id -> datatype_id/value
        # order_no is for sorting, will be 0 for default index

        if "_id" not in document:
            document["_id"] = self._generate_id()

        doc_id = document["_id"]

        for key, value in document.items():
            if key != "_id":
                key_string = f"{self.name}/0/0/{doc_id}/{key}"
                encoded_data = encoding.encode_this(value)
                encoded_data_type = encoding.encode_int(
                    self.encoding_types[type(value)]
                )  # byte of length 1

                encoded_key = encoding.encode_str(key_string)
                encoded_value = encoded_data_type + encoded_data

                # insert in db
                if wb is not None:
                    wb[encoded_key] = encoded_value
                else:
                    self.collection[encoded_key] = encoded_value
                    # print(f"{encoded_key} -> {encoding.decode_int(encoded_value)}")

        self._delete_old_logs()
        return doc_id

    def insert_batch(self, document_list: list):
        wb = WriteBatch(raw_mode=True)

        for document in document_list:
            self.insert(document, wb)

        self.collection.write(wb)

    def insert_object_batch(self, object_list: list):
        for object in object_list:
            self.insert_object(object)

    def _decode_value(self, value: bytes):
        if not value:
            return None

        decoded_data_type = self.encoding_types[value[0]]
        decoded_value = encoding.decode_this(decoded_data_type, value[1:])

        return decoded_value

    def _get(self, key: bytes):
        value = self.collection[key]
        return self._decode_value(value)

    def _iterate_keys(self):
        for key in self.collection.keys():
            yield key

        self._delete_old_logs()

    # def create_index(self, name: str, fields: list, batch: bool = False):
    #     index = Index(
    #         self.path,
    #         self.collection,
    #         self.name,
    #         name,
    #         fields,
    #         encoding_types=self.encoding_types,
    #     )
    #     index.create(batch)

    #     return index

    # def get_index(self, name: str):
    #     index = Index(
    #         self.path,
    #         self.collection,
    #         self.name,
    #         name,
    #         encoding_types=self.encoding_types,
    #     )
    #     index.get_index(name)

    #     return index

    def get_id_contains(self, field: str, value, max_count: int = None):
        all_ids = []

        for key in self._iterate_keys():
            decoded_key = encoding.decode_str(key).split("/")
            key_column = decoded_key[4]
            key_value = self._get(key)

            if (field == key_column) and key_value:
                if value in self._get(key):
                    row_id = decoded_key[3]
                    all_ids.append(row_id)

            if max_count:
                if len(all_ids) == max_count:
                    return all_ids

        return all_ids

    def _contains(self, field: str, value, max_count: int = None):
        results = []
        doc_ids = self.get_id_contains(field, value, max_count)

        if doc_ids:
            for doc_id in doc_ids:
                doc_dict = {}
                doc_dict["_id"] = doc_id

                for key in self._iterate_keys():
                    decoded_key = encoding.decode_str(key).split("/")
                    search_doc_id = decoded_key[3]

                    if search_doc_id == doc_id:

                        column_name = decoded_key[4]
                        doc_dict[column_name] = self._get(key)

                results.append(doc_dict)

        return results

    def find(self, query: dict, limit: int = 1):
        results = []
        if not query or not limit:
            return results

        lt = {}
        lte = {}
        gt = {}
        gte = {}
        eq = {}
        # need to iterate over keys and values once only
        for spec, v in query.items():
            q_loc = spec.find("?")

            if q_loc != -1:
                query_type = spec[q_loc + 1 :]

                # can only be of one type below
                if query_type == "lte":
                    lte[spec[:q_loc]] = v
                    continue

                if query_type == "gte":
                    gte[spec[:q_loc]] = v
                    continue

                if query_type == "lt":
                    lt[spec[:q_loc]] = v
                    continue

                if query_type == "gt":
                    gt[spec[:q_loc]] = v
                    continue

                print(f"Unkown query type {query_type}")
                return results

            else:
                # add to equals dict
                eq[spec] = v

        # iterate through all keys to find doc ids that match
        count = 0
        read_opt = ReadOptions(raw_mode=True)
        read_opt.fill_cache(False)
        read_opt.set_readahead_size(8_388_608)
        read_opt.set_tailing(True)
        read_opt.set_pin_data(True)

        for k, v in self.collection.items(read_opt=read_opt):
            decoded_key = encoding.decode_str(k).split("/")
            column = decoded_key[4]

            # check for equal
            if column in eq:
                if query[column] == self._decode_value(v):
                    results.append(self.get(decoded_key[3]))
                    count += 1

            if column in lte:
                if self._decode_value(v) <= lte[column]:
                    results.append(self.get(decoded_key[3]))
                    count += 1

            if column in gte:
                if self._decode_value(v) >= gte[column]:
                    results.append(self.get(decoded_key[3]))
                    count += 1

            if column in lt:
                if self._decode_value(v) < lt[column]:
                    results.append(self.get(decoded_key[3]))
                    count += 1

            if column in gt:
                if self._decode_value(v) > gt[column]:
                    results.append(self.get(decoded_key[3]))
                    count += 1

            if count == limit:
                break

        return results

    def delete(self, id: str) -> bool:
        found_doc = False
        writebatch = WriteBatch(raw_mode=True)

        for encoded_key in self._id_rows(id):
            writebatch.delete(encoded_key)
            found_doc = True

        self.collection.write(writebatch)

        return found_doc

    def _id_rows(self, id: str):
        key = encoding.encode_str(self.name + "/0/0/" + id)
        iter = self.collection.iter(ReadOptions(raw_mode=True))
        iter.seek(key)

        if not iter.key():
            return {}

        while iter.valid():
            encoded_key = iter.key()
            decoded_key = encoding.decode_str(encoded_key).split("/")
            if decoded_key[3] != id:
                break

            yield encoded_key
            iter.next()

    def delete_batch(self, id_list: list):
        for id in id_list:
            self.delete(id)

    def _delete_tmp_blocks(self):
        iter = self.collection.iter(ReadOptions(raw_mode=True))
        iter.seek(b"tmp/")

        while iter.valid():
            k = iter.key()
            if k[:3] != b"tmp":
                break

            self.delete(encoding.decode_str(k))
            iter.next()

    def get(self, id: str) -> dict:
        document = {}

        for encoded_key in self._id_rows(id):
            decoded_key = encoding.decode_str(encoded_key).split("/")

            column = decoded_key[4]
            document[column] = self._get(encoded_key)

        if not document:
            return None

        document["_id"] = id
        return document

    def get_batch(self, id_list: list):
        results = []

        for id in id_list:
            document = self.get(id)
            results.append(document)

        return results

    def create_index(self, name: str, field: str):
        index_id = 0
        # check if index already exists
        meta_file = self.path + "/meta.json"
        with open(meta_file, "r") as f:
            index_data = json.load(f)

        for index in index_data:
            if index["name"] == name:
                print("Index already exists, please choose a different index name")
                return None

            if index["id"] >= index_id:
                index_id = index["id"]

        index = Index(self.collection, self.name, name, index_id + 1, field)
        index_spec = index.create()

        # now delete all tmp blocks that were saved in db
        self._delete_tmp_blocks()

        # update meta file once index fully created
        index_data.append(index_spec)
        with open(self.path + "/meta.json", "w") as f:
            json.dump(index_data, f, indent=4)

        return index

    def get_index(self, name: str):
        pass

    def delete_index(self, name: str):
        pass

    def destroy(self):
        Rdict.destroy(self.path)

    def flush(self, wait: bool = False):
        self.collection.flush(wait)

    def compact_range(self, start: bytes = None, end: bytes = None):
        if not start or not end:
            iter = self.collection.iter(ReadOptions(raw_mode=True))
            iter.seek_to_first()
            start = iter.key()
            iter.seek_to_last()
            end = iter.key()

        self.collection.compact_range(start, end, CompactOptions())
