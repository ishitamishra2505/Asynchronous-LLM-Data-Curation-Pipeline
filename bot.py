import os
from pydoc import text

from loaders import UnifiedLoader
from models import Document
from typing import List
import json 

import json
from groq import AsyncGroq
# WARNING: In a real enterprise app, you hide this in a .env file!
# For this local MVP test, you can paste your key here.


class TrainingDataBot:
    def __init__(self):
        print("Factory Manager is waking up...")
        
        # 1. The manager hires our smart traffic controller!
        self.loader = UnifiedLoader()
        
        # 2. The manager needs a filing cabinet to remember what it has loaded
        self.documents = {}  # We will store our Document boxes here
        
        # The manager gets a direct line to Groq's LPUs
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

        print("Training Data Bot initialized successfully and ready to work!")

    async def load_documents(self, folder_path: str) -> List[Document]:
        print(f"Manager is sending the team to look at folder: {folder_path}")
        
        # The manager just tells the loader to do the heavy lifting!
        loaded_docs = await self.loader.load_directory(folder_path)
        
        # The manager files them away in the cabinet using their unique ID
        for doc in loaded_docs:
            self.documents[doc.id] = doc
            
        print(f"Successfully loaded {len(loaded_docs)} documents!")
        return loaded_docs


    def chunk_document(text, chunk_size=4000, overlap=300):
    #Slices a large document into overlapping chunks."""
        chunks = []
        start = 0
        text_length = len(text)
    
        while start < text_length:
            # Define the end of the current chunk
            end = start + chunk_size
        
        # Slice the text and add it to our list
            chunk = text[start:end]
            chunks.append(chunk)
        
        # Move the starting point forward, minus the overlap
            start += (chunk_size - overlap)
        
        return chunks
    
    # We add this superpower to process the documents we just loaded!
    
    async def process_documents(self, documents: List[Document], instruction_prompt: str):
        print("Manager is starting the AI processing line...")
        
        final_training_examples = []
        
        # Step 1: Look at every document we loaded
        for doc in documents:
            
           # Step 2: Break the huge document into perfectly sized overlapping pieces
            text_chunks = chunk_document(doc.content, chunk_size=4000, overlap=300)
            print(f"Chopped {doc.title} into {len(text_chunks)} chunks.")

           # Step 3: Loop through every single chunk for this document (THE INNER LOOP)
            for i, chunk_content in enumerate(text_chunks):
                print(f"Sending chunk {i + 1}/{len(text_chunks)} from {doc.title} to the cloud AI...")
           
            # --- THE MOCK AI WORKER ---
            # Instead of paying for a real API right now, we just pretend the AI answered!
            # This saves you money and lets you test your code instantly on your laptop.
           # ai_answer = f"Q: What is this text about? A: It is about {doc.title}."

           # --- THE REAL AI WORKER ---
            print(f"Sending text from {doc.title} to the cloud AI...")
                        
            # We glue your instructions and the extracted text together
            full_prompt = f"{instruction_prompt}\n\nTEXT TO READ:\n{chunk_content}"
            
           
            try:
                # Swapping from chat.completions to raw completions!
                response = await self.client.chat.completions.create(
                    model="qwen/qwen3.8-27b", # Try the Qwen model first
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a technical interviewer extracting questions from notes."
                        },
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ],
                    max_tokens=3000,
                    temperature=0.3
                )
                
                # The extraction path is slightly different for raw text completions
                ai_answer = response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"Oops! The AI stumbled on {doc.title}. Error: {e}")
                ai_answer = "FAILED TO GENERATE"
            
            
            # Step 4: Package the perfect result into a TrainingExample box
            example = {
                "input_text": chunk_content,
                "instruction": instruction_prompt,
                "ai_output": ai_answer
            }
            final_training_examples.append(example)
            
        print(f"Successfully created {len(final_training_examples)} perfect training examples!")
        
        return final_training_examples

    async def export_dataset(self, training_examples: list, output_path: str):
        print(f"Manager is packaging the final dataset into {output_path}...")
        
        # Here is your 'with open' magic! 'w' stands for write mode.
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in training_examples:
                # json.dumps converts our Python dictionary into a neat JSON string
                json_string = json.dumps(example)
                
                # Write it to the file, and add \n to hit 'Enter' for the next line
                f.write(json_string + "\n")
                
        print("Finished! The dataset is packed and ready.")