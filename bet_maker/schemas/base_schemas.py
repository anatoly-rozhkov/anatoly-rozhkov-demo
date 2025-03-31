from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        """
        Schema config.
        """

        from_attributes = True
