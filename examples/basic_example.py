#!/usr/bin/env python3
"""
Basic Chord DHT Network Example

This example demonstrates the basic usage of the Chord DHT network,
including node creation, data insertion, lookup, and visualization.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Node import Node
from Network import Network
import time


def basic_chord_example():
    """Demonstrate basic Chord DHT operations"""
    print("=== Basic Chord DHT Network Example ===\n")
    
    # Set up network parameters
    m = 4  # Ring size = 2^4 = 16
    initial_nodes = [0, 4, 8, 12]
    
    print(f"Creating Chord network with m={m} (ring size: {2**m})")
    print(f"Initial nodes: {initial_nodes}\n")
    
    # Initialize network
    Node.m = m
    Node.ring_size = 2 ** m
    network = Network(m, initial_nodes)
    
    # Add more nodes to the network
    additional_nodes = [2, 6, 10, 14]
    print(f"Adding additional nodes: {additional_nodes}")
    
    for node_id in additional_nodes:
        network.insert_node(node_id)
        print(f"✓ Node {node_id} added successfully")
    
    print(f"\nNetwork now has {len(network.nodes)} nodes")
    
    # Insert some test data
    test_data = [
        "document1.pdf",
        "image.jpg", 
        "video.mp4",
        "music.mp3",
        "source_code.py",
        "database.db",
        "config.xml",
        "readme.txt"
    ]
    
    print(f"\nInserting test data: {test_data}")
    for data in test_data:
        network.insert_data(data)
        hashed_key = network.hash_function(data)
        responsible_node = network.first_node.find_successor(hashed_key)
        print(f"✓ '{data}' (key: {hashed_key}) stored on node {responsible_node.node_id}")
    
    # Demonstrate data lookup
    print("\n=== Data Lookup Tests ===")
    for data in test_data[:3]:  # Test first 3 items
        result = network.find_data(data)
        if result:
            print(f"✓ Found '{data}': {result}")
        else:
            print(f"✗ '{data}' not found")
    
    # Test lookup for non-existent data
    result = network.find_data("nonexistent_file.txt")
    print(f"✗ 'nonexistent_file.txt' found: {result}")
    
    # Display network information
    print("\n=== Network Information ===")
    network_info = network.get_network_info()
    for key, value in network_info.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    
    # Generate network visualization
    print("\n=== Generating Network Visualization ===")
    try:
        network.print_network()
        print("✓ Network graph generated as 'network_graph.svg'")
    except Exception as e:
        print(f"✗ Visualization failed: {e}")
    
    # Demonstrate node deletion
    print("\n=== Node Deletion Test ===")
    node_to_delete = 6
    print(f"Deleting node {node_to_delete}")
    try:
        network.delete_node(node_to_delete)
        print(f"✓ Node {node_to_delete} deleted successfully")
        print(f"Network now has {len(network.nodes)} nodes")
    except Exception as e:
        print(f"✗ Node deletion failed: {e}")
    
    # Final network health check
    print("\n=== Network Health Check ===")
    health_status = network.check_network_health()
    for check, status in health_status.items():
        status_symbol = "✓" if status else "✗"
        print(f"{status_symbol} {check}: {'PASS' if status else 'FAIL'}")
    
    # Cleanup
    print("\n=== Cleanup ===")
    try:
        network.cleanup()
        print("✓ Network cleanup completed")
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    basic_chord_example()