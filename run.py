from pathlib import Path
import streamlit.web.cli as stcli

if __name__ == "__main__":
    app = Path(__file__).parent / "app" / "main.py"
    import sys
    sys.argv = ["streamlit", "run", str(app)]
    raise SystemExit(stcli.main())
