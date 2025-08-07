#!/usr/bin/env python3
"""
Test suite for Node class functionality
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Node import Node


class TestNode:
    """Test suite for Node class"""
    
    def setup_method(self):
        """Setup test environment before each test"""
        self.m = 4
        self.node_id = 0
        Node.m = self.m
        Node.ring_size = 2 ** self.m
        self.node = Node(self.node_id, self.m)
    
    def test_node_initialization(self):
        """Test node initialization with correct parameters"""
        assert self.node.node_id == self.node_id
        assert self.node.m == self.m
        assert self.node.ring_size == 2 ** self.m
        assert self.node.predecessor == self.node
        assert self.node.successor == self.node
        assert len(self.node.fingers_table) == self.m
        assert all(finger == self.node for finger in self.node.fingers_table)
    
    def test_node_string_representation(self):
        """Test string representation of node"""
        expected = f"Node {self.node_id}"
        assert str(self.node) == expected
    
    def test_node_comparison(self):
        """Test node comparison operations"""
        node1 = Node(5, self.m)
        node2 = Node(10, self.m)
        
        assert node1 < node2
        assert not node2 < node1
    
    def test_data_encryption_decryption(self):
        """Test data encryption and decryption"""
        test_data = "test_file.txt"
        
        # Encrypt data
        encrypted = self.node.encrypt_data(test_data)
        assert encrypted != test_data
        assert isinstance(encrypted, bytes)
        
        # Decrypt data
        decrypted = self.node.decrypt_data(encrypted)
        assert decrypted == test_data
    
    def test_heartbeat(self):
        """Test heartbeat functionality"""
        initial_time = self.node.last_heartbeat
        result = self.node.send_heartbeat()
        
        assert result is True
        assert self.node.last_heartbeat > initial_time
    
    def test_distance_calculation(self):
        """Test distance calculation between nodes"""
        # Test cases for ring size 16 (m=4)
        test_cases = [
            (0, 0, 0),    # Same node
            (0, 1, 1),    # Adjacent nodes
            (0, 8, 8),    # Half ring
            (15, 1, 2),   # Wrap around
            (10, 5, 11),  # Wrap around case
        ]
        
        for n1, n2, expected in test_cases:
            result = self.node.distance(n1, n2)
            assert result == expected, f"Distance({n1}, {n2}) = {result}, expected {expected}"
    
    def test_cache_operations(self):
        """Test cache storage and lookup"""
        key = 42
        node_ref = Node(5, self.m)
        
        # Store in cache
        self.node.cache_store(key, node_ref)
        
        # Lookup from cache
        result = self.node.cache_lookup(key)
        assert result == node_ref
        
        # Test cache miss
        result = self.node.cache_lookup(999)
        assert result is None
    
    def test_load_calculation(self):
        """Test node load calculation"""
        # Initially no data
        load = self.node.check_load()
        assert load == 0
        
        # Add some data
        self.node.data[1] = "file1"
        self.node.data[2] = "file2"
        self.node.data[3] = "file3"
        
        load = self.node.check_load()
        expected_load = 3 / self.node.ring_size
        assert load == expected_load
    
    def test_metrics_update(self):
        """Test metrics tracking"""
        initial_lookups = self.node.metrics['lookups']
        initial_successful = self.node.metrics['successful_lookups']
        
        # Test successful lookup
        self.node.update_metrics(lookup_success=True)
        assert self.node.metrics['lookups'] == initial_lookups + 1
        assert self.node.metrics['successful_lookups'] == initial_successful + 1
        
        # Test failed lookup
        initial_failed = self.node.metrics['failed_lookups']
        self.node.update_metrics(lookup_success=False)
        assert self.node.metrics['failed_lookups'] == initial_failed + 1
    
    def test_backup_creation(self):
        """Test backup data creation"""
        # Add some test data
        self.node.data[1] = "test_data_1"
        self.node.data[2] = "test_data_2"
        
        # Create another node as successor
        successor = Node(8, self.m)
        self.node.successor = successor
        
        # Create backup
        self.node.backup_to_successor()
        
        # Verify backup was created
        assert hasattr(successor, 'backup_data')
        assert successor.backup_data['node_id'] == self.node.node_id
        assert 1 in successor.backup_data['data']
        assert 2 in successor.backup_data['data']
    
    def test_state_export(self):
        """Test node state export for backup"""
        # Add some test data
        test_data = "test_file.txt"
        encrypted_data = self.node.encrypt_data(test_data)
        self.node.data[42] = encrypted_data
        
        # Set up successor and predecessor
        successor = Node(8, self.m)
        predecessor = Node(12, self.m)
        self.node.successor = successor
        self.node.predecessor = predecessor
        
        # Export state
        state = self.node.export_state()
        
        # Verify exported state
        assert state['node_id'] == self.node.node_id
        assert state['successor_id'] == successor.node_id
        assert state['predecessor_id'] == predecessor.node_id
        assert '42' in state['data']
        assert state['data']['42'] == test_data  # Should be decrypted
        assert 'metrics' in state
        assert 'load' in state
        assert 'timestamp' in state


if __name__ == "__main__":
    pytest.main([__file__])