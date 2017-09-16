from ObjectsUnification.similarity import SimilarityCalculator
from ObjectsUnification.unification import ObjectsUnificator
from ObjectsUnification.parameters_loader import load_all_from_file_for_similarity, load_all_from_file_for_unification
from ImageProcessing.ObjectDetector import ObjectDetector
from ImageProcessing.parameters_loader import load_all_from_file as load_all_from_file_for_object_detector
from Common.config import config
from Common.TCPConnections import TCPClient
from TCPServer import TCPServer
import Common.configurable_objects_factory
import paramiko


def create_object_detector():
    object_detector = ObjectDetector()
    load_all_from_file_for_object_detector(object_detector)
    return object_detector


def create_objects_unificator():
    similarity_calculator = SimilarityCalculator()
    load_all_from_file_for_similarity(similarity_calculator)
    objects_unificator = ObjectsUnificator()
    load_all_from_file_for_unification(objects_unificator)
    objects_unificator.calculate_similarity_function = similarity_calculator.calculate
    return objects_unificator


def create_tcp_server(main, logger):
    receive_address = config('TCPConnection/receive_address')
    receive_port = config('TCPConnection/receive_port')
    buffer_size = config('TCPConnection/buffer_size')
    socket_timeout = config('TCPConnection/socket_timeout')
    return TCPServer(receive_address, receive_port, buffer_size, socket_timeout, logger, main)


def create_tcp_client(logger):
    agent_address = config('TCPConnection/agent_address')
    agent_port = config('TCPConnection/agent_port')
    socket_timeout = config('TCPConnection/socket_timeout')
    return TCPClient(agent_address, agent_port, socket_timeout, logger)


def create_logger():
    return Common.configurable_objects_factory.create_logger()


def create_ssh_client():
    hostname = config('TCPConnection/agent_address')
    username = config('SSHConnection/username')
    password = config('SSHConnection/password')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname,
                   username=username,
                   password=password)
    return client
