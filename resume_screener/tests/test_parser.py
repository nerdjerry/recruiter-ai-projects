from __future__ import annotations

import pytest

from app.services.parser import BaseParser, DocxParser, ParserFactory, PdfParser


class TestParserFactory:
    def test_returns_pdf_parser_for_pdf(self) -> None:
        parser = ParserFactory.get_parser("resume.pdf")
        assert isinstance(parser, PdfParser)

    def test_returns_docx_parser_for_docx(self) -> None:
        parser = ParserFactory.get_parser("resume.docx")
        assert isinstance(parser, DocxParser)

    def test_raises_for_unsupported_extension(self) -> None:
        with pytest.raises(ValueError, match="Unsupported file type"):
            ParserFactory.get_parser("resume.txt")

    def test_case_insensitive_extension(self) -> None:
        parser = ParserFactory.get_parser("Resume.PDF")
        assert isinstance(parser, PdfParser)


class TestBaseParser:
    def test_cannot_instantiate_abstract_class(self) -> None:
        with pytest.raises(TypeError):
            BaseParser()  # type: ignore[abstract]


class TestParserFactoryRegister:
    def test_register_new_parser(self) -> None:
        class TxtParser(BaseParser):
            def parse(self, file_bytes: bytes, filename: str) -> str:
                return file_bytes.decode("utf-8")

        ParserFactory.register(".txt", TxtParser)
        parser = ParserFactory.get_parser("notes.txt")
        assert isinstance(parser, TxtParser)
        assert parser.parse(b"hello", "notes.txt") == "hello"

        # Cleanup: remove the registered parser so other tests aren't affected
        ParserFactory._parsers.pop(".txt", None)
