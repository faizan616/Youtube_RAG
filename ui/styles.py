import streamlit as st


def load_custom_css():

    st.html(
        """
        <style>

        /* ==================================================
           GLOBAL
           ================================================== */

        .stApp {
            background: #f7f7f7;
            color: #202020;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* Main text */
        .stApp p,
        .stApp label,
        .stApp span {
            color: #202020;
        }

        /* Streamlit headers */
        h1, h2, h3, h4 {
            color: #181818 !important;
        }

        /* Hide Streamlit branding */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }


        /* ==================================================
           HEADER
           ================================================== */

        .app-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 12px;
        }

        .youtube-logo {
            width: 48px;
            height: 34px;

            background: #ff0000;

            border-radius: 9px;

            display: flex;
            align-items: center;
            justify-content: center;
        }

        .youtube-play {
            width: 0;
            height: 0;

            border-top: 7px solid transparent;
            border-bottom: 7px solid transparent;
            border-left: 11px solid white;

            margin-left: 3px;
        }

        .app-title {
            font-size: 30px;
            font-weight: 750;

            color: #181818 !important;

            line-height: 1.1;
        }

        .app-subtitle {
            font-size: 14px;

            color: #666666 !important;

            margin-top: 4px;
        }


        /* ==================================================
           URL INPUT
           ================================================== */

        .stTextInput input {
            background: white !important;

            color: #202020 !important;

            border: 1px solid #cccccc !important;

            border-radius: 9px !important;
        }

        .stTextInput input::placeholder {
            color: #888888 !important;
        }

        .stTextInput input:focus {
            border-color: #ff0000 !important;

            box-shadow: 0 0 0 1px #ff0000 !important;
        }

        /* Load button */

        .stButton button {
            background: #ff0000 !important;

            color: white !important;

            border: none !important;

            border-radius: 9px !important;

            font-weight: 600 !important;
        }

        .stButton button:hover {
            background: #cc0000 !important;
        }


        /* ==================================================
           PROCESSING / LOADER
           ================================================== */

        [data-testid="stStatusWidget"] {
            background: white !important;

            border: 1px solid #dddddd !important;

            border-radius: 12px !important;

            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }

        [data-testid="stStatusWidget"] p {
            color: #333333 !important;

            font-size: 13px !important;
        }


        /* Processing steps */
        [data-testid="stStatusWidget"] {
            margin-top: 10px;
            margin-bottom: 8px;
        }

        [data-testid="stStatusWidget"] [data-testid="stMarkdownContainer"] p {
            margin: 0.15rem 0 !important;
        }

        /* ==================================================
           SUMMARY
           ================================================== */

        .summary-card {
            background: white;

            border: 1px solid #dddddd;

            border-radius: 14px;

            padding: 22px;

            min-height: 100%;

            box-sizing: border-box;

            box-shadow:
                0 2px 8px rgba(0, 0, 0, 0.04);
        }

        .summary-heading {
            font-size: 19px;

            font-weight: 700;

            color: #181818 !important;

            margin-bottom: 15px;
        }

        .summary-text {
            color: #444444 !important;

            font-size: 14px;

            line-height: 1.75;
        }


        /* ==================================================
           METRICS
           ================================================== */

        .metric-card {
            background: white;

            border: 1px solid #dddddd;

            border-radius: 12px;

            padding: 18px;

            min-height: 100px;

            box-sizing: border-box;

            box-shadow:
                0 2px 8px rgba(0, 0, 0, 0.04);
        }

        .metric-label {
            color: #777777 !important;

            font-size: 11px;

            font-weight: 600;

            text-transform: uppercase;

            letter-spacing: 0.7px;
        }

        .metric-value {
            color: #181818 !important;

            font-size: 25px;

            font-weight: 700;

            margin-top: 8px;
        }

        .metric-description {
            color: #888888 !important;

            font-size: 11px;

            margin-top: 4px;
        }


        /* ==================================================
           CHAT
           ================================================== */

        .chat-title {
            color: #181818 !important;

            font-size: 22px;

            font-weight: 700;

            margin-top: 10px;

            margin-bottom: 4px;
        }

        .chat-subtitle {
            color: #777777 !important;

            font-size: 13px;

            margin-bottom: 25px;
        }


        /* User message */

        .user-message {
            display: flex;

            flex-direction: column;

            align-items: flex-end;

            margin: 20px 0;
        }

        .message-label {
            color: #777777 !important;

            font-size: 11px;

            margin-bottom: 5px;
        }

        .message-content {
            background: #eeeeee;

            color: #202020 !important;

            padding: 12px 17px;

            border-radius:
                18px 18px 4px 18px;

            max-width: 70%;

            font-size: 14px;

            line-height: 1.5;
        }


        /* Assistant */

        .assistant-message {
            margin-top: 25px;
        }

        .assistant-header {
            color: #181818 !important;

            font-size: 14px;

            font-weight: 700;

            margin-bottom: 10px;
        }


        /* ==================================================
           SOURCE CHUNKS
           ================================================== */

        .source-section {
            margin-top: 25px;
        }

        .sources-heading {
            color: #181818 !important;

            font-size: 16px;

            font-weight: 700;

            margin-top: 25px;

            margin-bottom: 12px;
        }

        .source-card {
            background: white;

            border: 1px solid #dddddd;

            border-radius: 10px;

            padding: 15px 17px;

            margin-bottom: 10px;

            box-shadow:
                0 1px 5px rgba(0, 0, 0, 0.03);
        }

        .source-header {
            display: flex;

            justify-content: space-between;

            align-items: center;

            margin-bottom: 9px;
        }

        .source-chunk {
            color: #181818 !important;

            font-size: 13px;

            font-weight: 700;
        }

        .source-score {
            color: #065fd4 !important;

            font-size: 12px;

            font-weight: 600;
        }

        .source-content {
            color: #555555 !important;

            font-size: 13px;

            line-height: 1.65;
        }


        /* ==================================================
           TRANSCRIPT
           ================================================== */

        .transcript-box {
            background: white;

            border: 1px solid #dddddd;

            border-radius: 12px;

            padding: 22px;

            color: #333333 !important;

            font-size: 14px;

            line-height: 1.8;

            white-space: pre-wrap;

            max-height: 700px;

            overflow-y: auto;
        }


        /* ==================================================
           TABS
           ================================================== */

        button[data-baseweb="tab"] {
            color: #666666 !important;

            font-weight: 600 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ff0000 !important;
        }


        /* ==================================================
           EMPTY STATE
           ================================================== */

        .empty-state {
            background: white;

            border: 1px dashed #cccccc;

            border-radius: 14px;

            padding: 50px 30px;

            text-align: center;

            box-shadow:
                0 2px 8px rgba(0, 0, 0, 0.03);
        }

        .empty-title {
            color: #181818 !important;

            font-size: 20px;

            font-weight: 700;
        }

        .empty-text {
            color: #777777 !important;

            font-size: 14px;

            margin-top: 8px;
        }


        /* ==================================================
           DIVIDER
           ================================================== */

        .section-divider {
            height: 1px;

            background: #dddddd;

            margin-top: 28px;

            margin-bottom: 28px;
        }

        </style>
        """
    )