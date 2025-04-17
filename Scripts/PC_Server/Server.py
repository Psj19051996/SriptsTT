import socket
import datetime
import signal
import sys
import time
import re
import threading
import os

# Directory to store log files
LOG_DIR = r"C:\Users\PrasoonJose\OneDrive - Tribe Technology\LogFiles"

# Ensure logging directory exists
if not os.path.exists(LOG_DIR):
    print(f"Creating log directory: {LOG_DIR}")
    os.makedirs(LOG_DIR, exist_ok=True)

# Server config
HOST = "10.254.251.20"
PORT = 5001

# Create and configure socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}...")

# Global flags
running = True
data_lock = threading.Lock()

# Graceful shutdown handler
def shutdown_server(signal, frame):
    global running
    print("\nShutting down server...")
    running = False
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_server)

def log_raw_plc_message(function_name, raw_data):
    """Logs PLC messages with metadata headers including milliseconds."""
    now = datetime.datetime.now()
    log_file_path = os.path.join(LOG_DIR, f"{function_name}.txt")
    file_exists = os.path.exists(log_file_path)

    # Format timestamp with milliseconds
    date_str = now.strftime("%d-%m-%Y")
    timestamp_str = now.strftime("%H:%M:%S") + f".{now.microsecond // 1000:03d}"

    # Parse data pairs
    data_pairs = [pair.strip() for pair in raw_data.split(",") if "=" in pair]
    headers = [pair.split("=")[0].strip() for pair in data_pairs]
    values = [pair.split("=")[1].strip() for pair in data_pairs]

    print(f"[LOG] Logging data for function: {function_name}")
    print(f"[LOG] Log file path: {log_file_path}")
    print(f"[LOG] Headers: {headers}")
    print(f"[LOG] Values: {values}")

    try:
        with data_lock:
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                if not file_exists:
                    log_file.write("Metadata, Raw Data Fields\n")
                    log_file.write("Date, Timestamp, " + ", ".join(headers) + "\n")

                log_file.write(f"{date_str}, {timestamp_str}, " + ", ".join(values) + "\n")
                print(f"[LOG] Successfully logged data to {log_file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write log file: {e}")

def extract_function_and_data(data):
    """Extracts function name and values from the received string."""
    print(f"[DEBUG] Extracting function and data from: {data}")
    function_data_list = []
    messages = [msg.strip() for msg in data.split(";") if msg.strip()]

    for message in messages:
        print(f"[DEBUG] Inspecting message: '{message}'")
        match = re.match(r"^([\w\d_]+):(.+)$", message)
        if match:
            function_name = match.group(1).strip()
            raw_data = match.group(2).strip()
            print(f"[DEBUG] Extracted function: {function_name}, Data: {raw_data}")
            function_data_list.append((function_name, raw_data))
        else:
            print(f"[WARNING] Invalid format detected: {message}")
    
    return function_data_list

def receive_from_plc(client_socket):
    """Receives and logs data from PLC."""
    buffer = ""  # Store incomplete messages
    while running:
        try:
            raw_data = client_socket.recv(1024)
            if not raw_data:
                print("[WARNING] Received empty message, ignoring...")
                break

            print(f"[DEBUG] Received raw bytes: {raw_data}")
            try:
                chunk = raw_data.decode("utf-8", errors="replace")
            except UnicodeDecodeError:
                chunk = raw_data.decode("latin-1")

            buffer += chunk
            print(f"[DEBUG] Updated buffer: {buffer}")

            # Split complete messages by delimiter
            while ";" in buffer:
                msg, buffer = buffer.split(";", 1)
                msg = msg.strip()
                if not msg:
                    continue

                print(f"[DEBUG] Processing message: {msg}")
                function_data_list = extract_function_and_data(msg + ";")  # Add back delimiter for parser
                for function_name, raw_data in function_data_list:
                    log_raw_plc_message(function_name, raw_data)

        except (socket.timeout, ConnectionResetError, BrokenPipeError):
            print("[ERROR] Client disconnected or timed out.")
            break
        except Exception as e:
            print(f"[ERROR] Exception in receive thread: {e}")
            break


def send_to_plc(client_socket):
    """Sends time updates to PLC."""
    while running:
        try:
            current_time = datetime.datetime.now()
            time_string = current_time.strftime("%d-%m-%Y %H:%M:%S")
            client_socket.sendall(time_string.encode("utf-8"))
            print(f"[DEBUG] Sent time to PLC: {time_string}")
            time.sleep(0.5)
        except (BrokenPipeError, ConnectionResetError):
            print("[ERROR] Client disconnected while sending.")
            break
        except Exception as e:
            print(f"[ERROR] Exception in send thread: {e}")
            break

# Accepting loop
while running:
    try:
        client_socket, client_address = server_socket.accept()
        print(f"[INFO] Connection established with {client_address}")

        receive_thread = threading.Thread(target=receive_from_plc, args=(client_socket,))
        send_thread = threading.Thread(target=send_to_plc, args=(client_socket,))
        
        receive_thread.start()
        send_thread.start()
        
        receive_thread.join()
        send_thread.join()

        client_socket.close()
    except socket.timeout:
        print("[WARNING] Socket accept timeout, retrying...")
    except Exception as e:
        print(f"[ERROR] Error accepting connection: {e}")
