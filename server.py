import grpc
from concurrent import futures
import items_pb2
import items_pb2_grpc
from grpc_reflection.v1alpha import reflection
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# In-memory data store
items = [
    {"id": 1, "name": "First"},
    {"id": 2, "name": "Second"}
]

class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        # Log incoming request details
        method_name = handler_call_details.method
        metadata = dict(handler_call_details.invocation_metadata)
        
        logging.info(
            f"gRPC request received | Method: {method_name} | Metadata: {metadata}"
        )

        # Proceed with the RPC call
        try:
            return continuation(handler_call_details)
        except Exception as e:
            logging.error(f"RPC failed | Method: {method_name} | Error: {str(e)}")
            raise

def find_item_by_id(item_id):
    """Helper function to find item by ID"""
    for item in items:
        if item_id == item["id"]:
            return item
    return None

class ItemServiceServicer(items_pb2_grpc.ItemServiceServicer):
    def GetItemById(self, request, context):
        item = find_item_by_id(request.id)
        if item is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Item not found")
            return items_pb2.ItemResponse()
        return items_pb2.ItemResponse(id=item["id"], name=item["name"])

    def ListAllItems(self, request, context):
        for item in items:
            yield items_pb2.ItemResponse(id=item["id"], name=item["name"])

    def AddItems(self, request_iterator, context):
        count = 0
        for request in request_iterator:
            new_id = max(item["id"] for item in items) + 1 if items else 1
            items.append({"id": new_id, "name": request.name})
            count += 1
        return items_pb2.ItemsAddedResult(count=count)

    def ChatAboutItems(self, request_iterator, context):
        for request in request_iterator:
            yield items_pb2.ChatMessage(content=f"Server received: {request.content}")

def serve():
    # Create server with interceptor
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingInterceptor()]  # Actually pass the interceptor here
    )
    
    # Register service
    items_pb2_grpc.add_ItemServiceServicer_to_server(ItemServiceServicer(), server)
    
    # Enable reflection
    SERVICE_NAMES = (
        items_pb2.DESCRIPTOR.services_by_name['ItemService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    # Start server
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()