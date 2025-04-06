#!/usr/bin/env python3
import sys
from utilities.system_check import SystemCheck

def main():
    """Run system check to verify environment"""
    system_check = SystemCheck()
    success = system_check.run()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 