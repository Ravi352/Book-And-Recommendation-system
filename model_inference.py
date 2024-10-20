import asyncio
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from functools import lru_cache
import time

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('model_inference.log'),
                        logging.StreamHandler()
                    ])

# Create a logger
logger = logging.getLogger(__name__)


# Define the template for the prompt
template1 = """Summary: {Summary}
Answer: Please take all the reviews into consideration, please give the overall summary about the book and summerize it in minimum words. """

# Create the prompt and initialize the model
prompt1 = ChatPromptTemplate.from_template(template1)
model = OllamaLLM(model="llama3.1")  # Consider switching to a smaller model if needed


# Caching function to store results of previous calls
@lru_cache(maxsize=128)
def get_summary(summary):
    start_time = time.time()  # Start timer
    logger.info("Invoking model for summary and review...")
    
    # Prepare the input for the model
    input_text = prompt1.format(Summary=summary)
    output = model.invoke(input_text)  # Call the model with the formatted string
    
    end_time = time.time()  # End timer
    logger.info(f"Time taken for model inference: {end_time - start_time:.4f} seconds")
    
    return output



template2 = """Summary: {Summary}
Answer: please give the overall summary about the book and summerize it in minimum words. please consider time taken should be minimum"""
prompt2 = ChatPromptTemplate.from_template(template2)

@lru_cache(maxsize=128)
def generate_summary(summary):
    start_time = time.time()  # Start timer
    logger.info("Invoking model for summary and review...")
    
    # Prepare the input for the model
    input_text = prompt2.format(Summary=summary)
    output = model.invoke(input_text)  # Call the model with the formatted string
    
    end_time = time.time()  # End timer
    logger.info(f"Time taken for model inference: {end_time - start_time:.4f} seconds")
    
    return output


template3 = """Summary: {Summary}
Answer: please give the top 3 good book recommendation considering the genres and give books name not too much details. please consider time taken should be minimum"""
prompt3 = ChatPromptTemplate.from_template(template3)


@lru_cache(maxsize=128)
def generate_recommendation(summary):
    start_time = time.time()  # Start timer
    logger.info("Invoking model for summary and review...")
    
    # Prepare the input for the model
    input_text = prompt3.format(Summary=summary,)
    output = model.invoke(input_text)  # Call the model with the formatted string
    
    end_time = time.time()  # End timer
    logger.info(f"Time taken for model inference: {end_time - start_time:.4f} seconds")
    
    return output

