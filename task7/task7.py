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
                 threshold: int = 2):
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

    def _check_pair_with_length(self, start: str, target: str, k: int = None) -> bool:
        """
        Checks if there is a connection between two people using BFS.
        - If `k` is provided, only returns True if the connection is exactly `k` hops.
        - If `k` is not provided, returns True if any connection exists.

        :param start: Starting person (node).
        :param target: Target person (node).
        :param k: (Optional) The exact number of hops required to count as a connection.
        :return: True if there is a valid connection (any or exactly k hops), False otherwise.
        """
        from collections import deque

        queue = deque([(start, 0)])  # (current_person, depth)
        visited = set()

        while queue:
            current, depth = queue.popleft()

            if current == target:
                if k is None:
                    return True  # Act as before (any connection is valid)
                return depth == k  # Return True only if at exactly k hops

            if k is None or depth < k:  # Continue exploring if k isn't reached yet
                if current not in visited:
                    visited.add(current)
                    for neighbor in self.graph_of_connections.get(current, set()):
                        queue.append((neighbor, depth + 1))

        return False  # No connection found (either at all or at exact k hops)

    def _check_connections_with_length(self, k: int = None):
        """
        Checks all pairs in the list to see if they are connected in the graph.
        - If `k` is provided, checks for exact k-hop connections.
        - If `k` is not provided, checks for any connection.

        Updates the results list with the connection status for each pair.

        :param k: (Optional) The exact connection length to check for.
        """
        self.pairs_to_check = [sorted(pair) for pair in self.pairs_to_check]
        self.pairs_to_check.sort()  # Sort the entire list of pairs alphabetically

        for pair in self.pairs_to_check:
            name1, name2 = pair  # Names are already sorted alphabetically
            is_connected = self._check_pair_with_length(name1, name2, k)
            self.results_list.append([name1, name2, is_connected])  # Append with connection result


    def to_json(self) -> str:
        """
        Converts the results into JSON format.
        """
        output = {
            "Question 7": {
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
