import uuid

class Config:
    @classmethod
    def get_uuid(cls):
        return uuid.uuid4()
    
    @classmethod
    def get_config(cls):
        return {"configurable": {"thread_id": str(uuid.uuid4())}}