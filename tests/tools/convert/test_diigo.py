from pathlib import Path

from tagmark.tools.convert.diigo import ExportedChromeFormatConverter, ExportedCsvFormatConverter


class TestExportedCsvFormatConverter:
    csv_format_converter: ExportedCsvFormatConverter = ExportedCsvFormatConverter()
    test_file: Path = Path("tests/data/16400249_csv_2023_04_18_dc9ef.csv")

    def test_load_items(
        self,
    ):
        for item in self.csv_format_converter.load_original_items(data_source=self.test_file):
            assert item.get("url")


class TestExportedChromeFormatConverter:
    chrome_format_converter: ExportedChromeFormatConverter = ExportedChromeFormatConverter()
    test_file: Path = Path("tests/data/16400249_chrome_2023_04_18_b776d.html")

    def test_load_items(
        self,
    ):
        for item in self.chrome_format_converter.load_original_items(
            data_source=self.test_file
        ):
            assert item.get("href")

    def test_convert(self):
        items: list[dict] = self.chrome_format_converter.load_original_items(
            data_source=self.test_file
        )
        self.chrome_format_converter.convert_to_tagmark(items=items)
        for _tagmark_item in self.chrome_format_converter.tagmark.tagmark_items:
            assert _tagmark_item.url
            assert _tagmark_item.time_added
        assert self.chrome_format_converter.tagmark.tagmark_items[1].comment
        assert self.chrome_format_converter.tagmark.tagmark_items[1].title
