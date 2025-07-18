# Routing Workflows

## Overview

Routing workflows are intelligent systems that dynamically direct requests, tasks, or data through different processing paths based on conditions, priorities, or content analysis. These workflows enable adaptive, efficient processing that can handle complex business logic and varying requirements.

## Key Characteristics

- **Dynamic Decision Making**: Routes change based on real-time conditions
- **Multi-Path Processing**: Multiple possible execution paths
- **Conditional Logic**: Complex decision trees and business rules
- **Error Handling**: Graceful handling of failures and edge cases
- **Scalability**: Can handle varying loads and priorities

## Common Use Cases

### 1. Customer Service Routing

**Problem**: Incoming customer requests need to be directed to the most appropriate agent or department based on the request type, urgency, and complexity.

**Solution**: Intelligent routing system that analyzes request content and routes accordingly.

```python
from langgraph.graph import StateGraph, MessagesState
from typing import Literal

class CustomerServiceState(TypedDict):
    messages: List[BaseMessage]
    request_type: str
    priority: str
    department: str
    agent_assigned: str

def classify_request(state: CustomerServiceState) -> Literal["technical", "billing", "general", "urgent"]:
    messages = state["messages"]
    if not messages:
        return "general"
    
    last_message = messages[-1].content.lower()
    
    # Urgency detection
    urgent_words = ["urgent", "emergency", "broken", "down"]
    if any(word in last_message for word in urgent_words):
        return "urgent"
    
    # Request type classification
    if any(word in last_message for word in ["error", "bug", "technical", "code"]):
        return "technical"
    elif any(word in last_message for word in ["bill", "payment", "charge", "refund"]):
        return "billing"
    else:
        return "general"

def assign_department(state: CustomerServiceState) -> CustomerServiceState:
    request_type = state["request_type"]
    
    department_map = {
        "technical": "tech_support",
        "billing": "billing_department", 
        "general": "customer_service",
        "urgent": "urgent_support"
    }
    
    return {
        **state,
        "department": department_map.get(request_type, "customer_service")
    }

# Build the routing workflow
workflow = StateGraph(CustomerServiceState)

workflow.add_node("classify", classify_request)
workflow.add_node("assign", assign_department)

workflow.add_conditional_edges("classify", lambda x: x["request_type"], {
    "technical": "assign",
    "billing": "assign", 
    "general": "assign",
    "urgent": "assign"
})

workflow.add_edge("assign", END)
```

**Benefits**:
- Faster response times for urgent issues
- Better resource allocation
- Improved customer satisfaction
- Reduced agent workload

### 2. Email Processing and Classification

**Problem**: High volume of incoming emails need to be automatically classified and routed to appropriate departments or individuals.

**Solution**: AI-powered email classification system with intelligent routing.

```python
class EmailState(TypedDict):
    email_content: str
    sender: str
    subject: str
    classification: str
    priority: str
    department: str
    spam_score: float

def analyze_email(state: EmailState) -> EmailState:
    content = state["email_content"].lower()
    subject = state["subject"].lower()
    
    # Spam detection
    spam_indicators = ["buy now", "limited time", "act fast", "make money"]
    spam_score = sum(1 for indicator in spam_indicators if indicator in content)
    
    # Classification
    if "order" in content or "purchase" in content:
        classification = "sales"
    elif "support" in content or "help" in content:
        classification = "support"
    elif "job" in content or "career" in content:
        classification = "hr"
    else:
        classification = "general"
    
    # Priority assessment
    urgent_words = ["urgent", "emergency", "asap"]
    priority = "high" if any(word in content for word in urgent_words) else "normal"
    
    return {
        **state,
        "spam_score": spam_score,
        "classification": classification,
        "priority": priority
    }

def route_email(state: EmailState) -> Literal["spam", "high_priority", "normal_priority", "low_priority"]:
    if state["spam_score"] > 2:
        return "spam"
    elif state["priority"] == "high":
        return "high_priority"
    elif state["classification"] in ["sales", "support"]:
        return "normal_priority"
    else:
        return "low_priority"

workflow = StateGraph(EmailState)
workflow.add_node("analyze", analyze_email)
workflow.add_conditional_edges("analyze", route_email, {
    "spam": "spam_handler",
    "high_priority": "immediate_processing",
    "normal_priority": "standard_processing",
    "low_priority": "batch_processing"
})
```

**Benefits**:
- Automatic spam filtering
- Priority-based processing
- Efficient resource allocation
- Improved response times

### 3. Approval Workflows

**Problem**: Business requests need to be routed through appropriate approval levels based on amount, type, and organizational hierarchy.

**Solution**: Multi-level approval system with intelligent routing.

```python
class ApprovalState(TypedDict):
    request_details: dict
    amount: float
    requester_level: str
    request_type: str
    approval_path: List[str]
    current_approver: str

def evaluate_request(state: ApprovalState) -> ApprovalState:
    amount = state["amount"]
    request_type = state["request_type"]
    
    # Determine approval path based on amount and type
    if amount > 10000:
        approval_path = ["manager", "director", "vp"]
    elif amount > 5000:
        approval_path = ["manager", "director"]
    elif amount > 1000:
        approval_path = ["manager"]
    else:
        approval_path = ["auto_approve"]
    
    return {
        **state,
        "approval_path": approval_path,
        "current_approver": approval_path[0] if approval_path else "auto_approve"
    }

def route_approval(state: ApprovalState) -> Literal["auto_approve", "manager", "director", "vp", "reject"]:
    current_approver = state["current_approver"]
    
    if current_approver == "auto_approve":
        return "auto_approve"
    elif current_approver == "manager":
        return "manager"
    elif current_approver == "director":
        return "director"
    elif current_approver == "vp":
        return "vp"
    else:
        return "reject"

workflow = StateGraph(ApprovalState)
workflow.add_node("evaluate", evaluate_request)
workflow.add_conditional_edges("evaluate", route_approval, {
    "auto_approve": "auto_approval",
    "manager": "manager_approval",
    "director": "director_approval", 
    "vp": "vp_approval",
    "reject": "rejection_handler"
})
```

**Benefits**:
- Automated approval routing
- Compliance with business rules
- Audit trail
- Faster processing

### 4. Content Processing Pipeline

**Problem**: Different types of content (text, images, videos) need different processing workflows based on content type and requirements.

**Solution**: Content-aware routing system that directs content to appropriate processing pipelines.

```python
class ContentState(TypedDict):
    content: str
    content_type: str
    file_size: int
    processing_requirements: List[str]
    quality_level: str

def analyze_content(state: ContentState) -> ContentState:
    content = state["content"]
    file_size = state["file_size"]
    
    # Determine content type
    if content.endswith(('.jpg', '.png', '.gif')):
        content_type = "image"
    elif content.endswith(('.mp4', '.avi', '.mov')):
        content_type = "video"
    elif content.endswith(('.txt', '.doc', '.pdf')):
        content_type = "text"
    else:
        content_type = "unknown"
    
    # Determine quality requirements
    if file_size > 10000000:  # 10MB
        quality_level = "high"
    elif file_size > 1000000:  # 1MB
        quality_level = "medium"
    else:
        quality_level = "low"
    
    return {
        **state,
        "content_type": content_type,
        "quality_level": quality_level
    }

def route_content(state: ContentState) -> Literal["image_processing", "video_processing", "text_processing", "unknown"]:
    content_type = state["content_type"]
    
    if content_type == "image":
        return "image_processing"
    elif content_type == "video":
        return "video_processing"
    elif content_type == "text":
        return "text_processing"
    else:
        return "unknown"

workflow = StateGraph(ContentState)
workflow.add_node("analyze", analyze_content)
workflow.add_conditional_edges("analyze", route_content, {
    "image_processing": "image_pipeline",
    "video_processing": "video_pipeline",
    "text_processing": "text_pipeline",
    "unknown": "error_handler"
})
```

**Benefits**:
- Optimized processing for each content type
- Resource efficiency
- Quality-based processing
- Scalable architecture

## Implementation Patterns

### 1. Multi-Stage Routing

```python
def multi_stage_router(state: State) -> str:
    stage = state.get("current_stage", "initial")
    
    if stage == "initial":
        return "classification"
    elif stage == "classification":
        return "priority_assessment"
    elif stage == "priority_assessment":
        return "resource_allocation"
    else:
        return "processing"

workflow.add_conditional_edges("route", multi_stage_router, {
    "classification": "classify_node",
    "priority_assessment": "priority_node",
    "resource_allocation": "allocation_node",
    "processing": "process_node"
})
```

### 2. Error Recovery Routing

```python
def error_recovery_router(state: State) -> str:
    error_count = state.get("error_count", 0)
    error_type = state.get("error_type")
    
    if error_count > 3:
        return "escalate"
    elif error_type == "retryable":
        return "retry"
    elif error_type == "validation":
        return "fix_validation"
    else:
        return "continue"

workflow.add_conditional_edges("handle_error", error_recovery_router, {
    "escalate": "escalation_node",
    "retry": "retry_node",
    "fix_validation": "validation_node",
    "continue": "continue_node"
})
```

### 3. Performance-Based Routing

```python
def performance_router(state: State) -> str:
    response_time = state.get("response_time", 0)
    queue_size = state.get("queue_size", 0)
    
    if response_time > 5000:
        return "optimize"
    elif queue_size > 100:
        return "scale"
    else:
        return "normal"

workflow.add_conditional_edges("route", performance_router, {
    "optimize": "optimization_node",
    "scale": "scaling_node",
    "normal": "normal_node"
})
```

## Best Practices

### 1. Design for Scalability

```python
# ✅ Good: Scalable routing logic
def scalable_router(state: State) -> str:
    # Use simple, fast decision logic
    priority = state.get("priority", "normal")
    return "high" if priority == "high" else "normal"

# ❌ Avoid: Complex logic in routing functions
def complex_router(state: State) -> str:
    # Don't put heavy computation in routing functions
    # This can slow down the entire workflow
    pass
```

### 2. Handle Edge Cases

```python
def robust_router(state: State) -> str:
    try:
        # Main routing logic
        condition = state.get("condition")
        if condition == "valid":
            return "valid_path"
        else:
            return "invalid_path"
    except Exception:
        # Always provide a fallback
        return "error_path"
```

### 3. Monitor and Log

```python
def monitored_router(state: State) -> str:
    # Log routing decisions for monitoring
    decision = route_logic(state)
    log_routing_decision(state, decision)
    return decision
```

## Related Use Cases

- [Chatbots](chatbots/) - Intelligent conversation routing
- [Agents](agents/) - Multi-agent coordination and routing
- [Research](research/) - Research workflow automation
- [Business Process Automation](workflows/) - Enterprise workflow routing 