from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from langchain.tools import ToolRuntime
from langchain_core.tools import ToolException, tool

from backend.app.core.dependency import get_db
from backend.app.db.models import Order, User
from backend.app.db.database import AsyncSessionLocal

@tool
def get_info():
    """get information about the company aroku"""
    return {"data":"its a software devlopment compnie, it owner is Alok he's aslo the seniour most ai agent dev, ts compnie provide servie realted to ai agents"}
@tool
async def get_order(order_id:str):
    """get info about any order by order id"""

    async with AsyncSessionLocal() as db:
        result= await db.execute(
            select(Order).options(
                selectinload(Order.user)
                )
            .where(
                Order.order_id==order_id
            )
        )

    order = result.scalar_one_or_none()

    if order is None:
        return "no order found"

    return {
        "order_id": order.id,
        "ordered_by":order.user.username,
        "product":order.product,
        "order_at": order.ordered_at
    }

@tool
def cancel_order(order_id:str):
    """cancel any order by order id"""

    return f"order cancled for {order_id}, an email has been send for more details"

@tool
def check_payment(order_id:str):
    """check payment status of an order"""

    if order_id=="ORD-FAILED":
        raise ToolException("payment service is cruntly unavliable")

    return f"payment for {order_id}is successfull"

check_payment.handle_tool_error = True

@tool
async def get_user(runtime: ToolRuntime):
    """get info about current authenticated user"""

    user_id = runtime.context.user_id

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.id == user_id)  
        )
        user = result.scalar_one_or_none()

    if user is None:
        raise ToolException("No information about user")

    return {
        "username": user.username,
        "bio": user.bio,
    }

get_user.handle_tool_error = True

@tool
def save_memory(runtime:ToolRuntime, key:str, value:str):
    """save important fact and memory about current user to long-term memory"""

    user_id = runtime.context.user_id

    namespace = ("user", str(user_id))

    runtime.store.put(
        namespace,
        key,
        {
            "text":value
        }
    )

    return "Memory saved sucessfully"

@tool
def get_memory(runtime: ToolRuntime, key:str):
    """ Retrieve a specific memory the current user. """

    user_id = runtime.context.user_id

    namespace = ("user", str(user_id))

    memory= runtime.store.get(
        namespace, key
    )

    if memory is None:
        return "No memory found"

    return memory.value["text"]

