from typing import Dict, Any, Optional, List
from .postgresql import Database
from datetime import datetime



class UserDatabase(Database):
    async def create_table_users(self):

        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            username VARCHAR(255) NULL,
            last_active TIMESTAMP NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        await self.execute(sql, commit=True)

    async def add_user(self, telegram_id: int, username: Optional[str], created_at: Optional[datetime] = None):
        sql = """
        INSERT INTO Users (telegram_id, username, created_at) 
        VALUES ($1, $2, $3) 
        RETURNING *
        """
        if created_at is None:
            created_at = datetime.now()
        return await self.execute(sql, parameters=(telegram_id, username, created_at), fetchone=True)

    async def select_all_users(self) -> List[Dict[str, Any]]:
        sql = """
        SELECT * FROM Users
        """
        return await self.execute(sql, fetchall=True)

    async def select_user(self, **kwargs) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters=parameters, fetchone=True)

    async def count_users(self) -> int:
        sql = "SELECT COUNT(*) FROM Users"
        result = await self.execute(sql, fetchone=True)
        return result["count"]

    async def delete_users(self):
        sql = "DELETE FROM Users WHERE TRUE"
        await self.execute(sql, commit=True)
