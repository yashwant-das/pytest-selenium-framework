#!/usr/bin/env python3
"""
Test script to demonstrate webdriver-manager capabilities across different browsers
"""

print("🔍 WEBDRIVER-MANAGER BROWSER SUPPORT TEST")
print("=" * 60)

# Test Chrome
print("\n1. 🟢 CHROME SUPPORT:")
try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("   ✅ ChromeDriverManager - AVAILABLE")
    try:
        path = ChromeDriverManager().install()
        print(f"   ✅ Download test - SUCCESS")
        print(f"   📁 Path: {path}")
    except Exception as e:
        print(f"   ⚠️  Download test - {e}")
except ImportError as e:
    print(f"   ❌ ChromeDriverManager - NOT AVAILABLE: {e}")

# Test Firefox
print("\n2. 🟠 FIREFOX SUPPORT:")
try:
    from webdriver_manager.firefox import GeckoDriverManager
    print("   ✅ GeckoDriverManager - AVAILABLE")
    try:
        path = GeckoDriverManager().install()
        print(f"   ✅ Download test - SUCCESS")
        print(f"   📁 Path: {path}")
    except Exception as e:
        print(f"   ⚠️  Download test - {e}")
except ImportError as e:
    print(f"   ❌ GeckoDriverManager - NOT AVAILABLE: {e}")

# Test Microsoft Edge
print("\n3. 🔵 MICROSOFT EDGE SUPPORT:")
try:
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    print("   ✅ EdgeChromiumDriverManager - AVAILABLE")
    try:
        path = EdgeChromiumDriverManager().install()
        print(f"   ✅ Download test - SUCCESS")
        print(f"   📁 Path: {path}")
    except Exception as e:
        print(f"   ⚠️  Download test - {e}")
except ImportError as e:
    print(f"   ❌ EdgeChromiumDriverManager - NOT AVAILABLE: {e}")

# Test Internet Explorer
print("\n4. 🔷 INTERNET EXPLORER SUPPORT:")
try:
    from webdriver_manager.microsoft import IEDriverManager
    print("   ✅ IEDriverManager - AVAILABLE")
    try:
        path = IEDriverManager().install()
        print(f"   ✅ Download test - SUCCESS")
        print(f"   📁 Path: {path}")
    except Exception as e:
        print(f"   ⚠️  Download test - {e}")
except ImportError as e:
    print(f"   ❌ IEDriverManager - NOT AVAILABLE: {e}")

# Test Opera
print("\n5. 🔴 OPERA SUPPORT:")
try:
    from webdriver_manager.opera import OperaDriverManager
    print("   ✅ OperaDriverManager - AVAILABLE")
    try:
        path = OperaDriverManager().install()
        print(f"   ✅ Download test - SUCCESS")
        print(f"   📁 Path: {path}")
    except Exception as e:
        print(f"   ⚠️  Download test - {e}")
except ImportError as e:
    print(f"   ❌ OperaDriverManager - NOT AVAILABLE: {e}")

# Check Safari (note: Safari doesn't need separate driver download)
print("\n6. 🟣 SAFARI SUPPORT:")
print("   ℹ️  Safari uses built-in driver (no download needed)")
print("   ℹ️  Enable via: Safari > Develop > Allow Remote Automation")

print("\n" + "=" * 60)
print("📋 SUMMARY:")
print("   webdriver-manager supports automatic downloads for:")
print("   ✅ Chrome (ChromeDriver)")
print("   ✅ Firefox (GeckoDriver)")  
print("   ✅ Edge Chromium (EdgeDriver)")
print("   ✅ Internet Explorer (IEDriver)")
print("   ✅ Opera (OperaDriver)")
print("   ℹ️  Safari (built-in driver)")
print("\n🎯 Your framework can support ALL major browsers!")
