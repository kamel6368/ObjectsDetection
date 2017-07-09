import unittest
from Common.TCPConnections import TCPServer, TCPClient


class MyTCPServer(TCPServer):
    def handle_message(self, command, content):
        pass


class TCPClientTest(unittest.TestCase):

    def setUp(self):
        self.tcp_client = TCPClient('xxx', 123)

    def test__prepare_message_should_return_as_expected(self):
        command = 'COMMAND'
        content = 'ala ma kota'

        data = self.tcp_client._prepare_message(command, content)
        self.assertEqual('22|COMMAND|ala ma kota', data)
        self.assertEqual(22, len(data))
        self.assertEqual(22, int(data.split('|')[0]))


class TCPServerTest(unittest.TestCase):

    def setUp(self):
        address = '127.0.0.1'
        port = 1234
        buffer_size = 1024
        self.tcp_server = MyTCPServer(address, port, buffer_size)

    def test__manage_chunk_read_simple_message(self):
        data = None
        msg_length = None
        chunk = '14|ala ma kota'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_simple_message_with_buffer_number(self):
        data = None
        msg_length = None
        chunk = '|ala ma kota'
        self.tcp_server.buffer = '14'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_simple_message_with_buffer_number_and_delimeter(self):
        data = None
        msg_length = None
        chunk = 'ala ma kota'
        self.tcp_server.buffer = '14|'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_simple_message_with_buffer_number_and_delimeter_and_part_message(self):
        data = None
        msg_length = None
        chunk = 'a ma kota'
        self.tcp_server.buffer = '14|al'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_second_part_of_message(self):
        data = '14|ala m'
        msg_length = 14
        chunk = 'a kota'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_second_part_of_message_with_buffer(self):
        data = 'a m'
        msg_length = None
        chunk = 'a kota'
        self.tcp_server.buffer = '14|al'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala ma kota', data)
        self.assertIsNone(msg_length)
        self.assertTrue(is_complete_message)

    def test__manage_chunk_read_incomplete_message(self):
        data = None
        msg_length = None
        chunk = '14|ala m'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala m', data)
        self.assertEqual(14, msg_length)
        self.assertFalse(is_complete_message)

    def test__manage_chunk_read_incomplete_message_with_data(self):
        data = '14'
        msg_length = 14
        chunk = '|ala m'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala m', data)
        self.assertEqual(14, msg_length)
        self.assertFalse(is_complete_message)

    def test__manage_chunk_read_incomplete_message_with_buffer(self):
        data = None
        msg_length = None
        chunk = 'ala m'
        self.tcp_server.buffer = '14|'
        data, msg_length, is_complete_message = self.tcp_server._manage_chunk(chunk, data, msg_length)

        self.assertEqual('14|ala m', data)
        self.assertEqual(14, msg_length)
        self.assertFalse(is_complete_message)

