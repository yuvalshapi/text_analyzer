import pandas as pd
import task6.task6 as task6
import json


class IndirectConnector:
    def __init__(self,
                 sentences_file_path: str,
                 name_file_path: str = None,
                 remove_words_file_path: str = None,
                 people_connections_path: str = None,
                 is_processed: bool = False,
                 window_size: int = 1,
                 threshold: int = 2,
                 fixed_len: int = None):
        """
        Initializes the IndirectConnector with input data and parameters.

        :param sentences_file_path: Path to the sentences file (CSV or preprocessed JSON).
        :param name_file_path: Path to the names file (optional).
        :param remove_words_file_path: Path to the file with words to remove (optional).
        :param people_connections_path: Path to the JSON file containing pairs to check.
        :param is_processed: If True, assumes the input is already preprocessed.
        :param window_size: The size of the sentence window to check.
        :param threshold: Minimum number of shared windows to create a connection.
        """
        if is_processed:
            # Load preprocessed data
            data = pd.read_json(sentences_file_path)
            # Normalize list_of_connections to match task6.ConnectionFinder output
            self.list_of_connections = [
                [" ".join(conn[0]), " ".join(conn[1])] for conn in data["Question 6"]["Pair Matches"]
            ]
        else:
            data = task6.ConnectionFinder(
                sentences_file_path, name_file_path, remove_words_file_path,
                is_processed, window_size, threshold
            )
            self.list_of_connections = data.get_list_of_connections()

        # Load pairs to check
        pc_data = pd.read_json(people_connections_path)
        self.pairs_to_check = pc_data[pc_data.columns[0]].tolist()

        # Initialize graph and results
        self.graph_of_connections = {}
        self.results_list = []
        self.fixed_len = fixed_len
        self._build_graph()
        self._check_connections_with_length()

    def _build_graph(self):
        """
        Builds a graph (adjacency list) from the list of connections.
        The graph represents connections as a dictionary where each key is a person,
        and the value is a set of connected people.
        """
        for connection in self.list_of_connections:
            # Extract the two names from the connection list
            name1, name2 = connection  # Directly unpack the two names

            # Initialize nodes in the graph if not already present
            if name1 not in self.graph_of_connections:
                self.graph_of_connections[name1] = set()
            if name2 not in self.graph_of_connections:
                self.graph_of_connections[name2] = set()

            # Add the connection
            self.graph_of_connections[name1].add(name2)
            self.graph_of_connections[name2].add(name1)

        # Debugging output to check the graph structure
        print("Graph of Connections:", self.graph_of_connections)

    def _check_pair_with_length(self, start: str, target: str) -> bool:
        """
        Uses DFS to find all paths from `start` to `target` and checks if any has exactly `self.fixed_len` hops.

        :param start: Starting person (node).
        :param target: Target person (node).
        :return: True if there exists a path of exactly `self.fixed_len` hops; otherwise, False.
        """
        if start not in self.graph_of_connections or target not in self.graph_of_connections:
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

            for neighbor in self.graph_of_connections.get(node, set()):
                if neighbor not in visited:  # Avoid visiting the same node twice in a path
                    if dfs(neighbor, depth + 1, visited.copy()):  # Use a new visited set per path
                        return True  # If we found a valid path, return True immediately

            return False  # No valid path found

        return dfs(start, 0, set()) if self.fixed_len is not None else self._check_any_connection(start, target)

    def _check_any_connection(self, start: str, target: str) -> bool:
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
                queue.extend(self.graph_of_connections.get(current, set()))

        return False  # No connection found

    def _check_connections_with_length(self):
        """
        Checks all pairs in the list to see if they are connected in the graph.
        - If `self.fixed_len` is provided, checks for exact k-hop connections.
        - If `self.fixed_len` is None, checks for any connection.

        Updates the results list with the connection status for each pair.
        """
        self.pairs_to_check = [sorted(pair) for pair in self.pairs_to_check]
        self.pairs_to_check.sort()  # Sort the entire list of pairs alphabetically

        print(f"DEBUG: Checking connections with fixed_len={self.fixed_len}")

        for pair in self.pairs_to_check:
            name1, name2 = pair
            is_connected = self._check_pair_with_length(name1, name2)
            self.results_list.append([name1, name2, is_connected])  # Append with connection result

            # Debugging output
            print(f"DEBUG: {name1} -> {name2} = {is_connected} at fixed_len={self.fixed_len}")

    def to_json(self) -> str:
        """
        Converts the results into JSON format.
        - Uses "Question 7" if `self.fixed_len` is None (any connection).
        - Uses "Question 8" if `self.fixed_len` has a value (fixed-length paths).
        """
        question_key = "Question 7" if self.fixed_len is None else "Question 8"

        output = {
            question_key: {
                "Pair Matches": self.results_list
            }
        }

        return json.dumps(output, indent=4)

    def __str__(self):
        """
        String representation of the class.
        """
        return self.to_json()

    def get_json_format(self):
        """
        Public method to get the JSON representation.
        """
        return self.to_json()
