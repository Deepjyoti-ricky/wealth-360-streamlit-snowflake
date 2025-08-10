#!/usr/bin/env python3
"""
Dependency installer script for BFSI Wealth 360 Analytics Platform.

This script helps ensure all required dependencies are properly installed
for both local development and Streamlit in Snowflake deployment.
"""

import subprocess
import sys


def install_requirements():
    """Install requirements from requirements.txt"""
    print("🚀 Installing BFSI Wealth 360 Analytics Platform dependencies...")

    try:
        # Upgrade pip first
        print("📦 Upgrading pip...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        )

        # Install requirements
        print("📋 Installing requirements from requirements.txt...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )

        print("✅ All dependencies installed successfully!")
        print("\n🎯 Ready to run: streamlit run streamlit_app.py")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("\n🔧 Try running manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)


def check_imports():
    """Test critical imports"""
    print("\n🧪 Testing critical imports...")

    try:
        import streamlit

        print(f"✅ streamlit {streamlit.__version__}")

        import plotly

        print(f"✅ plotly {plotly.__version__}")

        import pandas

        print(f"✅ pandas {pandas.__version__}")

        import snowflake.snowpark  # noqa: F401

        print("✅ snowflake-snowpark-python")

        import pydeck

        print(f"✅ pydeck {pydeck.__version__}")

        import numpy

        print(f"✅ numpy {numpy.__version__}")

        print("\n🎉 All critical imports successful!")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Try reinstalling dependencies")
        sys.exit(1)


if __name__ == "__main__":
    print("🏦 BFSI Wealth 360 Analytics Platform - Dependency Setup")
    print("=" * 60)

    install_requirements()
    check_imports()

    print("\n" + "=" * 60)
    print("🚀 Setup complete! You can now run:")
    print("   streamlit run streamlit_app.py")
    print("\n📖 For more information, see README.md")
