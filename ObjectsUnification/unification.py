import copy
import numpy as np


class ObjectsUnificator:

    def __init__(self):
        self.calculate_similarity_function = None
        self.min_similarity_factor = None
        self.min_connection_length_percentage = None
        self.work_on_copy = None

    def unify_objects(self, frames):
        return unify_objects(frames, self.calculate_similarity_function, self.min_similarity_factor,
                             self.min_connection_length_percentage, self.work_on_copy)


def unify_objects(frames, calculate_similarity, min_similarity_factor=0.5,
                  min_connection_length_percentage=0.5, work_on_copy=True):
    if work_on_copy:
        frames = copy.deepcopy(frames)
    _prepare_frames(frames)

    connections = []
    for frame_index in range(0, len(frames)-1):
        node_neighbours_dictionary = {}
        for object_pair in frames[frame_index]:
            connection = _create_object_connection(object_pair[1], frame_index, frames, min_similarity_factor,
                                                   calculate_similarity, node_neighbours_dictionary)
            if len(connection) > 1:
                connections.append(connection)

    objects = []
    for connection in connections:
        percentage_length = float(len(connection)) / len(frames)
        if percentage_length >= min_connection_length_percentage:
            objects.append(_extract_unified_objects(connection, calculate_similarity))
    return objects


def _prepare_frames(frames):
    for frame_index in range(len(frames)):
        frames[frame_index] = map(lambda object: [None, object], frames[frame_index])


def _create_object_connection(object, current_frame_index, frames, min_similarity_factor,
                              calculate_similarity, node_neighbours_dictionary):
    connection = [object]
    for frame_index in range(current_frame_index + 1, len(frames)):
        next_nodes_similarity_list = _find_next_node(object, frames[frame_index], calculate_similarity,
                                                     min_similarity_factor)
        if len(next_nodes_similarity_list) == 0:
            continue
        next_node = next_nodes_similarity_list[0][0]
        next_node_similarity_factor = next_nodes_similarity_list[0][1]
        node_neighbours_dictionary[object] = next_nodes_similarity_list
        next_nodes_similarity_list.pop(0)

        if next_node[0] is not None:
            current_ancestor_similarity_factor = \
                calculate_similarity(next_node[0], next_node[1])
            if next_node_similarity_factor < current_ancestor_similarity_factor:
                continue
            else:
                alternative_neighbours_list = node_neighbours_dictionary[next_node[0]]
                alternative_neighbour = alternative_neighbours_list[0]
                alternative_neighbour[0] = next_node[0]
                alternative_neighbours_list.pop(0)

        next_node[0] = object
        connection.append(next_node[1])
    return connection


def _find_next_node(single_object, next_frame, calculate_similarity, min_similarity_factor):
    if next_frame == []:
        return []

    next_nodes_similarity_list = []

    for index in range(0, len(next_frame)):
        if next_frame[index][0] is not None:
            continue
        next_single_object = next_frame[index][1]
        node_similarity_factor = calculate_similarity(single_object, next_single_object)
        if node_similarity_factor >= min_similarity_factor:
            next_nodes_similarity_list.append((next_frame[index], node_similarity_factor))

    next_nodes_similarity_list.sort(key=lambda tup: tup[1])
    return next_nodes_similarity_list


def _extract_unified_objects(connection, calculate_similarity):
    connection_length = len(connection)
    matrix = np.zeros((connection_length, connection_length))
    for obj_index in range(connection_length):
        for other_index in range(obj_index + 1, connection_length):
            similarity_factor = calculate_similarity(connection[obj_index], connection[other_index])
            matrix[obj_index][other_index] = similarity_factor
            matrix[other_index][obj_index] = similarity_factor
    matrix = np.sum(matrix, axis=1)
    max_index = np.argmax(matrix)
    final_object = connection[max_index]
    certainty_factor = matrix[max_index] / (connection_length - 1)
    return final_object, certainty_factor
