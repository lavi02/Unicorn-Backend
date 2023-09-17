from sqlalchemy import inspect, text, MetaData, Table
from dependency_injector.wiring import inject
from src.database.__init__ import container

# dependencies
from src.database.users.user import UserTable
from src.database.users.coupon import UserCoupon

from src.database.orders.order import OrderTable

from src.database.stocks.stock import StocksTable
from src.database.stocks.images import StockImages

from src.database.stores.store import StoreTable
from src.database.stores.log import StoreLogTable
from src.database.stores.tables.table import StoreTableData
from src.database.stores.tables.generated import GeneratedTable
from src.database.stores.user import StoreUserTable

from src.database.cart.cart import CartTable
from collections import deque


def topological_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = deque()
    for node, degree in in_degree.items():
        if degree == 0:
            queue.append(node)

    sorted_list = []
    while queue:
        node = queue.popleft()
        sorted_list.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_list


def build_dependency_graph(table_classes):
    table_to_class = {
        table_class.__table__: table_class for table_class in table_classes}

    graph = {}
    for table, table_class in table_to_class.items():
        graph[table_class] = []
        for column in table.columns:
            if isinstance(column.foreign_keys, set):
                for fk in column.foreign_keys:
                    ref_table = fk.column.table
                    if ref_table in table_to_class:
                        graph[table_class].append(table_to_class[ref_table])
    return graph

def compare_tables(inspector, existing_table_name, new_table):
    # 컬럼 비교
    existing_columns = {c['name']: c['type'] for c in inspector.get_columns(existing_table_name)}
    new_columns = {c.name: c.type for c in new_table.columns}
    if existing_columns != new_columns:
        return False
    
    # 기본 키 비교
    existing_pks = [c['name'] for c in inspector.get_pk_constraint(existing_table_name)['constrained_columns']]
    new_pks = [c.name for c in new_table.primary_key.columns]
    if set(existing_pks) != set(new_pks):
        return False
    
    # 외래 키 비교
    existing_fks_info = inspector.get_foreign_keys(existing_table_name)
    existing_fks = {(fk['constrained_columns'][0], fk['referred_table'], fk['referred_columns'][0]) for fk in existing_fks_info}
    new_fks = {(fk.column.name, fk.column.table.name, list(fk.column.foreign_keys)[0].column.name) for fk in new_table.columns if fk.foreign_keys}
    if existing_fks != new_fks:
        return False
    
    # 인덱스 비교
    existing_indexes_info = inspector.get_indexes(existing_table_name)
    existing_indexes = {(idx['name'], tuple(idx['column_names']), idx['unique']) for idx in existing_indexes_info}
    new_indexes = {(idx.name, tuple([col.name for col in idx.columns]), idx.unique) for idx in new_table.indexes}
    
    if existing_indexes != new_indexes:
        return False

    return True



table_classes = [
    UserTable, StoreTable, UserCoupon, OrderTable, StocksTable, StockImages,
    StoreLogTable, StoreTableData, GeneratedTable,
    StoreUserTable, CartTable
]
graph = build_dependency_graph(table_classes)
sorted_tables = topological_sort(graph)


@inject
def check_and_create_table():
    session = container.SessionLocal()()
    meta = MetaData()

    try:
        inspector = inspect(session.bind)
        existing_table_names = inspector.get_table_names()

        session.execute(text("SET foreign_key_checks = 0;"))

        for table_class in sorted_tables:
            table_name = table_class.__tablename__
            if table_name in existing_table_names:
                existing_table = Table(table_name, meta, autoload_with=session.bind)
                if not compare_tables(inspector, table_name, table_class.__table__):
                    table_class.__table__.drop(session.bind)

        session.execute(text("SET foreign_key_checks = 1;"))

        for table_class in reversed(sorted_tables):
            table_class.__table__.create(session.bind)

    except Exception as e:
        session.execute(text("SET foreign_key_checks = 1;"))
        print(e)
    finally:
        session.close()



