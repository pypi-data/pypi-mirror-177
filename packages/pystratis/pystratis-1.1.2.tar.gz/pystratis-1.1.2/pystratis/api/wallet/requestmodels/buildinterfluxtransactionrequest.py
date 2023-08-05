from typing import Optional, List
from pydantic import Field, SecretStr, validator
from pystratis.core import DestinationChain, Outpoint, Recipient
from pystratis.api import Model
from pystratis.core.types import Address, Money


# noinspection PyUnresolvedReferences
class BuildInterfluxTransactionRequest(Model):
    """A request model for the wallet/build-interflux-transaction endpoint.

    Args:
        destination_chain (int): Enumeration representing the destination chain.
        destination_address (Address): The destination address.
        fee_amount (Money, optional): The fee amount. Cannot be set with fee_type.
        password (str): The password.
        segwit_change_address (bool, optional): If True, the change address is a segwit address.
        wallet_name (str): The wallet name.
        account_name (str, optional): The account name. Default='account 0'.
        outpoints (List[Outpoint]): A list of outpoints to include in the transaction.
        recipients (List[Recipient]): A list of recipients with amounts.
        op_return_data (str, optional): The OP_RETURN data.
        op_return_amount (Money, optional): The amount to burn in OP_RETURN.
        fee_type (str, optional): The fee type. Allowed [low, medium, high]
        allow_unconfirmed (bool, optional): If True, includes unconfirmed outputs. Default=False.
        shuffle_outputs (bool, optional): If True, shuffle outputs. Default=False.
        change_address (Address, optional): Specify a change address. If not set, a new change address is used.
    """
    destination_chain: DestinationChain = Field(alias='destinationChain')
    destination_address: Address = Field(alias='destinationAddress')
    fee_amount: Optional[Money] = Field(alias='feeAmount')
    password: SecretStr
    segwit_change_address: Optional[bool] = Field(default=False, alias='segwitChangeAddress')
    wallet_name: str = Field(alias='walletName')
    account_name: Optional[str] = Field(default='account 0', alias='accountName')
    outpoints: List[Outpoint]
    recipients: List[Recipient]
    op_return_data: Optional[str] = Field(alias='opReturnData')
    op_return_amount: Optional[Money] = Field(alias='opReturnAmount')
    fee_type: Optional[str] = Field(alias='feeType')
    allow_unconfirmed: Optional[bool] = Field(default=False, alias='allowUnconfirmed')
    shuffle_outputs: Optional[bool] = Field(default=False, alias='shuffleOutputs')
    change_address: Optional[Address] = Field(alias='changeAddress')

    # noinspection PyMethodParameters,PyUnusedLocal
    @validator('fee_type')
    def validate_fee_type(cls, v, values):
        allowed = [
            'low',
            'medium',
            'high'
        ]
        if v is not None and v not in allowed:
            raise ValueError(f'Invalid command. Must be: {allowed}')
        if v is not None and values['fee_amount'] is not None:
            raise ValueError('Both fee_type and fee_amount cannot be set.')
        return v

    # noinspection PyMethodParameters,PyUnusedLocal
    @validator('fee_amount', always=True)
    def check_fee_too_high(cls, v, values):
        if v is not None:
            if v > Money(1):
                raise ValueError('Fee should not be more than 1. Check parameters.')
        return v
