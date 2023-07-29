from tagmark.tools.convert.tagmark import JsonLinesConverter


class TestJsonlinesConverter:
    jsonlines_converter: JsonLinesConverter = JsonLinesConverter()

    def test_load_items(self, test_input_file_paths):
        for item in self.jsonlines_converter.load_original_items(
            data_source=test_input_file_paths["tagmark_data_json"]
        ):
            assert item.get("url")

    def test_convert(self, test_input_file_paths):
        items: list[dict] = self.jsonlines_converter.load_original_items(
            data_source=test_input_file_paths["tagmark_data_json"]
        )
        self.jsonlines_converter.convert_to_tagmark(items=items)
        for _tagmark_item in self.jsonlines_converter.tagmark.tagmark_items:
            assert _tagmark_item.url
