import pandas as pd
import json
import task1.textprocessor as tp
import text_analayzer_project_final.general_files.general_functions as gf
import text_analayzer_project_final.general_files.json_formats as j_formats


class ConnectionFinder:
    def __init__(self,
                 processed_data: tp.TextPreprocessor,
                 w_size: int,
                 threshold: int,
                 fixed_len: int,
                 people_connections_path: str = None):
        self.processed_data = processed_data
        self.w_size = w_size
        self.threshold = threshold
        self.people_connections_path = people_connections_path
        if fixed_len:
            self.fixed_len = int(fixed_len)
        else:
            self.fixed_len = None

        # Not needed in Task 6
        if people_connections_path is not None:
            # Load pairs to check
            pc_data = pd.read_json(people_connections_path)
            self.pairs_to_check = pc_data[pc_data.columns[0]].tolist()

    def _create_windows_dict(self):
        """
        Creates a dictionary where each person maps to the windows they appear in.
        A window is a list of consecutive sentences determined by the window size.
        """
        names_dict = self.processed_data.get_dict_of_names()
        sentences_list = self.processed_data.get_processed_sentences()
        people_windows_dict = {}

        windows_list = gf.create_all_sublists(sentences_list, self.w_size)

        for window in windows_list:
            for name in names_dict:
                name_variations = [[word] for word in name.split()]
                name_variations.extend([nickname.split() for nickname in names_dict[name]])

                if gf.is_appear(window, name_variations):
                    if name not in people_windows_dict:
                        people_windows_dict[name] = []
                    people_windows_dict[name].append(window)

        return dict(sorted(people_windows_dict.items()))

    def calculate_shared_windows(self):
        """Calculates the number of shared windows between each pair of people."""
        people_windows_dict = self._create_windows_dict()
        pair_count_dict = {}
        names = list(people_windows_dict.keys())

        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                name1, name2 = names[i], names[j]
                windows1 = people_windows_dict[name1]
                windows2 = people_windows_dict[name2]

                shared_count = sum(1 for window1 in windows1 for window2 in windows2 if window1 == window2)

                if shared_count > 0:
                    pair_count_dict[(name1, name2)] = shared_count

        return pair_count_dict

    def _find_connections(self):
        """Finds all connections between people based on the threshold."""
        full_connections_dict = self.calculate_shared_windows()
        people_connections_list = []

        for names, num_of_connections in full_connections_dict.items():
            if num_of_connections >= self.threshold:
                people_connections_list.append(sorted(names))

        return people_connections_list

    def find_connections(self):
        people_connections_list = self._find_connections()
        formatted_result = j_formats.json_format_t6(people_connections_list)
        return json.dumps(formatted_result, indent=4)

    def _build_graph(self):
        """Builds a graph (adjacency list) from the list of connections."""
        list_of_connections = self._find_connections()
        graph_of_connections = {}

        for connection in list_of_connections:
            name1, name2 = connection

            if name1 not in graph_of_connections:
                graph_of_connections[name1] = set()
            if name2 not in graph_of_connections:
                graph_of_connections[name2] = set()

            graph_of_connections[name1].add(name2)
            graph_of_connections[name2].add(name1)

        return graph_of_connections

    def _check_pair_with_length(self, start: str, target: str) -> bool:
        """Checks if a connection of exactly `self.fixed_len` exists between `start` and `target`."""
        graph_of_connections = self._build_graph()
        if start not in graph_of_connections or target not in graph_of_connections:
            return False

        def dfs(node, depth, visited):
            if node == target:
                return depth == self.fixed_len

            if depth >= self.fixed_len:
                return False

            visited.add(node)

            for neighbor in graph_of_connections.get(node, set()):
                if neighbor not in visited:
                    if dfs(neighbor, depth + 1, visited.copy()):
                        return True

            return False

        return dfs(start, 0, set())

    def _check_any_connection_task7(self, start: str, target: str) -> bool:
        """Task 7: Checks if any connection exists between `start` and `target` (no hop limit)."""
        graph_of_connections = self._build_graph()
        if start not in graph_of_connections or target not in graph_of_connections:
            return False

        from collections import deque

        queue = deque([start])
        visited = set()

        while queue:
            current = queue.popleft()
            if current == target:
                return True  # ✅ Found a connection

            if current not in visited:
                visited.add(current)
                queue.extend(graph_of_connections.get(current, set()))

        return False  # ❌ No connection found

    def _check_connections_with_length(self):
        """Task 8: Checks all pairs in the list to see if they are connected in exactly `self.fixed_len` hops."""
        results_list = []
        self.pairs_to_check = [sorted(pair) for pair in self.pairs_to_check]
        self.pairs_to_check.sort()

        for pair in self.pairs_to_check:
            name1, name2 = pair
            is_connected = self._check_pair_with_length(name1, name2)
            results_list.append([name1, name2, is_connected])

        return results_list

    def _check_any_connections(self):
        """Task 7: Checks all pairs for *any* connection (no hop limit)."""
        results_list = []
        self.pairs_to_check = [sorted(pair) for pair in self.pairs_to_check]
        self.pairs_to_check.sort()

        for pair in self.pairs_to_check:
            name1, name2 = pair
            is_connected = self._check_any_connection_task7(name1, name2)
            results_list.append([name1, name2, is_connected])

        return results_list

    def check_connections(self):
        """
        Runs Task 7 or Task 8 based on whether `fixed_len` is set:
        - If `fixed_len` is None → Task 7 (find *any* connection).
        - If `fixed_len` is set → Task 8 (find connection with exactly `fixed_len` hops).
        """
        if self.fixed_len is None:
            results_list = self._check_any_connections()  # ✅ Task 7
        else:
            results_list = self._check_connections_with_length()  # ✅ Task 8

        formatted_results = j_formats.json_format7_8(results_list, self.processed_data.get_task_num())
        return json.dumps(formatted_results, indent=4)
