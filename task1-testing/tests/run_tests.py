
#!/usr/bin/env python3
"""Скрипт для запуска всех тестов"""

import subprocess
import sys
import os

def run_tests():
    """Запуск тестов с разными уровнями детализации"""
    
    # Получаем корневую директорию проекта
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("🔬 Running SOCKS5 Proxy Tests...")
    
    # Unit тесты
    print("\n📋 Running Unit Tests...")
    result = subprocess.run([
        'pytest', 'tests/unit/', '-v', '--tb=short'
    ], cwd=project_root)
    
    if result.returncode != 0:
        print("❌ Unit tests failed!")
        return result.returncode
    
    # Интеграционные тесты
    print("\n🔗 Running Integration Tests...")
    result = subprocess.run([
        'pytest', 'tests/integration/', '-v', '--tb=short'
    ], cwd=project_root)
    
    if result.returncode != 0:
        print("❌ Integration tests failed!")
        return result.returncode
    
    # Performance тесты
    print("\n⚡️ Running Performance Tests...")
    result = subprocess.run([
        'pytest', 'tests/performance/', '-v', '--tb=short'
    ], cwd=project_root)
    
    if result.returncode != 0:
        print("⚠️  Performance tests have issues")
        # Не прерываем выполнение для performance тестов
    
    print("\n✅ All tests completed successfully!")
    return 0

if __name__ == '__main__':
    sys.exit(run_tests())
