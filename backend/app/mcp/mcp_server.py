from app.mcp.tools import mcp

if __name__ == "__main__":
    # Docker/웹 환경에서는 stdio가 아닌 sse로 실행해야 합니다.
    # 호스트는 0.0.0.0, 포트는 Dockerfile/Compose와 일치하는 8200으로 설정
    mcp.run(transport='sse')

# run streamlit
# streamlit run frontend/App.py
