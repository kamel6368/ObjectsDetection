from ObjectsUnification.similarity import SimilarityCalculator
from ObjectsUnification.unification import ObjectsUnificator
from ObjectsUnification.parameters_loader import load_all_from_file_for_similarity, load_all_from_file_for_unification


def create_object_detector():
    pass


def create_objects_unificator():
    similarity_calculator = SimilarityCalculator()
    load_all_from_file_for_similarity(similarity_calculator)
    objects_unificator = ObjectsUnificator()
    load_all_from_file_for_unification(objects_unificator)
    objects_unificator.calculate_similarity_function = similarity_calculator.calculate
    return objects_unificator


def create_tcp_server():
    pass


def create_tcp_client():
    pass