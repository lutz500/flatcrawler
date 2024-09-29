import json
import os


class Storage:
    def __init__(self, filepath: str) -> None:
        if not filepath.endswith(".json"):
            raise ValueError("Invalid filepath! Add filepath ending with .json!")
        self.filepath = filepath

    def _check_storage(self):
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w") as file:
                file.write(json.dumps({}))

    def _read_storage(self):
        with open(self.filepath, "r") as file:
            return json.load(file)

    def _write_stores(self, data: dict):
        with open(self.filepath, "w") as file:
            file.write(json.dumps(data))

    def save_objs(self, objs: dict):
        self._check_storage()

        update_objs = []
        deleted_obj = 0

        stored_data = self._read_storage()

        existing_id = [id for id in stored_data.keys()]
        new_ids = [id for id in objs.keys()]

        obj_id_check = list(set(existing_id + new_ids))

        for id in obj_id_check:
            print(id)

            if id in existing_id and id not in new_ids:
                stored_data.pop(id, None)
                deleted_obj += 1

            if id not in existing_id and id in new_ids:
                stored_data[id] = objs[id]
                update_objs.append(id)

        self._write_stores(data=stored_data)

        print(f"New objects found: {len(update_objs)}")
        print(f"Deleted objects: {deleted_obj}")
        print(f"Still open objects: {len(stored_data)-len(update_objs)}")

        return update_objs
