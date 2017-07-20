import copy
import numpy as np


def unify_objects(frames, calculate_similarity, min_similarity_factor=0.5, work_on_copy=False):
    if work_on_copy:
        frames = copy.deepcopy(frames)
    prepare_frames(frames)

    connections = []
    for frame_index in range(0, len(frames)-1):
        for object_pair in frames[frame_index]:
            connection = create_object_connection(object_pair[1], frame_index, frames, min_similarity_factor, calculate_similarity)
            if len(connection) > 1:
                connections.append(connection)

    objects = []
    for connection in connections:
        objects.append(extract_unified_objects(connection, calculate_similarity))
    return objects


def prepare_frames(frames):
    # frames = [frame for frame in frames if frame != []]
    for frame_index in range(len(frames)):
        frames[frame_index] = map(lambda object: [None, object], frames[frame_index])


def create_object_connection(object, current_frame_index, frames, min_similarity_factor, calculate_similarity):
    connection = [object]
    for frame_index in range(current_frame_index + 1, len(frames)):
        next_node, next_node_index, next_node_similarity_factor = find_next_node(object,
                                                                                 frames[frame_index],
                                                                                 calculate_similarity)

        if next_node is None or next_node_similarity_factor < min_similarity_factor:
            continue
        if next_node[0] is not None:
            current_ancestor_similarity_factor = \
                calculate_similarity(next_node[0], next_node[1])
            if next_node_similarity_factor < current_ancestor_similarity_factor:
                continue

        next_node[0] = object
        object = next_node[1]
        connection.append(next_node[1])
    return connection


def find_next_node(single_object, next_frame, calculate_similarity):
    if next_frame == []:
        return None, None, None
    next_node_index = None
    similarity_factor = 0
    for index in range(0, len(next_frame)):
        next_single_object = next_frame[index][1]
        node_similarity_factor = calculate_similarity(single_object, next_single_object)
        if node_similarity_factor > similarity_factor:
            next_node_index = index
            similarity_factor = node_similarity_factor
    return next_frame[next_node_index], next_node_index, similarity_factor


def extract_unified_objects(connection, calculate_similarity):
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

'''
def extract_connections(frames):
    connections = []
    for frame_index in range(len(frames)):
        for object_tuple in frames[frame_index]:
            connection = _extract_connection_for_first_object(object_tuple[1], frame_index, frames)
            connection.append(connection)
    return connections


def _extract_connection_for_first_object(single_object, initial_frame_index, frames):
    connection = [single_object]
    temp_object = single_object
    for frame_index in range(initial_frame_index + 1, len(frames) - 1):
        next_node = _find_descendant(temp_object, frames[frame_index])
        if next_node is None:
            continue
        frames[frame_index].remove((temp_object, next_node))
        connection.append(next_node)
        temp_object = next_node
    return connection


def _find_descendant(single_object, frame):
    if frame == []:
        return None
    descendant = None
    current_index = 0
    while current_index < len(frame) and descendant is None:
        if frame[current_index][0] is single_object:
            descendant = frame[current_index][1]
        current_index += 1
    return descendant
'''

