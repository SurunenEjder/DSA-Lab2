import grpc
import items_pb2
import items_pb2_grpc
import time

def run():

    channel = grpc.insecure_channel("localhost:50051")
    stub = items_pb2_grpc.ItemServiceStub(channel)

    # 1. Unary call
    response = stub.GetItemById(items_pb2.ItemRequest(id=1))
    print("Unary response:", response)

    # 2. Server-streaming
    for item in stub.ListAllItems(items_pb2.Empty()):
        print("Server-streaming item:", item)

    # 3. Client-streaming
    # Create an iterator of ItemRequest messages

    print("\n--- Client Streaming ---")
    def generate_requests():
        names = ["Third", "Fourth", "Fifth"]
        for name in names:
            yield items_pb2.ItemRequest(name=name)
            print(f"Sent item: {name}")

    response = stub.AddItems(generate_requests())
    print(f"Server added {response.count} items")

    
    # 4. Bidirectional
    # Then call stub.AddItems(...) and capture the final result
    # Open a stub.ChatAboutItems() stream
    # Send ChatMessage objects and read responses in a loop
    print("\n--- Bidirectional Streaming ---")
    def generate_messages():
        messages = [
            "Hello server",
            "Can you hear me?",
            "Sending final message"
        ]
        for msg in messages:
            yield items_pb2.ChatMessage(content=msg)
            print(f"Client: {msg}")

    chat_stream = stub.ChatAboutItems(generate_messages())
    for response in chat_stream:
        print(f"Server replied: {response.content}")


# Configuration for calculating time
# TOTAL_REQUESTS = 100
# GRPC_SERVER = "localhost:50051"

# def run_grpc_test():
#     channel = grpc.insecure_channel(GRPC_SERVER)
#     stub = items_pb2_grpc.ItemServiceStub(channel)
    
#     print("Testing gRPC with Python client...")
#     start_time = time.time()
   
#     for i in range(TOTAL_REQUESTS):
#         response = stub.GetItemById(items_pb2.ItemRequest(id=1))
#         print(".", end="", flush=True)  # Progress indicator
   
#     total_time = time.time() - start_time
#     avg_time = total_time / TOTAL_REQUESTS
   
#     print(f"\n\ngRPC Results:")
#     print(f"Total time for {TOTAL_REQUESTS} calls: {total_time:.6f} seconds")
    # print(f"Average time per call: {avg_time:.6f} seconds")


if __name__ == "__main__":
    run()