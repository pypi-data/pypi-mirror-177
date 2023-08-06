def mysql(sql, root, password, host, db):
    """
    :param sql: 输入sql语句
    :param root: 用户
    :param password: 密码
    :param host: 主机
    :param db: 数据库名称
    :return: DataFrame
    """
    from sqlalchemy import create_engine
    import pandas as pd
    from string import Template

    # 初始化引擎
    engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(root, password, host, db))
    query_sql = sql
    query_sql = Template(query_sql)  # template方法

    df = pd.read_sql_query(query_sql.substitute(), engine)  # 配合pandas的方法读取数据库值
    # 配合pandas的to_sql方法使用十分方便（dataframe对象直接入库）
    return df
