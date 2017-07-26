from collections import deque
from DataModel.enums import Color, Shape, Pattern, Size
from DataModel.Symbol import Symbol
from DataModel.SimpleObject import SimpleObject
from DataModel.CombinedObject import CombinedObject


def calculate_objects_similarity(object_1, object_2, color_weight, shape_weight, size_weight,
                                 pattern_weight, symbols_weight):
    if isinstance(object_1, SimpleObject) and isinstance(object_2, SimpleObject):
        return calculate_simple_object_to_simple_object_similarity(
            object_1,
            object_2,
            color_weight,
            shape_weight,
            size_weight,
            pattern_weight,
            symbols_weight)
    if isinstance(object_1, CombinedObject) and isinstance(object_2, CombinedObject):
        return calculate_combine_object_to_combined_object_similarity()


def calculate_combine_object_to_combined_object_similarity(object_1, object_2, color_weight, shape_weight, size_weight,
                                                           pattern_weight, parts_weight, symbols_weight):
    shape_similarity = calculate_shapes_similarity(object_1.shape, object_2.shape)
    width_similarity = calculate_size_similarity(object_1.width, object_2.width)
    height_similarity = calculate_size_similarity(object_1.height, object_2.height)
    parts_similarity = calculate_list_similarity(object_1.parts, object_2.parts, color_weight, shape_weight,
                                                 size_weight, pattern_weight, symbols_weight)
    result = shape_similarity * shape_weight + \
        width_similarity * size_weight + \
        height_similarity * size_weight + \
        parts_similarity * parts_weight
    result = result / 4.0
    return result


def calculate_simple_object_to_combined_object_similarity(simple_object, combined_object):
    return 0.0


def calculate_simple_object_to_simple_object_similarity(object_1, object_2, color_weight, shape_weight, size_weight,
                                                        pattern_weight, symbols_weight):
    color_similarity = calculate_colors_similarity(object_1.color, object_2.color)
    shape_similarity = calculate_shapes_similarity(object_1.shape, object_2.shape)
    width_similarity = calculate_size_similarity(object_1.width, object_2.width)
    height_similarity = calculate_size_similarity(object_1.height, object_2.height)
    pattern_similarity = calculate_pattern_similarity(object_1.pattern, object_2.pattern)
    pattern_color_similarity = calculate_colors_similarity(object_1.pattern_color, object_2.pattern_color)
    symbols_similarity = calculate_list_similarity(object_1.symbols, object_2.symbols, color_weight, shape_weight,
                                                   size_weight, pattern_weight, symbols_weight)
    result = color_similarity * color_weight + \
        shape_similarity * shape_weight + \
        width_similarity * size_weight + \
        height_similarity * size_weight + \
        pattern_similarity * pattern_weight + \
        pattern_color_similarity * color_weight + \
        symbols_similarity * symbols_weight
    result = result / 7.0
    return result


def calculate_list_similarity(list_1, list_2, color_weight, shape_weight, size_weight, pattern_weight, symbols_weight):
    # if list_1 and list_2 have different length than list_2 should be the one that is longer
    if len(list_1) > len(list_2):
        temp = list_1
        list_1 = list_2
        list_2 = temp
    similarities_matrix = []
    for list_item in list_1:
        similarities_matrix.append(_get_all_similarities(list_item, list_2, color_weight, shape_weight, size_weight,
                                                         pattern_weight, symbols_weight))
    _remove_duplicate_bindings(similarities_matrix)
    similarities = [row[0][1] for row in similarities_matrix]
    sum_of_similarities = sum(similarities)
    return sum_of_similarities / len(list_2)


def _get_all_similarities(entity, list_of_entities, color_weight, shape_weight, size_weight, pattern_weight,
                          symbols_weight):
    queue = deque()
    for other_entity in list_of_entities:
        if isinstance(entity, Symbol):
            temp = calculate_symbol_to_symbol_similarity(entity, other_entity, color_weight, shape_weight, size_weight)
        elif isinstance(entity, SimpleObject):
            temp = calculate_simple_object_to_simple_object_similarity(entity, other_entity, color_weight, shape_weight,
                                                                       size_weight, pattern_weight, symbols_weight)
        queue.append((other_entity, temp))
    return sorted(queue, key=lambda pair: pair[1], reverse=True)


def _remove_duplicate_bindings(similarities_matrix):
    first_column = [row[0] for row in similarities_matrix]
    seen = set()
    indexes = []
    index = 0
    for element in first_column:
        if element[0] in seen:
            indexes.append([index])
        else:
            seen.add(element)
        index += 1

    if len(indexes) == 0:
        return similarities_matrix

    for index in indexes:
        row = similarities_matrix[index]
        queue = deque(row)
        first = queue.popleft()
        queue.append(first)
        similarities_matrix[index] = list(queue)

    return _remove_duplicate_bindings(similarities_matrix)


def calculate_symbol_to_symbol_similarity(symbol_1, symbol_2, color_weight, shape_weight, size_weight):
    color_similarity = calculate_colors_similarity(symbol_1.color, symbol_2.color)
    shape_similarity = calculate_shapes_similarity(symbol_1.shape, symbol_2.shape)
    width_similarity = calculate_size_similarity(symbol_1.width, symbol_2.width)
    height_similarity = calculate_size_similarity(symbol_1.height, symbol_2.height)
    result = color_similarity * color_weight + \
        shape_similarity * shape_weight + \
        width_similarity * size_weight + \
        height_similarity * size_weight
    result = result / 4.0
    return result


def calculate_colors_similarity(color_1, color_2):
    if color_1 == color_2:
        return 1.0
    if not {Color.RED, Color.VIOLET} - {color_1, color_2}:
        return 0.25
    if not {Color.BLUE, Color.VIOLET} - {color_1, color_2}:
        return 0.25
    if not {Color.YELLOW, Color.GREEN} - {color_1, color_2}:
        return 0.25
    if color_1 == Color.NONE or color_2 == Color.NONE:
        return 0.0
    return 0.0


def calculate_shapes_similarity(shape_1, shape_2):
    if shape_1 == shape_2:
        return 1.0
    if not {Shape.TRIANGLE, Shape.EQUILATERAL_TRIANGLE} - {shape_1, shape_2}:
        return 0.8
    if not {Shape.TRIANGLE, Shape.ISOSCELES_TRIANGLE} - {shape_1, shape_2}:
        return 0.8
    if not {Shape.ISOSCELES_TRIANGLE, Shape.EQUILATERAL_TRIANGLE} - {shape_1, shape_2}:
        return 0.8
    if not {Shape.SQUARE, Shape.RECTANGLE} - {shape_1, shape_2}:
        return 0.75
    if not {Shape.RHOMBUS, Shape.PARALLELOGRAM} - {shape_1, shape_2}:
        return 0.75
    if not {Shape.PARALLELOGRAM, Shape.TRAPEZIUM} - {shape_1, shape_2}:
        return 0.4
    if not {Shape.QUADRILATERAL, Shape.SQUARE} - {shape_1, shape_2}:
        return 0.25
    if not {Shape.QUADRILATERAL, Shape.RECTANGLE} - {shape_1, shape_2}:
        return 0.25
    if not {Shape.QUADRILATERAL, Shape.RHOMBUS} - {shape_1, shape_2}:
        return 0.25
    if not {Shape.QUADRILATERAL, Shape.PARALLELOGRAM} - {shape_1, shape_2}:
        return 0.25
    if not {Shape.QUADRILATERAL, Shape.TRAPEZIUM} - {shape_1, shape_2}:
        return 0.25
    if not {Shape.QUADRILATERAL, Shape.KITE} - {shape_1, shape_2}:
        return 0.25
    if not {Shape.PENTAGON, Shape.QUADRILATERAL} - {shape_1, shape_2}:
        return 0.4
    if not {Shape.PENTAGON, Shape.PARALLELOGRAM} - {shape_1, shape_2}:
        return 0.3
    if not {Shape.PENTAGON, Shape.RECTANGLE} - {shape_1, shape_2}:
        return 0.2
    if not {Shape.HEXAGON, Shape.PENTAGON} - {shape_1, shape_2}:
        return 0.3
    if not {Shape.HEPTAGON, Shape.HEXAGON} - {shape_1, shape_2}:
        return 0.3
    if not {Shape.OCTAGON, Shape.HEPTAGON} - {shape_1, shape_2}:
        return 0.3
    if not {Shape.CIRCLE, Shape.OCTAGON} - {shape_1, shape_2}:
        return 0.4
    if not {Shape.ELLIPSE, Shape.CIRCLE} - {shape_1, shape_2}:
        return 0.8
    if not {Shape.KITE, Shape.RHOMBUS} - {shape_1, shape_2}:
        return 0.75
    if not {Shape.PARALLELOGRAM, Shape.KITE} - {shape_1, shape_2}:
        return 0.75
    if not {Shape.ELLIPSE, Shape.OCTAGON} - {shape_1, shape_2}:
        return 0.4
    if not {Shape.POLYGON, Shape.CIRCLE} - {shape_1, shape_2}:
        return 0.5
    if not {Shape.POLYGON, Shape.ELLIPSE} - {shape_1, shape_2}:
        return 0.5
    if shape_1 == Shape.INVALID or shape_2 == Shape.INVALID:
        return 0.0
    return 0.0


def calculate_pattern_similarity(pattern_1, pattern_2):
    if pattern_1 == pattern_2:
        return 1.0
    if not {Pattern.HORIZONTAL_LINES, Pattern.LEFT_INCLINED_LINES} - {pattern_1, pattern_2}:
        return 0.75
    if not {Pattern.HORIZONTAL_LINES, Pattern.RIGHT_INCLINED_LINES} - {pattern_1, pattern_2}:
        return 0.75
    if not {Pattern.VERTICAL_LINES, Pattern.LEFT_INCLINED_LINES} - {pattern_1, pattern_2}:
        return 0.75
    if not {Pattern.VERTICAL_LINES, Pattern.RIGHT_INCLINED_LINES} - {pattern_1, pattern_2}:
        return 0.75
    if pattern_1 == Pattern.NONE or pattern_2 == Pattern.NONE:
        return 0.0
    return 0.0


def calculate_size_similarity(size_1, size_2):
    if size_1 == size_2:
        return 1.0
    if not {Size.TINY, Size.SMALL} - {size_1, size_2}:
        return 0.5
    if not {Size.SMALL, Size.MEDIUM} - {size_1, size_2}:
        return 0.5
    if not {Size.MEDIUM, Size.BIG} - {size_1, size_2}:
        return 0.5
    if not {Size.BIG, Size.LARGE} - {size_1, size_2}:
        return 0.5
    return 0.0
