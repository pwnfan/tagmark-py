from pathlib import Path

from tagmark.tools.convert.diigo import CsvConverter, ChromeConverter


class TestCsvConverter:
    csv_converter: CsvConverter = CsvConverter()
    test_file: Path = Path("tests/data/16400249_csv_2023_04_18_dc9ef.csv")

    def test_load_items(
        self,
    ):
        for item in self.csv_converter.load_original_items(data_source=self.test_file):
            assert item.get("url")


class TestChromeConverter:
    chrome_converter: ChromeConverter = ChromeConverter()
    test_file: Path = Path("tests/data/16400249_chrome_2023_04_18_b776d.html")

    def test_load_items(
        self,
    ):
        for item in self.chrome_converter.load_original_items(data_source=self.test_file):
            assert item.get("href")

    def test_convert(self):
        items: list[dict] = self.chrome_converter.load_original_items(data_source=self.test_file)
        self.chrome_converter.convert_to_tagmark(items=items)
        for _tagmark_item in self.chrome_converter.tagmark.tagmark_items:
            assert _tagmark_item.url
            assert _tagmark_item.time_added
        assert self.chrome_converter.tagmark.tagmark_items[1].comment
        assert self.chrome_converter.tagmark.tagmark_items[1].title
