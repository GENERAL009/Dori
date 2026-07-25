from app.parsers.base import PrescriptionParser, ParsedPrescription, ParsedMedication


class GoogleVisionParser(PrescriptionParser):
    async def parse_image(self, image_path: str) -> ParsedPrescription:
        raise NotImplementedError("Google Vision parser not yet configured")

    async def parse_text(self, text: str) -> ParsedPrescription:
        raise NotImplementedError("Google Vision parser not yet configured")

    def get_provider_name(self) -> str:
        return "google_vision"


class OpenAIVisionParser(PrescriptionParser):
    async def parse_image(self, image_path: str) -> ParsedPrescription:
        raise NotImplementedError("OpenAI Vision parser not yet configured")

    async def parse_text(self, text: str) -> ParsedPrescription:
        raise NotImplementedError("OpenAI Vision parser not yet configured")

    def get_provider_name(self) -> str:
        return "openai_vision"


class ClaudeVisionParser(PrescriptionParser):
    async def parse_image(self, image_path: str) -> ParsedPrescription:
        raise NotImplementedError("Claude Vision parser not yet configured")

    async def parse_text(self, text: str) -> ParsedPrescription:
        raise NotImplementedError("Claude Vision parser not yet configured")

    def get_provider_name(self) -> str:
        return "claude_vision"


def get_parser(provider: str = "claude_vision") -> PrescriptionParser:
    parsers = {
        "google_vision": GoogleVisionParser,
        "openai_vision": OpenAIVisionParser,
        "claude_vision": ClaudeVisionParser,
    }
    parser_class = parsers.get(provider)
    if not parser_class:
        raise ValueError(f"Unknown parser provider: {provider}")
    return parser_class()
