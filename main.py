import asyncio
from bot import TrainingDataBot

async def main():
    print("--- Starting the AI Data Factory ---")
    
    # 1. Turn on the Factory Manager
    bot = TrainingDataBot()
    
    # 2. Point it at a folder
    # (Create a folder named 'test_docs' in your project and put a .txt file in it!)
    docs = await bot.load_documents("test_docs")
    
    if not docs:
        print("Oops! Put some text or PDF files in the 'test_docs' folder first.")
        return

    # 3. Process the documents with your custom prompt
    prompt = "Go through the text chunk carefully and draft 10 most important questions along with their answers."
    examples = await bot.process_documents(docs, prompt)
    
    # 4. Save the final JSONL dataset
    await bot.export_dataset(examples, "my_dataset.jsonl")
    
    print("--- Factory Shutdown ---")

# This is Python's standard way of saying "run this script"
if __name__ == "__main__":
    asyncio.run(main())