from fastapi import HTTPException, status

class AddressNotFoundException(HTTPException):
    def __init__(self, address):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address {address} not found on-chain"
        )
