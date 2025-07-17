"""
Test for motivation summary creation

This module tests that all motivation summary documents
have been created as specified in Subtask 2.5.
"""

import os

def test_motivation_summary():
    """Test that motivation summary is created"""
    
    required_files = [
        'src/modules/introduction/lessons/lesson-1-motivation/motivation_summary.md',
        'src/modules/introduction/lessons/lesson-1-motivation/advantages.md',
        'src/modules/introduction/lessons/lesson-1-motivation/comparison.md',
        'src/modules/introduction/lessons/lesson-1-motivation/use_cases.md'
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Missing {file_path}"
    
    print("✅ Motivation summary created")
    return True

def test_motivation_summary_content():
    """Test that motivation summary has required content"""
    
    # Test motivation_summary.md
    with open('src/modules/introduction/lessons/lesson-1-motivation/motivation_summary.md', 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'Why LangGraph?' in content
        assert 'Core Problems LangGraph Solves' in content
        assert 'Key Advantages' in content
        assert 'When to Use LangGraph' in content
    
    # Test advantages.md
    with open('src/modules/introduction/lessons/lesson-1-motivation/advantages.md', 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'Reliability and Controllability' in content
        assert 'Low-level and Extensible' in content
        assert 'First-class Streaming Support' in content
    
    # Test comparison.md
    with open('src/modules/introduction/lessons/lesson-1-motivation/comparison.md', 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'LangGraph vs LangChain' in content
        assert 'LangGraph vs AutoGen' in content
        assert 'Decision Matrix' in content
    
    # Test use_cases.md
    with open('src/modules/introduction/lessons/lesson-1-motivation/use_cases.md', 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'Enterprise Applications' in content
        assert 'Healthcare Applications' in content
        assert 'Financial Services' in content
    
    print("✅ Motivation summary content verified")
    return True

def test_three_advantages_documented():
    """Test that three main advantages are clearly documented"""
    
    advantages = [
        "Reliability and Controllability",
        "Low-level and Extensible", 
        "First-class Streaming Support"
    ]
    
    with open('src/modules/introduction/lessons/lesson-1-motivation/advantages.md', 'r', encoding='utf-8') as f:
        content = f.read()
        for advantage in advantages:
            assert advantage in content, f"Missing advantage: {advantage}"
    
    print("✅ Three advantages clearly documented")
    return True

def test_comparison_included():
    """Test that comparison with alternatives is included"""
    
    alternatives = [
        "LangChain",
        "AutoGen", 
        "CrewAI",
        "Custom Solutions"
    ]
    
    with open('src/modules/introduction/lessons/lesson-1-motivation/comparison.md', 'r', encoding='utf-8') as f:
        content = f.read()
        for alternative in alternatives:
            assert alternative in content, f"Missing comparison with {alternative}"
    
    print("✅ Comparison with alternatives included")
    return True

def test_use_cases_identified():
    """Test that use cases are identified"""
    
    use_case_categories = [
        "Enterprise Applications",
        "Healthcare Applications", 
        "Financial Services",
        "Education and Training",
        "Manufacturing and Supply Chain",
        "Creative Industries",
        "Government and Public Services"
    ]
    
    with open('src/modules/introduction/lessons/lesson-1-motivation/use_cases.md', 'r', encoding='utf-8') as f:
        content = f.read()
        for category in use_case_categories:
            assert category in content, f"Missing use case category: {category}"
    
    print("✅ Use cases identified")
    return True

if __name__ == "__main__":
    test_motivation_summary()
    test_motivation_summary_content()
    test_three_advantages_documented()
    test_comparison_included()
    test_use_cases_identified()
    print("🎉 All motivation summary tests passed!") 