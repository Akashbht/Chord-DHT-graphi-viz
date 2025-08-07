#!/usr/bin/env python3
"""
Performance Testing Example for Chord DHT Network

This example demonstrates performance testing of the Chord DHT network,
including load testing, latency measurements, and scalability analysis.
"""

import sys
import os
import time
import random
from statistics import mean, median, stdev

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Node import Node
from Network import Network


def performance_test():
    """Comprehensive performance testing of Chord DHT"""
    print("=== Chord DHT Performance Testing ===\n")
    
    # Test configurations
    test_configs = [
        {"m": 4, "nodes": 8, "data_items": 100},
        {"m": 6, "nodes": 20, "data_items": 500},
        {"m": 8, "nodes": 50, "data_items": 1000},
    ]
    
    results = []
    
    for config in test_configs:
        print(f"Testing configuration: m={config['m']}, nodes={config['nodes']}, data={config['data_items']}")
        result = run_performance_test(config)
        results.append(result)
        print(f"✓ Test completed\n")
    
    # Display summary results
    print("=== Performance Summary ===")
    print(f"{'Config':<15} {'Insert (ms)':<12} {'Lookup (ms)':<12} {'Success Rate':<12} {'Throughput':<12}")
    print("-" * 70)
    
    for i, result in enumerate(results):
        config = test_configs[i]
        config_str = f"m={config['m']},n={config['nodes']}"
        print(f"{config_str:<15} {result['avg_insert']:<12.2f} {result['avg_lookup']:<12.2f} "
              f"{result['success_rate']:<12.1f}% {result['throughput']:<12.0f}")


def run_performance_test(config):
    """Run performance test for a specific configuration"""
    m = config['m']
    num_nodes = config['nodes']
    num_data_items = config['data_items']
    
    # Setup network
    Node.m = m
    Node.ring_size = 2 ** m
    node_ids = random.sample(range(Node.ring_size), num_nodes)
    network = Network(m, node_ids)
    
    # Add remaining nodes
    for node_id in node_ids[1:]:
        node = network.create_node(node_id)
        node.join(network.first_node)
        network.nodes.append(node)
    
    # Generate test data
    test_data = [f"file_{i:06d}.txt" for i in range(num_data_items)]
    
    # Measure insertion performance
    insert_times = []
    print(f"  Inserting {num_data_items} data items...")
    
    start_total = time.time()
    
    for data in test_data:
        start_time = time.time()
        try:
            network.insert_data(data)
            insert_time = (time.time() - start_time) * 1000  # Convert to ms
            insert_times.append(insert_time)
        except Exception as e:
            print(f"    Insert failed for {data}: {e}")
    
    total_insert_time = time.time() - start_total
    
    # Measure lookup performance
    lookup_times = []
    successful_lookups = 0
    print(f"  Performing {num_data_items} lookups...")
    
    # Test lookup for all inserted data
    for data in test_data:
        start_time = time.time()
        try:
            result = network.find_data(data)
            lookup_time = (time.time() - start_time) * 1000  # Convert to ms
            lookup_times.append(lookup_time)
            if result:
                successful_lookups += 1
        except Exception as e:
            print(f"    Lookup failed for {data}: {e}")
    
    # Calculate statistics
    avg_insert = mean(insert_times) if insert_times else 0
    avg_lookup = mean(lookup_times) if lookup_times else 0
    success_rate = (successful_lookups / len(test_data)) * 100 if test_data else 0
    throughput = len(test_data) / total_insert_time if total_insert_time > 0 else 0
    
    # Cleanup
    try:
        network.cleanup()
    except:
        pass
    
    return {
        'avg_insert': avg_insert,
        'avg_lookup': avg_lookup,
        'success_rate': success_rate,
        'throughput': throughput,
        'insert_times': insert_times,
        'lookup_times': lookup_times
    }


def stress_test():
    """Stress test with high load"""
    print("\n=== Stress Test ===")
    
    m = 10  # Large ring
    num_nodes = 100
    num_operations = 5000
    
    print(f"Stress test: m={m}, nodes={num_nodes}, operations={num_operations}")
    
    # Setup large network
    Node.m = m
    Node.ring_size = 2 ** m
    node_ids = random.sample(range(Node.ring_size), num_nodes)
    network = Network(m, node_ids)
    
    # Add nodes gradually to simulate realistic join patterns
    batch_size = 10
    for i in range(1, len(node_ids), batch_size):
        batch = node_ids[i:i+batch_size]
        for node_id in batch:
            try:
                node = network.create_node(node_id)
                node.join(network.first_node)
                network.nodes.append(node)
            except Exception as e:
                print(f"Failed to add node {node_id}: {e}")
    
    print(f"✓ Network setup complete with {len(network.nodes)} nodes")
    
    # Stress test with mixed operations
    operations = []
    for i in range(num_operations):
        if random.random() < 0.7:  # 70% insert operations
            operations.append(('insert', f'stress_file_{i:06d}.dat'))
        else:  # 30% lookup operations
            if i > 100:  # Ensure there's data to lookup
                lookup_id = random.randint(0, i-1)
                operations.append(('lookup', f'stress_file_{lookup_id:06d}.dat'))
            else:
                operations.append(('insert', f'stress_file_{i:06d}.dat'))
    
    # Execute stress test
    start_time = time.time()
    successful_ops = 0
    failed_ops = 0
    
    print(f"Executing {len(operations)} mixed operations...")
    
    for i, (op_type, data) in enumerate(operations):
        try:
            if op_type == 'insert':
                network.insert_data(data)
            else:  # lookup
                network.find_data(data)
            successful_ops += 1
        except Exception as e:
            failed_ops += 1
            if failed_ops <= 5:  # Show first few errors
                print(f"  Operation failed: {op_type} {data} - {e}")
        
        # Progress update
        if (i + 1) % 1000 == 0:
            print(f"  Progress: {i+1}/{len(operations)} operations completed")
    
    total_time = time.time() - start_time
    
    print(f"\n=== Stress Test Results ===")
    print(f"Total operations: {len(operations)}")
    print(f"Successful: {successful_ops}")
    print(f"Failed: {failed_ops}")
    print(f"Success rate: {(successful_ops/len(operations)*100):.1f}%")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Throughput: {len(operations)/total_time:.0f} ops/sec")
    
    # Final health check
    print(f"\n=== Final Health Check ===")
    health_status = network.check_network_health()
    for check, status in health_status.items():
        print(f"{'✓' if status else '✗'} {check}: {'PASS' if status else 'FAIL'}")
    
    # Cleanup
    try:
        network.cleanup()
        print("✓ Cleanup completed")
    except Exception as e:
        print(f"✗ Cleanup failed: {e}")


if __name__ == "__main__":
    performance_test()
    stress_test()