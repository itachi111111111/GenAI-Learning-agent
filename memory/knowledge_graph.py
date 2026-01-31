import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import math

KNOWLEDGE_GRAPH_FILE = "data/knowledge_graph.json"


class KnowledgeGraph:
    """
    Tracks concept mastery using spaced repetition algorithm (SM-2)
    and prerequisite relationships.
    """
    
    def __init__(self):
        self.concepts = {}  # concept_name -> metadata
        self.prerequisites = {}  # concept -> [prerequisites]
        self.load()
    
    def load(self):
        if os.path.exists(KNOWLEDGE_GRAPH_FILE):
            with open(KNOWLEDGE_GRAPH_FILE, 'r') as f:
                data = json.load(f)
                self.concepts = data.get('concepts', {})
                self.prerequisites = data.get('prerequisites', {})
    
    def save(self):
        os.makedirs(os.path.dirname(KNOWLEDGE_GRAPH_FILE), exist_ok=True)
        with open(KNOWLEDGE_GRAPH_FILE, 'w') as f:
            json.dump({
                'concepts': self.concepts,
                'prerequisites': self.prerequisites,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
    
    def add_concept(self, concept: str, prerequisites: List[str] = None):
        """Register a new concept in the knowledge graph"""
        if concept not in self.concepts:
            self.concepts[concept] = {
                'mastery_level': 0.0,  # 0.0 to 1.0
                'exposure_count': 0,
                'successful_applications': 0,
                'failed_attempts': 0,
                'last_reviewed': None,
                'next_review': datetime.now().isoformat(),
                'interval': 1,  # Days until next review
                'ease_factor': 2.5,  # SM-2 ease factor
                'status': 'new'  # new|learning|review|mastered
            }
        
        if prerequisites:
            self.prerequisites[concept] = prerequisites
        self.save()
    
    def update_mastery(self, concept: str, performance: float):
        """
        Update mastery based on performance (0.0 to 1.0)
        Uses SM-2 spaced repetition algorithm
        """
        if concept not in self.concepts:
            self.add_concept(concept)
        
        node = self.concepts[concept]
        node['exposure_count'] += 1
        
        # SM-2 Algorithm
        if performance >= 0.7:  # Successful response
            node['successful_applications'] += 1
            
            if node['status'] == 'new':
                node['status'] = 'learning'
                node['interval'] = 1
            elif node['status'] == 'learning':
                node['interval'] = 2
                node['status'] = 'review'
            else:
                # Increase interval
                node['interval'] = int(node['interval'] * node['ease_factor'])
            
            # Update ease factor
            node['ease_factor'] = max(1.3, node['ease_factor'] + (0.1 - (1 - performance) * 0.15))
            
        else:  # Failed response
            node['failed_attempts'] += 1
            node['interval'] = 1
            node['status'] = 'learning'
            node['ease_factor'] = max(1.3, node['ease_factor'] - 0.2)
        
        # Calculate mastery level (exponential moving average)
        old_mastery = node['mastery_level']
        node['mastery_level'] = old_mastery * 0.7 + performance * 0.3
        
        node['last_reviewed'] = datetime.now().isoformat()
        interval = min(node['interval'], 365)  # Cap at 1 year
        next_review = datetime.now() + timedelta(days=interval)
        node['next_review'] = next_review.isoformat()
        
        self.save()
        return node['mastery_level']
    
    def get_readiness_score(self, concept: str) -> float:
        """
        Returns 0.0-1.0 indicating readiness to learn this concept
        Based on prerequisite mastery
        """
        if concept not in self.concepts:
            return 0.0
        
        prereqs = self.prerequisites.get(concept, [])
        if not prereqs:
            return 1.0
        
        mastery_sum = sum(self.concepts.get(p, {}).get('mastery_level', 0) for p in prereqs)
        return min(1.0, mastery_sum / len(prereqs))
    
    def get_learning_path(self, target_concept: str) -> List[str]:
        """
        Returns ordered list of concepts to learn to reach target
        Uses topological sort on prerequisite graph
        """
        visited = set()
        path = []
        
        def dfs(concept):
            if concept in visited or concept not in self.prerequisites:
                return
            visited.add(concept)
            for prereq in self.prerequisites.get(concept, []):
                if self.concepts.get(prereq, {}).get('mastery_level', 0) < 0.7:
                    dfs(prereq)
                    path.append(prereq)
        
        dfs(target_concept)
        path.append(target_concept)
        return path
    
    def get_struggle_areas(self, limit: int = 3) -> List[str]:
        """Concepts with high failure rates"""
        struggles = []
        for concept, data in self.concepts.items():
            total = data['successful_applications'] + data['failed_attempts']
            if total > 0:
                success_rate = data['successful_applications'] / total
                if success_rate < 0.5 and data['exposure_count'] > 2:
                    struggles.append((concept, success_rate))
        
        struggles.sort(key=lambda x: x[1])
        return [s[0] for s in struggles[:limit]]
    
    def get_due_reviews(self) -> List[str]:
        """NEW METHOD: Get concepts due for spaced repetition"""
        now = datetime.now()
        due = []
        
        for concept, data in self.concepts.items():
            if data['next_review']:
                review_date = datetime.fromisoformat(data['next_review'])
                if review_date <= now:
                    due.append(concept)
        
        return due
    
    def export_for_llm(self) -> str:
        """Export relevant data for LLM context"""
        due_reviews = self.get_due_reviews()  # NOW THIS WORKS!
        struggles = self.get_struggle_areas()
        
        mastered = [c for c, d in self.concepts.items() if d['mastery_level'] > 0.8]
        learning = [c for c, d in self.concepts.items() if 0.3 < d['mastery_level'] <= 0.8]
        
        return json.dumps({
            'mastered_concepts': mastered,
            'learning_concepts': learning,
            'struggle_areas': struggles,
            'due_for_review': due_reviews,
            'total_concepts': len(self.concepts),
            'average_mastery': sum(d['mastery_level'] for d in self.concepts.values()) / len(self.concepts) if self.concepts else 0
        })


# Global instance
_knowledge_graph = KnowledgeGraph()


def get_concept_mastery(concept: str) -> str:
    """Tool for agents to query mastery"""
    kg = _knowledge_graph
    if concept not in kg.concepts:
        return json.dumps({"status": "unknown", "concept": concept})
    
    data = kg.concepts[concept]
    readiness = kg.get_readiness_score(concept)
    
    return json.dumps({
        "concept": concept,
        "mastery_level": data['mastery_level'],
        "status": data['status'],
        "exposures": data['exposure_count'],
        "readiness": readiness,
        "prerequisites": kg.prerequisites.get(concept, [])
    })


def get_due_reviews() -> str:
    """Wrapper function for external access"""
    due = _knowledge_graph.get_due_reviews()
    return json.dumps({"due_concepts": due, "count": len(due)})


def update_concept_mastery(concept: str, performance: float):
    """Interface for runner to update after interactions"""
    _knowledge_graph.update_mastery(concept, performance)
    _knowledge_graph.save()


def export_knowledge_graph() -> str:
    """Get full graph for teaching agent context"""
    return _knowledge_graph.export_for_llm()