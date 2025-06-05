import asyncio

async def say_hello():
    print("👋 Привет из async!")
    await asyncio.sleep(1)
    print("✅ Всё работает!")

async def main():
    await say_hello()

if __name__ == "__main__":
    asyncio.run(main())
