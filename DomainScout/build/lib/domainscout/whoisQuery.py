import socket
import whois
import datetime

def handle_value(value):
    """Handles conversion of datetime objects and ensures proper handling of emails and lists."""
    try:
        # If the value is a datetime object, convert it to ISO format string
        if isinstance(value, datetime.datetime):
            return value.isoformat()  # Convert datetime to ISO format string
        
        # If it's a list (like nameservers or emails), return the first item (if available)
        if isinstance(value, list):
            if value:
                return value[0]  # Only return the first nameserver
            return "N/A"  # Return 'N/A' if the list is empty
        
        # If it's a string and contains commas (e.g., multiple emails), split it into a list
        if isinstance(value, str) and '@' in value:  # Simple check if it's an email-like string
            return value.split(",")  # Split string into list by commas
        
        return value  # Return other values as is (no conversion)
    except Exception as e:
        return "N/A"  # Return 'N/A' in case of an error

def whoisQuery(domain):
    expectedFields = [
        "domain_name", "registrar", "whois_server", "referral_url", "updated_date", "creation_date", 
        "expiration_date", "name_servers", "status", "dnssec", "name", "org", "address", 
        "city", "state", "postal_code", "country"
    ]
    
    try:
        print(f"Fetching WHOIS info for: {domain}")
        w = whois.whois(domain)

        # Initialize the result with "N/A" for all expected fields
        result = {field: "N/A" for field in expectedFields}
        
        # If nameservers is a string (like in some cases), make it a list
        if isinstance(w.get("name_servers"), str):
            w["name_servers"] = [w["name_servers"]]  # Make sure name_servers is always a list

        # Format each field as a string and append it to the result
        formatted_result = []
        for field in expectedFields:
            value = handle_value(w.get(field, "N/A"))
            formatted_result.append(f"{field.replace('_', ' ').title()}: {value}")
        
        # Join formatted fields into a single string with newlines
        return "\n".join(formatted_result)

    except Exception as e:
        return f"Error fetching WHOIS info for {domain}: {e}"

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((host, port))
        serverSocket.listen(1)
        print(f"WHOIS micro-service listening on {host}:{port}")

        while True:
            try:
                # Accept incoming connection
                conn, addr = serverSocket.accept()

                with conn:
                    while True:
                        # Receive the data (domain name) from the client
                        data = conn.recv(1024).decode('utf-8')
                        
                        # Handle case where the client sends no data (disconnects early)
                        if not data:
                            break

                        # Query WHOIS information for the domain
                        whois_info = whoisQuery(data)

                        # Send the formatted WHOIS info as a string back to the client
                        try:
                            conn.sendall(whois_info.encode('utf-8'))
                            print(f"Sent WHOIS info to Domain Scout for {data}")
                        except BrokenPipeError:
                            print(f"Error: Broken pipe when sending data to {addr}")
                            break  # Handle the broken pipe and close the connection

            except Exception as e:
                print(f"Error with connection: {e}")
                continue

if __name__ == "__main__":
    start_server('127.0.0.1', 1025)