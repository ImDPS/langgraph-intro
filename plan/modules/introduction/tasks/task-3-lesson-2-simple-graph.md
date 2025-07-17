# Task 3: Lesson 2 - Simple Graph

## Overview

Build your first LangGraph application by creating a simple graph with basic nodes and edges. This lesson introduces the fundamental concepts of StateGraph, nodes, and graph compilation. You'll start with a basic Python function and see how it fits into the graph structure, setting the stage for integrating Gemini LLM in subsequent lessons.

## 🎯 Learning Objectives

By the end of this lesson, you will be able to:
- Create a basic StateGraph
- Define a simple state schema using TypedDict
- Implement a basic node function
- Set the entry and finish points of a graph
- Compile and run a LangGraph application
- Understand the relationship between state, nodes, and graphs

## 📋 Atomic Subtasks

### Subtask 3.1: Create Basic State Schema
**Duration**: 30 minutes  
**Prerequisites**: Task 2 (Lesson 1 - Motivation)  
**Deliverable**: Simple state schema definition

**Steps**:
1. Import TypedDict from typing and StateGraph from langgraph
2. Define a TypedDict class representing your graph's state (message and response fields)
3. Instantiate a StateGraph with your state schema
4. Write a test to verify the state schema works correctly

**Test Criteria**:
- [ ] State schema defined correctly using TypedDict
- [ ] All imports working without errors
- [ ] State structure is clear and simple for initial graph
- [ ] No type errors in schema definition
- [ ] StateGraph can be instantiated with the schema

### Subtask 3.2: Create Simple Node Function
**Duration**: 30 minutes  
**Prerequisites**: Subtask 3.1  
**Deliverable**: Working, testable node function

**Steps**:
1. Define a Python function that accepts state dictionary as its only argument
2. Implement basic logic to process the message and create a response (placeholder for future Gemini LLM integration)
3. Ensure the function returns a dictionary with updated state fields
4. Write comprehensive tests for the node function

**Test Criteria**:
- [ ] Node function defined with correct signature (state: State) -> dict
- [ ] Function correctly processes input state
- [ ] Function returns dictionary with updated state fields
- [ ] Function is testable in isolation
- [ ] Function handles edge cases gracefully

### Subtask 3.3: Build Basic Graph Structure
**Duration**: 45 minutes  
**Prerequisites**: Subtask 3.2  
**Deliverable**: Complete graph definition with single node

**Steps**:
1. Create an instance of StateGraph using your state schema
2. Add your node to the graph using the `.add_node()` method with a unique name
3. Set the entry point using `.set_entry_point()` to define where execution starts
4. Set the finish point using `.set_finish_point()` to define where execution ends
5. Verify the graph structure is correct

**Test Criteria**:
- [ ] StateGraph created successfully with state schema
- [ ] Node added to graph with appropriate name
- [ ] Entry point set correctly to node name
- [ ] Finish point set correctly to node name
- [ ] Graph structure validation passes

### Subtask 3.4: Compile and Test Graph
**Duration**: 30 minutes  
**Prerequisites**: Subtask 3.3  
**Deliverable**: Compiled, runnable graph application

**Steps**:
1. Compile your graph definition using the `.compile()` method to create a runnable application
2. Verify the compiled application has expected methods (`.invoke()`, `.stream()`)
3. Test the application by calling `.invoke()` with initial state
4. Validate that the final state returned matches expectations
5. Test error handling and edge cases

**Test Criteria**:
- [ ] Graph compiles without errors
- [ ] Compiled app has `.invoke()` and `.stream()` methods
- [ ] Application can be invoked with valid input dictionary
- [ ] Invocation returns expected final state
- [ ] Error handling works for invalid inputs

### Subtask 3.5: Create Complete Simple Graph Application
**Duration**: 45 minutes  
**Prerequisites**: All previous subtasks  
**Deliverable**: Complete, documented simple graph application

**Steps**:
1. Create a complete Python file (`simple_graph.py`) containing state definition, node function, graph definition, and compilation
2. Add comprehensive documentation (docstrings and comments) explaining each component
3. Create a `README.md` file with clear instructions on how to run the application
4. Create an `example_usage.py` file demonstrating how to import and use the application
5. Ensure the application follows best practices and is production-ready

**Test Criteria**:
- [ ] Complete `simple_graph.py` file created with all components
- [ ] Code is well-documented with clear explanations
- [ ] `README.md` file provides clear usage instructions
- [ ] `example_usage.py` file demonstrates proper usage
- [ ] Application can be imported and run from external scripts
- [ ] Code follows Python best practices and conventions

## 🧪 Integration Test

**Test Name**: Complete Simple Graph Application  
**Duration**: 20 minutes  
**Prerequisites**: All subtasks completed

**Steps**:
1. Run all individual subtask tests to ensure each component works
2. Test the complete application workflow using the `example_usage.py` script
3. Verify that all components (state, node, graph) work together seamlessly
4. Test the compiled app with various input messages to ensure consistent behavior
5. Validate error handling and edge cases in the complete application

## 📊 Success Criteria

- [ ] All subtasks completed successfully
- [ ] All individual tests are passing
- [ ] Simple graph application runs correctly end-to-end
- [ ] Code is well-documented and easy to understand
- [ ] Usage examples are clear and functional
- [ ] Integration test passes successfully
- [ ] Application handles edge cases gracefully

## 🚀 Next Steps

After completing this task, you can proceed to:
- **Task 4**: Lesson 3 - LangGraph Studio
- **Alternative**: Experiment with different node functions and state structures
- **Optional**: Enhance the state schema with additional fields and modify nodes accordingly

## 📝 Notes

- **Start Simple**: Begin with basic mechanics to understand core concepts. The power of LangGraph emerges from how simple pieces connect.
- **Independent Testing**: Testing each component separately (like the node function) is crucial for building complex graphs.
- **LangChain Integration**: The compiled application is a standard LangChain Runnable with familiar interfaces (`.invoke`, `.stream`, `.batch`).
- **Foundation Building**: This simple graph sets the foundation for more complex applications with LLM integration.
- **State Management**: Understanding state flow is essential for all subsequent LangGraph development.

## 🔗 Related Concepts

- **State Management**: How data flows through your graph
- **Node Functions**: The building blocks of graph logic
- **Graph Compilation**: Converting graph definitions to runnable applications
- **LangChain Integration**: How LangGraph fits into the broader LangChain ecosystem

---

*Last Updated: 2025-07-17*  
*Task Lead: LangGraph Team*