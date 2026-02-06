from app.constants.app_constants import (
    AppConstants,
    Environment,
    ALLOWED_FILES,
    OPENAI_CHAT_MODEL,
    GEMINI_CHAT_MODEL,
    VECTOR_DB,
)


def test_environment_enum_values():
    assert Environment.LOCAL.value == "local"
    assert Environment.DEV.value == "dev"
    assert Environment.PROD.value == "prod"


def test_allowed_files_enum_values():
    assert ALLOWED_FILES.PDF.value == ".pdf"
    assert ALLOWED_FILES.DOCX.value == ".docx"
    assert ALLOWED_FILES.ALL_FILES.value == (".pdf", ".docx")


def test_app_constants_values():
    assert AppConstants.HOST.value == "127.0.0.1"
    assert AppConstants.PORT.value == 3000
    assert AppConstants.RELOAD.value is True


def test_model_constants():
    assert OPENAI_CHAT_MODEL.MODEL_NAME.value == "gpt-4o-mini"
    assert OPENAI_CHAT_MODEL.TEMPERATURE.value == 0.0
    assert GEMINI_CHAT_MODEL.MODEL_NAME.value == "gemini-3-flash-preview"
    assert GEMINI_CHAT_MODEL.TEMPERATURE.value == 0.0


def test_vector_db_constants():
    assert VECTOR_DB.NAME.value == "agentic_rag_template"
    assert VECTOR_DB.COLLECTION_NAME.value == "agentic_rag_template"
    assert VECTOR_DB.TOP_K.value == 5
