import aiosqlite


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self, db_path: str = 'db.sqlite3') -> None:
        """
        Ma'lumotlar bazasiga ulanishni o'rnatadi.
        """
        self.pool = await aiosqlite.connect(db_path)
        await self.pool.execute('PRAGMA foreign_keys = ON;')  # Chet el kalitlarini yoqish
        await self.pool.commit()

    async def close(self) -> None:
        """
        Ma'lumotlar bazasi ulanishini yopadi.
        """
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args) -> None:
        """
        SQL buyruqni bajaradi (INSERT, UPDATE, DELETE).
        """
        async with self.pool.cursor() as cursor:
            await cursor.execute(query, args)
            await self.pool.commit()

    async def fetchone(self, query: str, *args) -> tuple:
        """
        SQL so'rovidan bitta natijani qaytaradi.
        """
        async with self.pool.cursor() as cursor:
            await cursor.execute(query, args)
            return await cursor.fetchone()

    async def add_certificate(self, fullname: str, course: str, image: str = None) -> int:
        """
        SQL yordamida ma'lumotlar jadvaliga yangi sertifikat qo'shadi va uning ID'sini qaytaradi.

        Args:
            fullname (str): Foydalanuvchining to'liq ismi.
            course (str): Kurs nomi (frontend, backend, yoki web_design).
            image (str): Sertifikat rasmi yo'li (null bo'lishi mumkin).

        Returns:
            int: Qo'shilgan sertifikatning ID'si.
        """
        query = """
        INSERT INTO certificates (fullname, course, image, created_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        RETURNING id;
        """
        async with self.pool.execute(query, (fullname, course, image)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

    async def update_cert_image(self, cert_id: int, image: str) -> None:
        query = """
            UPDATE certificates
            SET image = ?
            WHERE id = ?;
        """
        await self.execute(query, image, cert_id)
