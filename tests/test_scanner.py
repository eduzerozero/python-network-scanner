import socket
from unittest.mock import patch

from scanner import scan_port

import json
from scanner import save_results


def test_save_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    results = [
        {"port": 80, "status": "OPEN", "duration": 0.015},
        {"port": 81, "status": "CLOSED", "duration": 2.042},
    ]

    save_results("127.0.0.1", 80, 81, 3.0, 2.05, results)

    file_path = tmp_path / "scan_results.json"

    assert file_path.exists()

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["host"] == "127.0.0.1"
    assert data["start_port"] == 80
    assert data["end_port"] == 81
    assert data["timeout"] == 3.0
    assert data["scan_duration"] == 2.05
    assert data["results"] == results


def test_scan_port_timeout():
    with patch("scanner.socket.socket") as mock_socket:

        mock_sock = mock_socket.return_value.__enter__.return_value

        mock_sock.connect.side_effect = socket.timeout()

        result = scan_port("127.0.0.1", 8081, 1)

        assert result["port"] == 8081
        assert result["status"] == "TIMEOUT"
        assert result["duration"] >= 0


def test_scan_port_closed():
    with patch("scanner.socket.socket") as mock_socket:

        mock_sock = mock_socket.return_value.__enter__.return_value

        mock_sock.connect.side_effect = ConnectionRefusedError()

        result = scan_port("127.0.0.1", 8081, 3)

        assert result["port"] == 8081
        assert result["status"] == "CLOSED"
        assert result["duration"] >= 0


def test_scan_port_open():
    with patch("scanner.socket.socket") as mock_socket:
        result = scan_port("127.0.0.1", 8080, 1)

        assert result["port"] == 8080
        assert result["status"] == "OPEN"
        assert result["duration"] >= 0

        mock_socket.return_value.__enter__.return_value.connect.assert_called_once_with(
            ("127.0.0.1", 8080)
        )


def test_port_range():
    start_port = 80
    end_port = 85

    ports = list(range(start_port, end_port + 1))

    assert ports == [80, 81, 82, 83, 84, 85]
