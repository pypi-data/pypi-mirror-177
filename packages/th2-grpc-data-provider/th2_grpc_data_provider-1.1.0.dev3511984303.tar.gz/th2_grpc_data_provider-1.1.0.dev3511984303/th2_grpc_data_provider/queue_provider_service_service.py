from . import queue_data_provider_pb2_grpc as importStub

class QueueProviderServiceService(object):

    def __init__(self, router):
        self.connector = router.get_connection(QueueProviderServiceService, importStub.QueueProviderServiceStub)

    def SearchMessageGroups(self, request, timeout=None):
        return self.connector.create_request('SearchMessageGroups', request, timeout)