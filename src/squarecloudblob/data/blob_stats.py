class Stats(object):
    """A Stats object that represents the statistics of your account related with the Square Cloud Blob storage."""
    __slots__ = ("objects", "storage_used", "storage_included",
                 "extra_storage_used", "extra_storage_price",
                 "extra_objects_price", "billing_price")
    
    def __init__(self, usage: dict[str, int], plan: dict[str, int], billing: dict[str, int]) -> None:
        self.objects: int = usage["objects"]
        self.storage_used: int = usage["storage"]
        self.storage_included: int = plan["included"]
        self.extra_storage_used: int = billing["extraStorage"]
        self.extra_storage_price: int = billing["storagePrice"]
        self.extra_objects_price: int = billing["objectsPrice"]
        self.billing_price: int = billing["totalEstimate"]
    
    