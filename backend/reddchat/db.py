import sqlite3
from pathlib import Path

import click
from flask import current_app, g


def get_db() -> sqlite3.Connection:
    """获取请求级数据库连接"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_PATH'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """从 SQL 文件初始化数据库"""
    db_path = current_app.config['DATABASE_PATH']

    # 确保目录存在
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # 读取 SQL 文件
    with current_app.open_resource('db/schema.sql') as f:
        sql_script = f.read().decode('utf-8')

    # 执行 SQL
    with get_db() as conn:  # 使用请求级连接
        conn.executescript(sql_script)


@click.command('init-db')
def init_db_command():
    """清空数据库并初始化"""
    init_db()
    click.echo('数据库已初始化。')


@click.command('db')
def db_command():
    """显示数据库路径"""
    click.echo(current_app.config['DATABASE_PATH'])


@click.command('clear-db')
def clear_db_command():
    """清空数据库"""
    with get_db() as conn:
        conn.execute('DELETE FROM user;')
        conn.execute('DELETE FROM message;')
        conn.execute('DELETE FROM conversation;')
    click.echo('数据库已清空。')
