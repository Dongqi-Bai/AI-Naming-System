from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker



from backend.settings import DB_URI

# 创建异步数据库连接引擎
engine = create_async_engine(
    DB_URI,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)

# 创建异步会话工厂
AsyncSessionFactory = sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=True, expire_on_commit=False
)


# 定义base类
class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            # ix: index，索引。
            "ix": "ix_%(column_0_label)s",
            # un: unique，唯一约束
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            # ck: Check，检查约束
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            # fk: Foreign Key，外键约束
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            # pk: Primary Key，主键约束
            "pk": "pk_%(table_name)s",
        }
    )
    
from . import user
