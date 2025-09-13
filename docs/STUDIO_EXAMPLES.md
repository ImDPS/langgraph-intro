# LangGraph Studio: Practical Examples

## Table of Contents
1. [Simple Chatbot](#simple-chatbot)
2. [Document Q&A System](#document-qa-system)
3. [Multi-Agent Workflow](#multi-agent-workflow)
4. [Conditional Routing](#conditional-routing)
5. [Memory-Enhanced Agent](#memory-enhanced-agent)
6. [Error Handling Patterns](#error-handling-patterns)
7. [Performance Optimization](#performance-optimization)

## Simple Chatbot

### Basic Chatbot Implementation

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
import google.generativeai as genai

class ChatState(TypedDict):
    user_message: str
    bot_response: str
    conversation_history: list[dict]

def initialize_chat(state: ChatState) -> ChatState:
    """Initialize chat with system message"""
    if "conversation_history" not in state:
        state["conversation_history"] = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
    return state

def generate_response(state: ChatState) -> ChatState:
    """Generate response using Gemini"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    # Add user message to history
    state["conversation_history"].append({
        "role": "user", 
        "content": state["user_message"]
    })
    
    # Generate response
    response = model.generate_content(state["user_message"])
    
    # Add bot response to history
    state["conversation_history"].append({
        "role": "assistant", 
        "content": response.text
    })
    
    return {
        **state,
        "bot_response": response.text
    }

def create_chatbot():
    """Create the chatbot graph"""
    graph = StateGraph(ChatState)
    
    # Add nodes
    graph.add_node("initialize", initialize_chat)
    graph.add_node("generate", generate_response)
    
    # Add edges
    graph.add_edge("initialize", "generate")
    
    # Set entry and finish points
    graph.set_entry_point("initialize")
    graph.set_finish_point("generate")
    
    return graph.compile()
```

### Studio Configuration

```json
{
  "dependencies": ["."],
  "graphs": {
    "chatbot": "./src/chatbot.py:create_chatbot"
  },
  "env": ".env"
}
```

### Testing in Studio

```python
# Test inputs for Studio
test_cases = [
    {"user_message": "Hello, how are you?"},
    {"user_message": "What's the weather like?"},
    {"user_message": "Can you help me with Python?"},
    {"user_message": "Tell me a joke"}
]
```

## Document Q&A System

### Advanced Document Processing

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
import google.generativeai as genai

class DocumentState(TypedDict):
    document_text: str
    user_question: str
    relevant_chunks: list[str]
    answer: str
    confidence: float
    sources: list[str]

def load_document(state: DocumentState) -> DocumentState:
    """Load and preprocess document"""
    # In a real implementation, this would load from file/database
    document = state.get("document_text", "")
    
    # Split into chunks (simplified)
    chunks = [document[i:i+500] for i in range(0, len(document), 500)]
    
    return {
        **state,
        "document_chunks": chunks
    }

def retrieve_relevant_chunks(state: DocumentState) -> DocumentState:
    """Retrieve chunks relevant to the question"""
    question = state["user_question"]
    chunks = state["document_chunks"]
    
    # Simple keyword matching (in production, use embeddings)
    relevant_chunks = []
    for chunk in chunks:
        if any(word in chunk.lower() for word in question.lower().split()):
            relevant_chunks.append(chunk)
    
    return {
        **state,
        "relevant_chunks": relevant_chunks[:3]  # Top 3 chunks
    }

def generate_answer(state: DocumentState) -> DocumentState:
    """Generate answer based on relevant chunks"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    context = "\n\n".join(state["relevant_chunks"])
    question = state["user_question"]
    
    prompt = f"""
    Based on the following context, answer the question.
    
    Context:
    {context}
    
    Question: {question}
    
    Provide a clear, accurate answer based only on the context provided.
    """
    
    response = model.generate_content(prompt)
    
    return {
        **state,
        "answer": response.text,
        "confidence": 0.8,  # Simplified confidence score
        "sources": [f"Chunk {i+1}" for i in range(len(state["relevant_chunks"]))]
    }

def create_document_qa():
    """Create document Q&A system"""
    graph = StateGraph(DocumentState)
    
    # Add nodes
    graph.add_node("load_document", load_document)
    graph.add_node("retrieve_chunks", retrieve_relevant_chunks)
    graph.add_node("generate_answer", generate_answer)
    
    # Add edges
    graph.add_edge("load_document", "retrieve_chunks")
    graph.add_edge("retrieve_chunks", "generate_answer")
    
    # Set entry and finish points
    graph.set_entry_point("load_document")
    graph.set_finish_point("generate_answer")
    
    return graph.compile()
```

## Multi-Agent Workflow

### Research Assistant with Multiple Agents

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
import google.generativeai as genai

class ResearchState(TypedDict):
    research_topic: str
    search_results: list[dict]
    analysis: str
    summary: str
    recommendations: list[str]
    current_agent: str

def research_agent(state: ResearchState) -> ResearchState:
    """Agent responsible for gathering information"""
    topic = state["research_topic"]
    
    # Simulate research (in production, use real search APIs)
    search_results = [
        {"title": f"Research on {topic}", "content": f"Detailed analysis of {topic}"},
        {"title": f"Latest trends in {topic}", "content": f"Current trends and developments in {topic}"},
        {"title": f"Best practices for {topic}", "content": f"Recommended practices for {topic}"}
    ]
    
    return {
        **state,
        "search_results": search_results,
        "current_agent": "research_agent"
    }

def analysis_agent(state: ResearchState) -> ResearchState:
    """Agent responsible for analyzing information"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    results = state["search_results"]
    topic = state["research_topic"]
    
    # Create analysis prompt
    content = "\n\n".join([f"{r['title']}: {r['content']}" for r in results])
    
    prompt = f"""
    Analyze the following research findings about {topic}:
    
    {content}
    
    Provide a comprehensive analysis including:
    1. Key findings
    2. Trends and patterns
    3. Potential implications
    """
    
    response = model.generate_content(prompt)
    
    return {
        **state,
        "analysis": response.text,
        "current_agent": "analysis_agent"
    }

def summary_agent(state: ResearchState) -> ResearchState:
    """Agent responsible for creating summaries"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    analysis = state["analysis"]
    topic = state["research_topic"]
    
    prompt = f"""
    Create a concise summary of the research on {topic}:
    
    Analysis: {analysis}
    
    Provide:
    1. Executive summary (2-3 sentences)
    2. Key recommendations (3-5 bullet points)
    """
    
    response = model.generate_content(prompt)
    
    # Extract recommendations (simplified)
    recommendations = [
        f"Recommendation 1 for {topic}",
        f"Recommendation 2 for {topic}",
        f"Recommendation 3 for {topic}"
    ]
    
    return {
        **state,
        "summary": response.text,
        "recommendations": recommendations,
        "current_agent": "summary_agent"
    }

def create_research_assistant():
    """Create multi-agent research assistant"""
    graph = StateGraph(ResearchState)
    
    # Add nodes
    graph.add_node("research_agent", research_agent)
    graph.add_node("analysis_agent", analysis_agent)
    graph.add_node("summary_agent", summary_agent)
    
    # Add edges
    graph.add_edge("research_agent", "analysis_agent")
    graph.add_edge("analysis_agent", "summary_agent")
    
    # Set entry and finish points
    graph.set_entry_point("research_agent")
    graph.set_finish_point("summary_agent")
    
    return graph.compile()
```

## Conditional Routing

### Smart Customer Service Router

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
import google.generativeai as genai

class CustomerServiceState(TypedDict):
    customer_message: str
    intent: str
    priority: str
    department: str
    response: str
    escalation_needed: bool

def classify_intent(state: CustomerServiceState) -> CustomerServiceState:
    """Classify customer intent"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    message = state["customer_message"]
    
    prompt = f"""
    Classify the following customer message into one of these categories:
    - billing: Questions about payments, invoices, charges
    - technical: Technical issues, bugs, feature requests
    - general: General questions, information requests
    - complaint: Complaints, dissatisfaction
    - sales: Sales inquiries, pricing questions
    
    Message: {message}
    
    Respond with only the category name.
    """
    
    response = model.generate_content(prompt)
    intent = response.text.strip().lower()
    
    return {
        **state,
        "intent": intent
    }

def determine_priority(state: CustomerServiceState) -> CustomerServiceState:
    """Determine priority level"""
    intent = state["intent"]
    
    priority_map = {
        "complaint": "high",
        "technical": "medium",
        "billing": "medium",
        "sales": "low",
        "general": "low"
    }
    
    return {
        **state,
        "priority": priority_map.get(intent, "low")
    }

def route_to_department(state: CustomerServiceState) -> CustomerServiceState:
    """Route to appropriate department"""
    intent = state["intent"]
    
    department_map = {
        "billing": "billing_department",
        "technical": "technical_support",
        "general": "general_support",
        "complaint": "customer_success",
        "sales": "sales_team"
    }
    
    return {
        **state,
        "department": department_map.get(intent, "general_support")
    }

def handle_billing(state: CustomerServiceState) -> CustomerServiceState:
    """Handle billing inquiries"""
    return {
        **state,
        "response": "I'll connect you with our billing department to help with your payment inquiry.",
        "escalation_needed": True
    }

def handle_technical(state: CustomerServiceState) -> CustomerServiceState:
    """Handle technical issues"""
    return {
        **state,
        "response": "I'll route your technical issue to our support team. They'll contact you within 24 hours.",
        "escalation_needed": True
    }

def handle_general(state: CustomerServiceState) -> CustomerServiceState:
    """Handle general inquiries"""
    return {
        **state,
        "response": "I can help with general questions. What would you like to know?",
        "escalation_needed": False
    }

def handle_complaint(state: CustomerServiceState) -> CustomerServiceState:
    """Handle complaints"""
    return {
        **state,
        "response": "I'm sorry to hear about your experience. I'll escalate this to our customer success team immediately.",
        "escalation_needed": True
    }

def handle_sales(state: CustomerServiceState) -> CustomerServiceState:
    """Handle sales inquiries"""
    return {
        **state,
        "response": "I'll connect you with our sales team to discuss our products and pricing.",
        "escalation_needed": True
    }

def route_handler(state: CustomerServiceState) -> str:
    """Route to appropriate handler based on intent"""
    intent = state["intent"]
    return intent

def create_customer_service():
    """Create customer service router"""
    graph = StateGraph(CustomerServiceState)
    
    # Add nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("determine_priority", determine_priority)
    graph.add_node("route_to_department", route_to_department)
    graph.add_node("billing", handle_billing)
    graph.add_node("technical", handle_technical)
    graph.add_node("general", handle_general)
    graph.add_node("complaint", handle_complaint)
    graph.add_node("sales", handle_sales)
    
    # Add edges
    graph.add_edge("classify_intent", "determine_priority")
    graph.add_edge("determine_priority", "route_to_department")
    graph.add_edge("route_to_department", "route_handler")
    
    # Add conditional edges
    graph.add_conditional_edges(
        "route_to_department",
        route_handler,
        {
            "billing": "billing",
            "technical": "technical",
            "general": "general",
            "complaint": "complaint",
            "sales": "sales"
        }
    )
    
    # Set entry and finish points
    graph.set_entry_point("classify_intent")
    graph.set_finish_point("billing")
    graph.set_finish_point("technical")
    graph.set_finish_point("general")
    graph.set_finish_point("complaint")
    graph.set_finish_point("sales")
    
    return graph.compile()
```

## Memory-Enhanced Agent

### Conversational Agent with Memory

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
import google.generativeai as genai

class MemoryState(TypedDict):
    user_message: str
    bot_response: str
    conversation_memory: list[dict]
    user_preferences: dict
    context: str

def load_memory(state: MemoryState) -> MemoryState:
    """Load conversation memory and context"""
    # In a real implementation, this would load from persistent storage
    memory = state.get("conversation_memory", [])
    preferences = state.get("user_preferences", {})
    
    # Build context from recent conversation
    recent_messages = memory[-5:] if len(memory) > 5 else memory
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
    
    return {
        **state,
        "conversation_memory": memory,
        "user_preferences": preferences,
        "context": context
    }

def generate_contextual_response(state: MemoryState) -> MemoryState:
    """Generate response with memory context"""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    message = state["user_message"]
    context = state["context"]
    preferences = state["user_preferences"]
    
    # Build prompt with context
    prompt = f"""
    You are a helpful AI assistant with memory of previous conversations.
    
    Previous conversation context:
    {context}
    
    User preferences: {preferences}
    
    Current message: {message}
    
    Respond naturally, referencing previous context when relevant.
    """
    
    response = model.generate_content(prompt)
    
    # Update memory
    new_memory = state["conversation_memory"] + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response.text}
    ]
    
    return {
        **state,
        "bot_response": response.text,
        "conversation_memory": new_memory
    }

def update_preferences(state: MemoryState) -> MemoryState:
    """Update user preferences based on conversation"""
    message = state["user_message"].lower()
    preferences = state["user_preferences"]
    
    # Simple preference extraction
    if "i like" in message or "i prefer" in message:
        # Extract preference (simplified)
        if "formal" in message:
            preferences["tone"] = "formal"
        elif "casual" in message:
            preferences["tone"] = "casual"
    
    if "call me" in message:
        # Extract name (simplified)
        name = message.split("call me")[-1].strip()
        preferences["name"] = name
    
    return {
        **state,
        "user_preferences": preferences
    }

def create_memory_agent():
    """Create memory-enhanced conversational agent"""
    graph = StateGraph(MemoryState)
    
    # Add nodes
    graph.add_node("load_memory", load_memory)
    graph.add_node("generate_response", generate_contextual_response)
    graph.add_node("update_preferences", update_preferences)
    
    # Add edges
    graph.add_edge("load_memory", "generate_response")
    graph.add_edge("generate_response", "update_preferences")
    
    # Set entry and finish points
    graph.set_entry_point("load_memory")
    graph.set_finish_point("update_preferences")
    
    # Add memory checkpoint
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
```

## Error Handling Patterns

### Robust Error Handling

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
import logging
from datetime import datetime

class RobustState(TypedDict):
    input_data: str
    processed_data: str
    error: str
    retry_count: int
    max_retries: int
    success: bool

def validate_input(state: RobustState) -> RobustState:
    """Validate input data"""
    input_data = state.get("input_data", "")
    
    if not input_data:
        return {
            **state,
            "error": "Input data is required",
            "success": False
        }
    
    if len(input_data) > 1000:
        return {
            **state,
            "error": "Input data too long (max 1000 characters)",
            "success": False
        }
    
    return {
        **state,
        "success": True
    }

def process_data(state: RobustState) -> RobustState:
    """Process data with error handling"""
    try:
        input_data = state["input_data"]
        
        # Simulate processing that might fail
        if "error" in input_data.lower():
            raise ValueError("Simulated processing error")
        
        processed_data = f"Processed: {input_data.upper()}"
        
        return {
            **state,
            "processed_data": processed_data,
            "success": True
        }
        
    except Exception as e:
        logging.error(f"Processing error: {e}")
        return {
            **state,
            "error": str(e),
            "success": False
        }

def handle_error(state: RobustState) -> RobustState:
    """Handle errors and determine retry strategy"""
    error = state["error"]
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 3)
    
    logging.error(f"Error occurred: {error} (retry {retry_count}/{max_retries})")
    
    if retry_count < max_retries:
        return {
            **state,
            "retry_count": retry_count + 1,
            "error": "",  # Clear error for retry
            "success": True  # Allow retry
        }
    else:
        return {
            **state,
            "error": f"Max retries exceeded. Final error: {error}",
            "success": False
        }

def should_retry(state: RobustState) -> str:
    """Determine if we should retry or fail"""
    if state.get("success", False):
        return "continue"
    elif state.get("retry_count", 0) < state.get("max_retries", 3):
        return "retry"
    else:
        return "fail"

def create_robust_processor():
    """Create robust data processor with error handling"""
    graph = StateGraph(RobustState)
    
    # Add nodes
    graph.add_node("validate", validate_input)
    graph.add_node("process", process_data)
    graph.add_node("handle_error", handle_error)
    
    # Add edges
    graph.add_edge("validate", "process")
    graph.add_edge("handle_error", "process")
    
    # Add conditional edges
    graph.add_conditional_edges(
        "process",
        should_retry,
        {
            "continue": END,
            "retry": "handle_error",
            "fail": END
        }
    )
    
    # Set entry point
    graph.set_entry_point("validate")
    
    return graph.compile()
```

## Performance Optimization

### Async Processing with Caching

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
import asyncio
import aiohttp
from functools import lru_cache
import hashlib

class OptimizedState(TypedDict):
    query: str
    cache_key: str
    cached_result: str
    api_response: str
    final_result: str
    processing_time: float

@lru_cache(maxsize=128)
def cached_expensive_operation(query: str) -> str:
    """Cached expensive operation"""
    # Simulate expensive computation
    import time
    time.sleep(0.1)  # Simulate API call delay
    return f"Cached result for: {query}"

def generate_cache_key(state: OptimizedState) -> OptimizedState:
    """Generate cache key for query"""
    query = state["query"]
    cache_key = hashlib.md5(query.encode()).hexdigest()
    
    return {
        **state,
        "cache_key": cache_key
    }

def check_cache(state: OptimizedState) -> OptimizedState:
    """Check if result is in cache"""
    query = state["query"]
    
    try:
        cached_result = cached_expensive_operation(query)
        return {
            **state,
            "cached_result": cached_result,
            "final_result": cached_result
        }
    except:
        return {
            **state,
            "cached_result": "",
            "final_result": ""
        }

async def fetch_from_api(state: OptimizedState) -> OptimizedState:
    """Fetch data from external API"""
    query = state["query"]
    
    # Simulate API call
    await asyncio.sleep(0.2)
    api_response = f"API response for: {query}"
    
    return {
        **state,
        "api_response": api_response,
        "final_result": api_response
    }

def should_use_cache(state: OptimizedState) -> str:
    """Determine if we should use cache or fetch from API"""
    if state.get("cached_result"):
        return "use_cache"
    else:
        return "fetch_api"

def create_optimized_processor():
    """Create optimized processor with caching"""
    graph = StateGraph(OptimizedState)
    
    # Add nodes
    graph.add_node("generate_key", generate_cache_key)
    graph.add_node("check_cache", check_cache)
    graph.add_node("fetch_api", fetch_from_api)
    
    # Add edges
    graph.add_edge("generate_key", "check_cache")
    
    # Add conditional edges
    graph.add_conditional_edges(
        "check_cache",
        should_use_cache,
        {
            "use_cache": END,
            "fetch_api": "fetch_api"
        }
    )
    
    # Set entry and finish points
    graph.set_entry_point("generate_key")
    graph.set_finish_point("fetch_api")
    
    return graph.compile()
```

## Studio Integration Examples

### Testing in Studio

For each example above, you can test in Studio with these inputs:

```python
# Chatbot testing
chatbot_tests = [
    {"user_message": "Hello, how are you?"},
    {"user_message": "What's the weather like?"},
    {"user_message": "Can you help me with Python?"}
]

# Document Q&A testing
document_tests = [
    {
        "document_text": "Python is a programming language...",
        "user_question": "What is Python?"
    }
]

# Customer service testing
service_tests = [
    {"customer_message": "I have a billing question"},
    {"customer_message": "My app is not working"},
    {"customer_message": "I want to buy your product"}
]
```

### Studio Configuration for Examples

```json
{
  "dependencies": ["."],
  "graphs": {
    "chatbot": "./examples/chatbot.py:create_chatbot",
    "document_qa": "./examples/document_qa.py:create_document_qa",
    "research_assistant": "./examples/research.py:create_research_assistant",
    "customer_service": "./examples/customer_service.py:create_customer_service",
    "memory_agent": "./examples/memory_agent.py:create_memory_agent",
    "robust_processor": "./examples/robust.py:create_robust_processor",
    "optimized_processor": "./examples/optimized.py:create_optimized_processor"
  },
  "env": ".env"
}
```

These examples demonstrate various patterns and best practices for building LangGraph applications that work seamlessly with Studio's visual interface and debugging capabilities.

---

*These examples provide practical implementations that you can run, test, and modify in LangGraph Studio. Each example includes error handling, proper state management, and Studio integration patterns.*
