import pandas as pd
import os
import json
import task1.textprocessor as tp
import general_files.general_functions as gf
import  general_files.json_formats as j_formats

class ConnectionFinder:
    def __init__(self,
                 processed_data: tp.TextPreprocessor,
                 w_size: int,
                 threshold:int,
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
        #Not needed in task 6
        if people_connections_path is not None:
            # Load pairs to check
            pc_data = pd.read_json(people_connections_path)
            self.pairs_to_check = pc_data[pc_data.columns[0]].tolist()

    def _create_windows_dict(self):
        """
        Creates a dictionary where each person maps to the windows they appear in.

        A window is a list of consecutive sentences determined by the window size.
        This checks all variations of a name (including nicknames).
        """
        #Get the processed data from the text processor
        names_dict = self.processed_data.get_dict_of_names()
        sentences_list = self.processed_data.get_processed_sentences()
        people_windows_dict = {}

        #Create all the possible windows
        windows_list = gf.create_all_sublists(sentences_list,self.w_size)

        for window in windows_list:
            for name in names_dict:
                # Create variations of the name and nicknames as lists of words
                name_variations = [[word] for word in name.split()]  # Words from full name
                name_variations.extend([nickname.split() for nickname in names_dict[name]])  # Nicknames

                if gf.is_appear(window, name_variations):  # Check if the person appears in the window
                    if name not in people_windows_dict:
                        people_windows_dict[name] = []  # Initialize if not already present
                    people_windows_dict[name].append(window)

        # Sort the dictionary alphabetically by names
        people_windows_dict = dict(sorted(people_windows_dict.items()))
        return  people_windows_dict

    def calculate_shared_windows(self):
        """
        Calculates the number of shared windows between each pair of people.

        :return: A dictionary where keys are tuples of two names and values are the count of shared windows.
        """
        people_windows_dict = self._create_windows_dict()
        pair_count_dict = {}
        names = list(people_windows_dict.keys())  # All people

        # Compare each pair of people
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                name1, name2 = names[i], names[j]
                windows1 = people_windows_dict[name1]
                windows2 = people_windows_dict[name2]

                # Count shared windows
                shared_count = sum(1 for window1 in windows1 for window2 in windows2 if window1 == window2)

                # Store the count if there are shared windows
                if shared_count > 0:
                    pair_count_dict[(name1, name2)] = shared_count

        return pair_count_dict

    def _find_connections(self):
        """
        Finds all connections between people based on the threshold.

        If two people share windows above the threshold, they are added as a connection.
        """
        #Accumelate the windows using the previous functions
        full_connections_dict = self.calculate_shared_windows()
        people_connections_list = []

        for names, num_of_connections in full_connections_dict.items():
            if num_of_connections >= self.threshold:
                people_connections_list.append(sorted(names))  # Ensure names are in alphabetical order
        return people_connections_list

    def find_connections(self):
        people_connections_list = self._find_connections()
        formatted_result = j_formats.json_format_t6(people_connections_list)
        return json.dumps(formatted_result, indent=4)

    def _build_graph(self):
        """
        Builds a graph (adjacency list) from the list of connections.
        The graph represents connections as a dictionary where each key is a person,
        and the value is a set of connected people.
        """
        list_of_connections = self._find_connections()
        graph_of_connections = {}
        results_list = []

        for connection in list_of_connections:
            # Extract the two names from the connection list
            name1, name2 = connection  # Directly unpack the two names

            # Initialize nodes in the graph if not already present
            if name1 not in graph_of_connections:
                graph_of_connections[name1] = set()
            if name2 not in graph_of_connections:
                graph_of_connections[name2] = set()

            # Add the connection
            graph_of_connections[name1].add(name2)
            graph_of_connections[name2].add(name1)

        return graph_of_connections

    def _check_pair_with_length(self, start: str, target: str) -> bool:
        """
        Uses DFS to find all paths from `start` to `target` and checks if any has exactly `self.fixed_len` hops.

        :param start: Starting person (node).
        :param target: Target person (node).
        :return: True if there exists a path of exactly `self.fixed_len` hops; otherwise, False.
        """
        graph_of_connections = self._build_graph()
        if start not in graph_of_connections or target not in graph_of_connections:
            return False  # If nodes are not in the graph, return False

        def dfs(node, depth, visited):
            """
            Recursive DFS function.

            :param node: Current node.
            :param depth: Current depth of traversal.
            :param visited: Set of visited nodes (to avoid cycles in the same path).
            :return: True if an exact-length path is found, False otherwise.
            """
            if node == target:
                return depth == self.fixed_len  # Check if we reached the target at the correct depth

            if depth >= self.fixed_len:  # Stop searching if we exceed the required depth
                return False

            visited.add(node)  # Mark node as visited for this path

            for neighbor in graph_of_connections.get(node, set()):
                if neighbor not in visited:  # Avoid visiting the same node twice in a path
                    if dfs(neighbor, depth + 1, visited.copy()):  # Use a new visited set per path
                        return True  # If we found a valid path, return True immediately

            return False  # No valid path found

        return dfs(start, 0, set()) if self.fixed_len is not None else self._check_any_connection(start, target,graph_of_connections)

    def _check_any_connection(self, start: str, target: str,graph_of_connections) -> bool:
        """
        Standard BFS to check if any connection exists between `start` and `target`.
        Used for Task 7 when `self.fixed_len` is None.
        """
        from collections import deque

        queue = deque([start])
        visited = set()

        while queue:
            current = queue.popleft()
            if current == target:
                return True

            if current not in visited:
                visited.add(current)
                queue.extend(graph_of_connections.get(current, set()))

        return False  # No connection found

    def _check_connections_with_length(self):
        """
        Checks all pairs in the list to see if they are connected in the graph.
        - If `self.fixed_len` is provided, checks for exact k-hop connections.
        - If `self.fixed_len` is None, checks for any connection.

        Updates the results list with the connection status for each pair.
        """
        results_list = []
        self.pairs_to_check = [sorted(pair) for pair in self.pairs_to_check]
        self.pairs_to_check.sort()  # Sort the entire list of pairs alphabetically


        for pair in self.pairs_to_check:
            name1, name2 = pair
            is_connected = self._check_pair_with_length(name1, name2)
            results_list.append([name1, name2, is_connected])  # Append with connection result
        return results_list

    def check_connections(self):
        results_list = self._check_connections_with_length()
        print(results_list)
        formatted_results = j_formats.json_format7_8(results_list,self.processed_data.get_task_num())
        return json.dumps(formatted_results, indent = 4)
