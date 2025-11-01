"""
Attack Simulator - DoS Testing Tool
This script simulates DoS attacks by sending multiple requests to test the detection system
"""

import requests
import time
import threading
from datetime import datetime
import sys


class AttackSimulator:
    def __init__(self, target_url, detection_url):
        self.target_url = target_url
        self.detection_url = detection_url
        self.request_count = 0
        self.success_count = 0
        self.blocked_count = 0
        self.running = False
    
    def send_request(self):
        """Send a single request to the target"""
        try:
            response = requests.get(self.target_url, timeout=2)
            self.request_count += 1
            
            if response.status_code == 200:
                self.success_count += 1
                return True
            else:
                self.blocked_count += 1
                return False
                
        except requests.exceptions.RequestException as e:
            self.blocked_count += 1
            return False
    
    def simulate_normal_traffic(self, duration=30, requests_per_second=1):
        """Simulate normal traffic (should not trigger detection)"""
        print("\n" + "="*60)
        print("🟢 SIMULATING NORMAL TRAFFIC")
        print("="*60)
        print(f"Duration: {duration} seconds")
        print(f"Rate: {requests_per_second} request(s) per second")
        print("="*60 + "\n")
        
        self.reset_counters()
        start_time = time.time()
        
        while time.time() - start_time < duration:
            self.send_request()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Request #{self.request_count} sent - Success: {self.success_count}, Blocked: {self.blocked_count}")
            time.sleep(1.0 / requests_per_second)
        
        self.print_summary()
    
    def simulate_dos_attack(self, total_requests=50, delay=0.1):
        """Simulate DoS attack (should trigger detection)"""
        print("\n" + "="*60)
        print("🔴 SIMULATING DoS ATTACK")
        print("="*60)
        print(f"Total Requests: {total_requests}")
        print(f"Delay between requests: {delay} seconds")
        print("="*60 + "\n")
        
        self.reset_counters()
        start_time = time.time()
        
        for i in range(total_requests):
            self.send_request()
            
            if (i + 1) % 10 == 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Progress: {i+1}/{total_requests} - Success: {self.success_count}, Blocked: {self.blocked_count}")
            
            time.sleep(delay)
        
        elapsed_time = time.time() - start_time
        print(f"\n⏱️  Attack completed in {elapsed_time:.2f} seconds")
        self.print_summary()
    
    def simulate_distributed_attack(self, total_requests=100, num_threads=5):
        """Simulate distributed DoS attack using multiple threads"""
        print("\n" + "="*60)
        print("🔴 SIMULATING DISTRIBUTED DoS ATTACK")
        print("="*60)
        print(f"Total Requests: {total_requests}")
        print(f"Number of Threads: {num_threads}")
        print("="*60 + "\n")
        
        self.reset_counters()
        self.running = True
        start_time = time.time()
        
        requests_per_thread = total_requests // num_threads
        threads = []
        
        def thread_worker(thread_id, num_requests):
            for i in range(num_requests):
                if not self.running:
                    break
                self.send_request()
                time.sleep(0.05)
        
        # Start threads
        for i in range(num_threads):
            thread = threading.Thread(target=thread_worker, args=(i, requests_per_thread))
            thread.start()
            threads.append(thread)
        
        # Monitor progress
        while any(t.is_alive() for t in threads):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Requests sent: {self.request_count} - Success: {self.success_count}, Blocked: {self.blocked_count}")
            time.sleep(1)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        elapsed_time = time.time() - start_time
        print(f"\n⏱️  Attack completed in {elapsed_time:.2f} seconds")
        self.print_summary()
    
    def reset_counters(self):
        """Reset all counters"""
        self.request_count = 0
        self.success_count = 0
        self.blocked_count = 0
    
    def print_summary(self):
        """Print attack summary"""
        print("\n" + "="*60)
        print("📊 ATTACK SUMMARY")
        print("="*60)
        print(f"Total Requests Sent: {self.request_count}")
        print(f"Successful Requests: {self.success_count}")
        print(f"Blocked Requests: {self.blocked_count}")
        
        if self.request_count > 0:
            block_rate = (self.blocked_count / self.request_count) * 100
            print(f"Block Rate: {block_rate:.1f}%")
        
        print("="*60 + "\n")


def print_menu():
    """Print main menu"""
    print("\n" + "="*60)
    print("🧪 DoS ATTACK SIMULATOR")
    print("="*60)
    print("1. Simulate Normal Traffic (Should NOT trigger detection)")
    print("2. Simulate DoS Attack (Should trigger detection)")
    print("3. Simulate Distributed DoS Attack (Multiple threads)")
    print("4. Custom Attack (Configure parameters)")
    print("5. Exit")
    print("="*60)


def main():
    """Main function"""
    # Default configuration
    target_url = "http://127.0.0.1:5000/"
    detection_url = "http://127.0.0.1:8000/"
    
    print("\n" + "="*60)
    print("🛡️  DoS ATTACK SIMULATOR - Testing Tool")
    print("="*60)
    print(f"Target Server: {target_url}")
    print(f"Detection Server: {detection_url}")
    print("="*60)
    
    # Check if servers are running
    try:
        requests.get(target_url, timeout=2)
        print("✅ Target server is running")
    except:
        print("❌ Target server is NOT running!")
        print("   Please start target_server.py first")
        return
    
    try:
        requests.get(detection_url, timeout=2)
        print("✅ Detection server is running")
    except:
        print("⚠️  Detection server is NOT running!")
        print("   Start app.py to monitor attacks")
    
    simulator = AttackSimulator(target_url, detection_url)
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            # Normal traffic
            duration = int(input("Enter duration in seconds (default 30): ") or "30")
            rate = float(input("Enter requests per second (default 1): ") or "1")
            simulator.simulate_normal_traffic(duration, rate)
            
        elif choice == '2':
            # DoS attack
            total = int(input("Enter total requests (default 50): ") or "50")
            delay = float(input("Enter delay between requests in seconds (default 0.1): ") or "0.1")
            simulator.simulate_dos_attack(total, delay)
            
        elif choice == '3':
            # Distributed attack
            total = int(input("Enter total requests (default 100): ") or "100")
            threads = int(input("Enter number of threads (default 5): ") or "5")
            simulator.simulate_distributed_attack(total, threads)
            
        elif choice == '4':
            # Custom attack
            print("\n📝 Custom Attack Configuration:")
            total = int(input("Total requests: "))
            delay = float(input("Delay between requests (seconds): "))
            simulator.simulate_dos_attack(total, delay)
            
        elif choice == '5':
            print("\n👋 Exiting simulator...")
            break
            
        else:
            print("\n❌ Invalid choice! Please select 1-5")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Simulator interrupted by user")
        sys.exit(0)
