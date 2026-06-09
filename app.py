import streamlit as st
import os


from auth.register import register_user
from auth.login import login_user

from utils.file_saver import save_uploaded_file

from ingestion.file_router import route_file

from rag.chunking import chunk_text
from rag.rag_chain import generate_rag_response

from vectordb.vector_store import store_chunks

from database.chat_history import (
    save_message,
    load_chat_history
)

from database.document_manager import (
    save_document,
    get_user_documents,
    delete_document
)

from database.supabase_storage import upload_file_to_storage

from vectordb.vector_store import is_vector_store_empty

from rag.rebuild_vectors import rebuild_all_vectors

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="ChatPDF AI", page_icon="🤖", layout="wide")

print("=" * 50)
print("APP STARTED")
print("=" * 50)

# temporary fix

if "vectors_checked" not in st.session_state:

    st.session_state.vectors_checked = True

    print("VECTOR CHECK STARTED")

    empty = is_vector_store_empty()

    print(f"IS EMPTY = {empty}")

    if empty:

        print("REBUILD STARTED")

        with st.spinner("Rebuilding vector database..."):
            rebuild_all_vectors()

        print("REBUILD FINISHED")

    else:

        print("REBUILD NOT REQUIRED")

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0E1117;
    color: white;
}


/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161B22;
    border-right: 1px solid #30363D;
}


/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background: linear-gradient(
        135deg,
        #7C3AED,
        #2563EB
    );
    color: white;
    font-weight: 600;
    padding: 0.6rem 1rem;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    opacity: 0.9;
}


/* Chat Input */
[data-testid="stChatInput"] {
    border-radius: 15px;
}


/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 15px;
    padding: 1rem;
}


/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    padding: 1rem;
    border-radius: 15px;
}


/* Expander */
.streamlit-expanderHeader {
    background-color: #161B22;
    border-radius: 10px;
}


/* Text Input */
.stTextInput > div > div > input {
    background-color: #161B22;
    color: white;
    border-radius: 10px;
}


/* Select Box */
.stSelectbox > div > div {
    background-color: #161B22;
    border-radius: 10px;
}


/* Success Message */
.stAlert {
    border-radius: 12px;
}


/* Hide Streamlit Footer */
footer {
    visibility: hidden;
}


/* Hide Hamburger Menu */
#MainMenu {
    visibility: hidden;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 15px;
    padding: 1rem;
    margin-bottom: 1rem;
}


/* Assistant Messages */
[data-testid="stChatMessageContent"] {
    font-size: 1rem;
    line-height: 1.7;
}


/* Expander Sources */
details {
    background-color: #161B22;
    border-radius: 12px;
    border: 1px solid #30363D;
    padding: 0.5rem;
}


/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #30363D;
    border-radius: 10px;
}

::-webkit-scrollbar-track {
    background: #0E1117;
}   


/* Better spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* Cleaner markdown */
h1, h2, h3 {
    letter-spacing: 0.5px;
}


/* Code blocks */
pre {
    border-radius: 12px !important;
}


/* Chat spacing */
[data-testid="stChatMessage"] {
    margin-top: 1rem;
    margin-bottom: 1rem;
}       

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_document" not in st.session_state:
    st.session_state.current_document = None

if "retrieval_documents" not in st.session_state:
    st.session_state.retrieval_documents = []


# ---------------- AUTH SECTION ---------------- #

if not st.session_state.logged_in:

    st.markdown("""
<div style="
padding: 2rem;
border-radius: 20px;
background: linear-gradient(
135deg,
#111827,
#1E293B
);
border: 1px solid #30363D;
margin-bottom: 2rem;
">

# 🤖 ChatPDF AI

### Multi-Document AI Workspace

Chat with PDFs, documents, screenshots, and knowledge bases using:

✅ Hybrid Search  
✅ Reranking  
✅ OCR  
✅ Streaming AI  
✅ Multi-Document RAG  

</div>
""", unsafe_allow_html=True)

    auth_mode = st.radio(
        "Select Mode",
        ["Login", "Signup"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    # SIGNUP
    if auth_mode == "Signup":

        if st.button("Create Account"):

            if username and password:

                success = register_user(
                    username,
                    password
                )

                if success:

                    st.success(
                        "Account created successfully!"
                    )

                else:

                    st.error(
                        "Username already exists."
                    )

            else:

                st.warning(
                    "Please enter username and password."
                )

    # LOGIN
    else:

        if st.button("Login"):

            user_id = login_user(
                username,
                password
            )

            if user_id:

                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username

                st.success("Login successful!")

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    st.stop()


# ---------------- HEADER ---------------- #

st.markdown("""
# 🤖 ChatPDF AI

### Multi-Document AI Assistant with RAG, OCR & Hybrid Search

Upload documents, extract knowledge, and chat with your files using advanced AI retrieval.
""")


# ---------------- DASHBOARD METRICS ---------------- #

st.markdown("""
<div style="
padding: 1rem;
border-radius: 15px;
background: linear-gradient(
135deg,
#7C3AED,
#2563EB
);
margin-top: 1rem;
margin-bottom: 1rem;
">

### 🚀 AI Pipeline Active

OCR • Hybrid Search • Reranking • Gemini • Multi-Document RAG

</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Knowledge Files",
        len(
            get_user_documents(
                st.session_state.user_id
            )
        )
    )

with col2:
    st.metric(
        "AI Model",
        "Gemini"
    )

with col3:
    st.metric(
        "Retrieval",
        "Hybrid + Rerank"
    )


# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.markdown(f"""
    # 🤖 ChatPDF AI
                
    
    **{st.session_state.username}**
    """)
    
    st.caption(
    "AI-Powered Knowledge Workspace"
)

    st.divider()

    st.subheader("📁 Your Documents")

    user_docs = get_user_documents(
        st.session_state.user_id
    )

    if user_docs:

        selected_doc = st.selectbox(
            "Select Document",
            user_docs
        )

        selected_retrieval_docs = st.multiselect(
    "Documents for Retrieval",
    user_docs,
    default=[selected_doc]
)
        st.session_state.retrieval_documents = (
    selected_retrieval_docs
)

        

        col1, col2 = st.columns(2)

        # LOAD DOCUMENT
        with col1:

            if st.button("Load"):

                st.session_state.current_document = selected_doc

                history = load_chat_history(
                    selected_doc,
                    st.session_state.user_id
                )

                st.session_state.messages = [
                    {
                        "role": role,
                        "content": message
                    }
                    for role, message in history
                ]

                st.success(
                    f"{selected_doc} loaded!"
                )

                st.rerun()

        # DELETE DOCUMENT
        with col2:

            if st.button("Delete"):

                delete_document(
                    st.session_state.user_id,
                    selected_doc
                )

                if (
                    st.session_state.current_document
                    == selected_doc
                ):

                    st.session_state.current_document = None
                    st.session_state.messages = []

                st.success(
                    "Document deleted successfully!"
                )

                st.rerun()

    else:

        st.info(
            "No documents uploaded yet."
        )

    st.divider()

    # CLEAR CHAT
    if st.button("Clear Current Chat"):

        st.session_state.messages = []

        st.success("Chat cleared!")

    st.divider()

    # LOGOUT
    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.messages = []
        st.session_state.current_document = None

        st.rerun()


# ---------------- FILE UPLOAD ---------------- #

st.markdown("""
<div style="
padding: 1.5rem;
border-radius: 18px;
background-color: #161B22;
border: 1px solid #30363D;
margin-bottom: 1rem;
">

## 📤 Upload Documents

Supported:
PDF • DOCX • TXT • PNG • JPG

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload PDF, DOCX, TXT or Image",
    type=[
        "pdf",
        "docx",
        "txt",
        "png",
        "jpg",
        "jpeg"
    ]
)


if uploaded_file:

    try:

        with st.spinner(
            "🧠 Extracting text, generating embeddings and indexing knowledge..."
        ):

            # Save file
            file_path = save_uploaded_file(uploaded_file)

            upload_file_to_storage(
                file_path, uploaded_file.name, st.session_state.user_id
            )

            # Extract text
            document_data = route_file(file_path)

            # Chunk text
            chunks = chunk_text(document_data)

            # Document name
            document_name = os.path.basename(file_path)

            # Store chunks
            store_chunks(
                chunks=chunks,
                source_name=document_name,
                user_id=st.session_state.user_id,
            )

            # Save document
            save_document(st.session_state.user_id, document_name)

            # Delete uploaded file after successful indexing
            if os.path.exists(file_path):
                os.remove(file_path)

            # Set active document
            st.session_state.current_document = document_name

            # Load old chats
            history = load_chat_history(document_name, st.session_state.user_id)

            st.session_state.messages = [
                {"role": role, "content": message} for role, message in history
            ]

            st.success("Document processed successfully!")

            st.metric("Chunks Stored", len(chunks))

    except Exception as e:

        st.error(f"Error: {str(e)}")

st.divider()


# ---------------- CHAT SECTION ---------------- #

st.markdown("""
<div style="
padding: 1rem;
border-radius: 15px;
background-color: #161B22;
border: 1px solid #30363D;
margin-top: 1rem;
margin-bottom: 1rem;
">

## 💬 AI Knowledge Chat

Ask questions across all uploaded documents using semantic retrieval and reranking.

</div>
""", unsafe_allow_html=True)


if st.session_state.current_document:

    st.markdown(f"""
    <div style="
    padding: 1rem;
    border-radius: 15px;
    background-color: #161B22;
    border: 1px solid #30363D;
    margin-bottom: 1rem;
    ">
    <h4>📄 Active Workspace</h4>
    <p>{st.session_state.current_document}</p>
    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
<div style="
padding: 2rem;
border-radius: 15px;
background-color: #161B22;
border: 1px dashed #30363D;
text-align: center;
margin-top: 2rem;
">

## 📂 No Active Workspace

Upload documents to start chatting with your AI knowledge base.

</div>
""", unsafe_allow_html=True)

if st.session_state.retrieval_documents:

    docs_text = ", ".join(
        st.session_state.retrieval_documents
    )

    st.info(
        f"📚 Searching Across: {docs_text}"
    )


# ---------------- DISPLAY CHAT ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------- CHAT INPUT ---------------- #

user_question = st.chat_input(
    "Ask questions across your AI workspace..."
)


if user_question and st.session_state.current_document:

    # Save user message locally
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Save user message in DB
    save_message(
        role="user",
        message=user_question,
        document_name=st.session_state.current_document,
        user_id=st.session_state.user_id
    )

    # Show user message
    with st.chat_message("user"):

        st.markdown(user_question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Generating response..."):

            try:

                result = generate_rag_response(
                    question=user_question,
                    user_id=st.session_state.user_id,
                    chat_history=st.session_state.messages,
                    selected_documents=
        st.session_state.retrieval_documents
                )

                # Streaming placeholder
                response_placeholder = st.empty()

                full_response = ""

                # Stream tokens
                for chunk in result["stream"]:

                    if chunk.text:

                        full_response += chunk.text

                        response_placeholder.markdown(
                            full_response + "▌"
                        )

                # Final response
                response_placeholder.markdown(
                    full_response
                )

                # Save assistant message locally
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

                # Save assistant message in DB
                save_message(
                    role="assistant",
                    message=full_response,
                    document_name=st.session_state.current_document,
                    user_id=st.session_state.user_id
                )

                # Sources
                with st.expander(
                    "📚 View Sources & Citations"
                    ):
                    for index, doc in enumerate(
                        result["sources"]
                        ):
                        st.markdown(f"""
                                    <div style="
                                    padding: 1rem;
                                    border-radius: 12px;
                                    background-color: #161B22;
                                    border: 1px solid #30363D;
                                    margin-bottom: 1rem;
                                    ">

<h4>📄 Source {index + 1}</h4>

<p><b>Document:</b> {doc.metadata.get('source')}</p>

<p><b>Page:</b> {doc.metadata.get('page')}</p>

<p><b>Chunk:</b> {doc.metadata.get('chunk_id')}</p>

</div>
""", unsafe_allow_html=True)

                        st.code(
                            doc.page_content,
                            language="text"
                            )

                        st.caption(
                            f"""
                            Document: {doc.metadata.get('source')}
                            | Page: {doc.metadata.get('page')}
                            | Chunk: {doc.metadata.get('chunk_id')}
"""
                        )

            except Exception as e:
                error_message = str(e)

                if "quota" in error_message.lower():
                    st.error(
            "Gemini API quota exceeded. Please try again later or use a different API key."
        )
                else:
                    st.error(
                        f"Error: {error_message}"
                        )
