"""Tests for exceptions module."""

from pathlib import Path

import pytest

from claude_code_docs_spa.exceptions import (
    ClaudeCodeDocsError,
    ConfigurationError,
    DocumentProcessingError,
    FetcherError,
    FileOperationError,
    InstallerError,
    NetworkError,
    PermissionError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)


class TestClaudeCodeDocsError:
    """Test suite for ClaudeCodeDocsError."""

    def test_base_exception_creation(self):
        """Test base exception creation."""
        error = ClaudeCodeDocsError("Test message")

        assert str(error) == "Test message"
        assert error.message == "Test message"

    def test_base_exception_inheritance(self):
        """Test that base exception inherits from Exception."""
        error = ClaudeCodeDocsError("Test message")

        assert isinstance(error, Exception)
        assert isinstance(error, ClaudeCodeDocsError)


class TestConfigurationError:
    """Test suite for ConfigurationError."""

    def test_config_error_without_file(self):
        """Test configuration error without file path."""
        error = ConfigurationError("Invalid configuration")

        assert str(error) == "Configuration error: Invalid configuration"
        assert error.config_file is None

    def test_config_error_with_file(self):
        """Test configuration error with file path."""
        config_file = "/path/to/config.toml"
        error = ConfigurationError("Invalid configuration", config_file)

        assert (
            str(error)
            == f"Configuration error: Invalid configuration (file: {config_file})"
        )
        assert error.config_file == Path(config_file)

    def test_config_error_inheritance(self):
        """Test that configuration error inherits from base exception."""
        error = ConfigurationError("Test error")

        assert isinstance(error, ClaudeCodeDocsError)
        assert isinstance(error, ConfigurationError)


class TestNetworkError:
    """Test suite for NetworkError."""

    def test_network_error_without_details(self):
        """Test network error without URL and status code."""
        error = NetworkError("Connection failed")

        assert str(error) == "Network error: Connection failed"
        assert error.url is None
        assert error.status_code is None

    def test_network_error_with_url(self):
        """Test network error with URL."""
        url = "https://example.com/api"
        error = NetworkError("Connection failed", url)

        assert str(error) == f"Network error: Connection failed (url: {url})"
        assert error.url == url
        assert error.status_code is None

    def test_network_error_with_status_code(self):
        """Test network error with status code."""
        error = NetworkError("HTTP error", status_code=404)

        assert str(error) == "Network error: HTTP error (status: 404)"
        assert error.status_code == 404
        assert error.url is None

    def test_network_error_with_all_details(self):
        """Test network error with URL and status code."""
        url = "https://example.com/api"
        error = NetworkError("HTTP error", url, 500)

        assert str(error) == f"Network error: HTTP error (url: {url}) (status: 500)"
        assert error.url == url
        assert error.status_code == 500


class TestFileOperationError:
    """Test suite for FileOperationError."""

    def test_file_error_without_details(self):
        """Test file operation error without details."""
        error = FileOperationError("File not found")

        assert str(error) == "File operation error: File not found"
        assert error.file_path is None
        assert error.operation is None

    def test_file_error_with_file_path(self):
        """Test file operation error with file path."""
        file_path = "/path/to/file.txt"
        error = FileOperationError("Permission denied", file_path)

        assert (
            str(error) == f"File operation error: Permission denied (file: {file_path})"
        )
        assert error.file_path == Path(file_path)
        assert error.operation is None

    def test_file_error_with_operation(self):
        """Test file operation error with operation."""
        error = FileOperationError("Write failed", operation="write")

        assert str(error) == "File operation error: Write failed (operation: write)"
        assert error.operation == "write"
        assert error.file_path is None

    def test_file_error_with_all_details(self):
        """Test file operation error with all details."""
        file_path = "/path/to/file.txt"
        error = FileOperationError("Write failed", file_path, "write")

        assert (
            str(error)
            == f"File operation error: Write failed (operation: write) (file: {file_path})"
        )
        assert error.file_path == Path(file_path)
        assert error.operation == "write"


class TestValidationError:
    """Test suite for ValidationError."""

    def test_validation_error_without_details(self):
        """Test validation error without field and value."""
        error = ValidationError("Invalid value")

        assert str(error) == "Validation error: Invalid value"
        assert error.field is None
        assert error.value is None

    def test_validation_error_with_field(self):
        """Test validation error with field."""
        error = ValidationError("Invalid value", field="username")

        assert str(error) == "Validation error: Invalid value (field: username)"
        assert error.field == "username"
        assert error.value is None

    def test_validation_error_with_value(self):
        """Test validation error with value."""
        error = ValidationError("Invalid value", value="test_value")

        assert str(error) == "Validation error: Invalid value (value: test_value)"
        assert error.value == "test_value"
        assert error.field is None

    def test_validation_error_with_all_details(self):
        """Test validation error with field and value."""
        error = ValidationError("Invalid email", field="email", value="invalid_email")

        assert (
            str(error)
            == "Validation error: Invalid email (field: email) (value: invalid_email)"
        )
        assert error.field == "email"
        assert error.value == "invalid_email"


class TestPermissionError:
    """Test suite for PermissionError."""

    def test_permission_error_without_resource(self):
        """Test permission error without resource."""
        error = PermissionError("Access denied")

        assert str(error) == "Permission error: Access denied"
        assert error.resource is None

    def test_permission_error_with_resource(self):
        """Test permission error with resource."""
        resource = "/path/to/protected/file"
        error = PermissionError("Access denied", resource)

        assert str(error) == f"Permission error: Access denied (resource: {resource})"
        assert error.resource == Path(resource)


class TestInstallerError:
    """Test suite for InstallerError."""

    def test_installer_error_without_step(self):
        """Test installer error without step."""
        error = InstallerError("Installation failed")

        assert str(error) == "Installer error: Installation failed"
        assert error.step is None

    def test_installer_error_with_step(self):
        """Test installer error with step."""
        error = InstallerError("Installation failed", step="download")

        assert str(error) == "Installer error: Installation failed (step: download)"
        assert error.step == "download"


class TestFetcherError:
    """Test suite for FetcherError."""

    def test_fetcher_error_without_url(self):
        """Test fetcher error without URL."""
        error = FetcherError("Fetch failed")

        assert str(error) == "Fetcher error: Fetch failed"
        assert error.url is None

    def test_fetcher_error_with_url(self):
        """Test fetcher error with URL."""
        url = "https://example.com/page"
        error = FetcherError("Fetch failed", url)

        assert str(error) == f"Fetcher error: Fetch failed (url: {url})"
        assert error.url == url


class TestRateLimitError:
    """Test suite for RateLimitError."""

    def test_rate_limit_error_without_details(self):
        """Test rate limit error without details."""
        error = RateLimitError("Too many requests")

        assert str(error) == "Network error: Too many requests"
        assert error.status_code == 429
        assert error.retry_after is None

    def test_rate_limit_error_with_url(self):
        """Test rate limit error with URL."""
        url = "https://example.com/api"
        error = RateLimitError("Too many requests", url)

        assert (
            str(error) == f"Network error: Too many requests (url: {url}) (status: 429)"
        )
        assert error.url == url
        assert error.status_code == 429
        assert error.retry_after is None

    def test_rate_limit_error_with_retry_after(self):
        """Test rate limit error with retry after."""
        error = RateLimitError("Too many requests", retry_after=60)

        assert str(error) == "Network error: Too many requests (status: 429)"
        assert error.retry_after == 60
        assert error.url is None

    def test_rate_limit_error_inheritance(self):
        """Test that rate limit error inherits from NetworkError."""
        error = RateLimitError("Too many requests")

        assert isinstance(error, NetworkError)
        assert isinstance(error, RateLimitError)


class TestTimeoutError:
    """Test suite for TimeoutError."""

    def test_timeout_error_without_details(self):
        """Test timeout error without details."""
        error = TimeoutError("Request timed out")

        assert str(error) == "Network error: Request timed out"
        assert error.timeout_seconds is None

    def test_timeout_error_with_url(self):
        """Test timeout error with URL."""
        url = "https://example.com/api"
        error = TimeoutError("Request timed out", url)

        assert str(error) == f"Network error: Request timed out (url: {url})"
        assert error.url == url
        assert error.timeout_seconds is None

    def test_timeout_error_with_timeout_seconds(self):
        """Test timeout error with timeout seconds."""
        error = TimeoutError("Request timed out", timeout_seconds=30.0)

        assert str(error) == "Network error: Request timed out"
        assert error.timeout_seconds == 30.0
        assert error.url is None

    def test_timeout_error_inheritance(self):
        """Test that timeout error inherits from NetworkError."""
        error = TimeoutError("Request timed out")

        assert isinstance(error, NetworkError)
        assert isinstance(error, TimeoutError)


class TestDocumentProcessingError:
    """Test suite for DocumentProcessingError."""

    def test_document_error_without_details(self):
        """Test document processing error without details."""
        error = DocumentProcessingError("Processing failed")

        assert str(error) == "Document processing error: Processing failed"
        assert error.document_path is None
        assert error.processing_step is None

    def test_document_error_with_document_path(self):
        """Test document processing error with document path."""
        doc_path = "/path/to/document.md"
        error = DocumentProcessingError("Processing failed", doc_path)

        assert (
            str(error)
            == f"Document processing error: Processing failed (document: {doc_path})"
        )
        assert error.document_path == Path(doc_path)
        assert error.processing_step is None

    def test_document_error_with_processing_step(self):
        """Test document processing error with processing step."""
        error = DocumentProcessingError(
            "Processing failed", processing_step="validation"
        )

        assert (
            str(error)
            == "Document processing error: Processing failed (step: validation)"
        )
        assert error.processing_step == "validation"
        assert error.document_path is None

    def test_document_error_with_all_details(self):
        """Test document processing error with all details."""
        doc_path = "/path/to/document.md"
        error = DocumentProcessingError("Processing failed", doc_path, "validation")

        assert (
            str(error)
            == f"Document processing error: Processing failed (step: validation) (document: {doc_path})"
        )
        assert error.document_path == Path(doc_path)
        assert error.processing_step == "validation"


class TestExceptionHierarchy:
    """Test suite for exception hierarchy."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all exceptions inherit from ClaudeCodeDocsError."""
        exceptions = [
            ConfigurationError,
            NetworkError,
            FileOperationError,
            ValidationError,
            PermissionError,
            InstallerError,
            FetcherError,
            RateLimitError,
            TimeoutError,
            DocumentProcessingError,
        ]

        for exception_class in exceptions:
            error = exception_class("Test message")
            assert isinstance(error, ClaudeCodeDocsError)
            assert isinstance(error, Exception)

    def test_network_error_hierarchy(self):
        """Test network error hierarchy."""
        network_errors = [RateLimitError, TimeoutError]

        for error_class in network_errors:
            error = error_class("Test message")
            assert isinstance(error, NetworkError)
            assert isinstance(error, ClaudeCodeDocsError)

    def test_exception_raising(self):
        """Test that exceptions can be raised and caught."""
        with pytest.raises(ClaudeCodeDocsError) as exc_info:
            raise ClaudeCodeDocsError("Test error")

        assert str(exc_info.value) == "Test error"
        assert exc_info.value.message == "Test error"

    def test_exception_chaining(self):
        """Test exception chaining."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise ConfigurationError("Configuration failed") from e
        except ConfigurationError as caught_error:
            assert caught_error.__cause__ is not None
            assert str(caught_error.__cause__) == "Original error"

    def test_exception_attributes(self):
        """Test that exception attributes are properly set."""
        error = ConfigurationError("Test error", "/path/to/config")
        assert (
            error.message == "Configuration error: Test error (file: /path/to/config)"
        )
        assert error.config_file == Path("/path/to/config")

    def test_exception_str_representation(self):
        """Test string representation of exceptions."""
        exceptions_and_messages = [
            (ClaudeCodeDocsError("Base error"), "Base error"),
            (ConfigurationError("Config error"), "Configuration error: Config error"),
            (NetworkError("Network error"), "Network error: Network error"),
            (FileOperationError("File error"), "File operation error: File error"),
            (ValidationError("Validation error"), "Validation error: Validation error"),
            (PermissionError("Permission error"), "Permission error: Permission error"),
            (InstallerError("Installer error"), "Installer error: Installer error"),
            (FetcherError("Fetcher error"), "Fetcher error: Fetcher error"),
            (
                DocumentProcessingError("Document error"),
                "Document processing error: Document error",
            ),
        ]

        for error, expected_message in exceptions_and_messages:
            assert str(error) == expected_message
