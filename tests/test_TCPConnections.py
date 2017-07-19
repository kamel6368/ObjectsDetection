import unittest
from mock import Mock
from Common.TCPConnections import TCPServer, TCPClient, ClientShutdownException


class MyTCPServer(TCPServer):
    def handle_message(self, command, content):
        pass

    def restart_callback(self):
        pass


class TCPClientTest(unittest.TestCase):

    def setUp(self):
        server_address = 'xxx'
        port = 123
        socket_timeout = 2
        logger_mock = Mock()
        self.tcp_client = TCPClient(server_address, port, socket_timeout, logger_mock)

    def test__prepare_message_should_return_as_expected_simple_data(self):
        command = 'COMMAND'
        content = 'ala ma kota'

        data = self.tcp_client._prepare_message(command, content)
        self.assertEqual('23|COMMAND|ala ma kota|', data)
        self.assertEqual(23, len(data))
        self.assertEqual(23, int(data.split('|')[0]))

    def test__prepare_message_should_return_as_expected_9_and_10_length(self):
        command = 'OBJECTS'
        content = ''

        data = self.tcp_client._prepare_message(command, content)
        self.assertEqual('12|OBJECTS||', data)
        self.assertEqual(12, len(data))
        self.assertEqual(12, int(data.split('|')[0]))

    def test__prepare_message_should_return_as_expected_19_and_20_length(self):
        command = 'OBJECTS'
        content = 'ala ma ko'

        data = self.tcp_client._prepare_message(command, content)
        self.assertEqual('21|OBJECTS|ala ma ko|', data)
        self.assertEqual(21, len(data))
        self.assertEqual(21, int(data.split('|')[0]))

    def test__prepare_message_should_return_as_expected_98_and_101_length(self):
        command = 'OBJECTS'
        content = 'ala ma kota ala ma kota ala ma kota ala ma kota ala ma kota ala ma kota ala ma kota alax'

        data = self.tcp_client._prepare_message(command, content)

        result_data = '101|OBJECTS|ala ma kota ala ma kota ala ma kota ala ma kota ala ma kota ala ma kota ala ma kota alax|'
        self.assertEqual(result_data, data)
        self.assertEqual(101, len(data))
        self.assertEqual(101, int(data.split('|')[0]))


class TCPServerTest(unittest.TestCase):

    def setUp(self):
        address = '127.0.0.1'
        port = 1234
        buffer_size = 1024
        socket_timeout = 3
        logger_mock = Mock()
        self.tcp_server = MyTCPServer(address, port, buffer_size, socket_timeout, logger_mock)

    def test__manage_chunk_read_simple_message(self):
        data = None
        msg_length = None
        chunk = '15|ala ma kota|'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_simple_message_with_buffer_number(self):
        data = None
        msg_length = None
        chunk = '|ala ma kota|'
        self.tcp_server.buffer = '15'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_simple_message_with_buffer_number_and_delimeter(self):
        data = None
        msg_length = None
        chunk = 'ala ma kota|'
        self.tcp_server.buffer = '15|'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_simple_message_with_buffer_number_and_delimeter_and_part_message(self):
        data = None
        msg_length = None
        chunk = 'a ma kota|'
        self.tcp_server.buffer = '15|al'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_second_part_of_message(self):
        data = '15|ala m'
        msg_length = 15
        chunk = 'a kota|'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_second_part_of_message_with_buffer(self):
        data = 'a m'
        msg_length = None
        chunk = 'a kota|'
        self.tcp_server.buffer = '15|al'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_incomplete_message(self):
        data = None
        msg_length = None
        chunk = '15|ala m'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala m', data)
        self.assertEqual(15, msg_length)
        self.assertFalse(is_complete_message)

    def test__manage_chunk_read_incomplete_message_with_data(self):
        data = '15'
        msg_length = 15
        chunk = '|ala m'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala m', data)
        self.assertEqual(15, msg_length)
        self.assertFalse(is_complete_message)

    def test__manage_chunk_read_incomplete_message_with_buffer(self):
        data = None
        msg_length = None
        chunk = 'ala m'
        self.tcp_server.buffer = '15|'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('15|ala m', data)
        self.assertEqual(15, msg_length)
        self.assertFalse(is_complete_message)

    def test__manage_chunk_invalid_message_should_raise_exception(self):
        data = None
        msg_length = None
        chunk = ''
        self.assertRaises(ClientShutdownException, self.tcp_server._manage_chunk, chunk, data, msg_length)


