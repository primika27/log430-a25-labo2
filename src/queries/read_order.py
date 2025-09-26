"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()
    order_keys = r.keys("order:*")
    main_order_keys = [key for key in order_keys if ":item:" not in key]
    main_order_keys = main_order_keys[:limit]
    orders = []
    for key in main_order_keys:
        order_data = r.hgetall(key)
        orders.append(order_data)
    return orders

def get_highest_spending_users():
    """Get highest spending users from Redis"""
    r = get_redis_conn()
    order_keys = r.keys("order:*")
    main_order_keys = [key for key in order_keys if ":item:" not in key]
    user_spending = {}
    for key in main_order_keys:
        order = r.hgetall(key)
        user_id = order.get("user_id")
        total = float(order.get("total_amount", 0))
        user_spending[user_id] = user_spending.get(user_id, 0) + total
    sorted_users = sorted(user_spending.items(), key=lambda x: x[1], reverse=True)
    return sorted_users