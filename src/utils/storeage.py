import json
import os


class Storage:
    def __init__(self, filepath: str) -> None:
        if not filepath.endswith(".json"):
            raise ValueError("Invalid filepath! Add filepath ending with .json!")
        self.filepath = filepath

    def _check_storage(self):
        """Check if storage file exists. If not create one."""
        if not os.path.isfile(self.filepath):
            with open(self.filepath, "w") as file:
                file.write(json.dumps({}))

    def _read_storage(self) -> dict:
        """Read storage file.

        Returns:
            dict: Dictionary containing the storage data
        """
        with open(self.filepath, "r") as file:
            return json.load(file)

    def _write_stores(self, data: dict):
        """Write data to storage file.

        Args:
            data (dict): Data to write to storage file
        """
        with open(self.filepath, "w") as file:
            file.write(json.dumps(data))

    def save_objs(self, objs: dict) -> list:
        """Save object to storage file.

        Args:
            objs (dict): List of scraped objects

        Returns:
            list: List of ids for updated objects
        """

        # Check if storage file exits
        self._check_storage()

        # Init variables
        update_objs = []
        deleted_obj = 0
        marked_deleted = 0
        unmarked_deleted = 0

        # Read storage
        stored_data = self._read_storage()

        # Define which ids(objs) to check
        existing_id = [id for id in stored_data.keys()]
        new_ids = [id for id in objs.keys()]
        obj_id_check = list(set(existing_id + new_ids))

        # For each object to check, find out how to handle
        # this object...
        for id in obj_id_check:
            # ... delete obj
            if id in existing_id and id not in new_ids:
                obj = stored_data.get(id)

                # check if obj is not found the first time
                if not obj.get("marked_deleted", False):
                    # if yes mark as deleted
                    stored_data[id]["marked_deleted"] = True
                    marked_deleted += 1

                    continue

                stored_data.pop(id, None)
                deleted_obj += 1

            # ... add obj
            if id not in existing_id and id in new_ids:
                objs[id]["marked_deleted"] = False
                stored_data[id] = objs[id]
                update_objs.append(id)

            # ... update obj
            if id in existing_id and id in new_ids:
                # if obj was marked as deleted unmark it
                if stored_data[id]["marked_deleted"]:
                    stored_data[id]["marked_deleted"] = False
                    unmarked_deleted += 1

        # Write data to storage file
        self._write_stores(data=stored_data)

        # Log changes to command line
        print(f"New objects found: {len(update_objs)}")
        print(f"Marked as deleted: {marked_deleted}")
        print(f"Unmarked as deleted: {unmarked_deleted}")
        print(f"Deleted objects: {deleted_obj}")
        print(f"Still open objects: {len(stored_data)-len(update_objs)}")

        return update_objs

    def get_values(self, key, filter_deleted=True):
        """
        Extracts all values associated with the specified key from the data storage.

        :param key: The key to extract values for
        :param filter_deleted: Whether to exclude deleted entries (default: True)
        :return: List of all values associated with the specified key
        """
        data = self._read_storage()  # Fetch the data
        values = [
            item[key]
            for item in data.values()
            if key in item and (not filter_deleted or not item.get("deleted", False))
        ]
        return values

    def get_all(self):
        """
        Extracts all entries from the data storage.

        :param filter_deleted: Whether to exclude deleted entries (default: True)
        :return: List of all entries
        """
        return self._read_storage()
