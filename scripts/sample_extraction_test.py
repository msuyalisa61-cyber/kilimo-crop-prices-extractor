"""
Sample test script to verify extraction works correctly
"""

import json
from extract_crop_prices import CropPriceExtractor


def create_sample_data():
    extractor = CropPriceExtractor()
    extractor.extracted_data = [
        {
            'source_pdf': 'kilimo_august_2024',
            'page': 1,
            'extracted_at': '2024-08-15T10:30:00',
            'data': {
                'Crop': 'Maize',
                'Variety': 'White',
                'Unit': '50kg',
                'Min Price': '25000',
                'Max Price': '28000',
                'Market': 'Dar es Salaam',
                'Date': '2024-08-15'
            }
        }
    ]
    return extractor


def test_extraction():
    extractor = create_sample_data()
    json_file = extractor.save_as_json('data/json/test_sample.json')
    csv_file = extractor.save_as_csv('data/csv/test_sample.csv')
    print('JSON:', json_file)
    print('CSV:', csv_file)
    print('Summary:', extractor.get_summary())


if __name__ == '__main__':
    test_extraction()
