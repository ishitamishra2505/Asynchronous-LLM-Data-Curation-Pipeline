AI Training Data Generator 🏭

An asynchronous, object-oriented Python pipeline designed to parse technical notes and automatically generate highly structured JSONL training datasets using Groq's high-speed LPU inference.

🚀 Features
Asynchronous Processing: Built with AsyncGroq and asyncio to prevent I/O blocking during API requests.

Sliding Window Chunking: Intelligently slices large documents (like Markdown DSA notes) into 4,000-character chunks with a 300-character overlap, preserving technical context across LLM prompts.

Frontier Open-Source Models: Configured to leverage qwen/qwen3.8-27b for extracting complex algorithmic concepts and generating technical interview questions.

Secure by Design: API credentials are fully decoupled from the codebase using python-dotenv.

JSONL Output: Extracts and serializes AI responses line-by-line, perfectly formatting the output for fine-tuning custom machine learning models.

🛠️ Architecture
main.py: The execution entry point that initializes and runs the pipeline.

bot.py: Contains TrainingDataBot, the core worker managing state, sliding window iteration, and async API communication.

loaders.py: Contains UnifiedLoader to ingest local files and prep them for processing.

models.py: Data structures ensuring strict type-hinting and pipeline reliability.

⚙️ Quick Start
1. Clone the repository

git clone https://github.com/ishitamishra2505/Training-Datasets-generator.git
cd Training-Datasets-generator

2. Set up the environment

python -m venv venv
venv\Scripts\activate
pip install groq python-dotenv pydantic

3. Secure your API Key
Create a .env file in the root directory and add your Groq API key:

Plaintext
GROQ_API_KEY=gsk_your_api_key_here

4. Run the Pipeline
Place your target notes in your input directory and fire up the factory manager:

python main.py
Generated training examples will be automatically appended to my_dataset.jsonl.