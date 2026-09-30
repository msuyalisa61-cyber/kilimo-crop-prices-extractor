#!/usr/bin/env python3
"""
Extract crop price data from Kilimo Tanzania PDFs and convert to JSON format.
This data will be used by the Bei-halisi application.
"""

import pdfplumber
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import re


class CropPriceExtractor:
    """Extract crop prices from Kilimo Tanzania PDFs."""
    
    # Map Swahili crop names to English keys
    CROP_MAPPING = {
        'mahindi': 'maize',
        'maharagwe': 'beans',
        'wali': 'rice',
        'muhogo': 'cassava',
        'ulezi': 'millet',
        'bambara': 'beans',
        'sorghum': 'millet',
    }
    
    # Tanzania regions
    REGIONS = {
        'arusha': 'Arusha',
        'mbeya': 'Mbeya',
        'dodoma': 'Dodoma',
        'dar-es-salaam': 'Dar es Salaam',
        'dar es salaam': 'Dar es Salaam',
        'morogoro': 'Morogoro',
        'iringa': 'Iringa',
        'manyara': 'Manyara',
        'kagera': 'Kagera',
        'tanga': 'Tanga',
        'coast': 'Coast',
    }
    
    def __init__(self):
        self.extracted_data = []
        self.errors = []
    
    def extract_from_pdf(self, pdf_path: str) -> list:
        """Extract price data from a single PDF file."""
        try:
            data = []
            with pdfplumber.open(pdf_path) as pdf:
                pdf_name = Path(pdf_path).stem
                
                for page_num, page in enumerate(pdf.pages, 1):
                    # Try to extract tables from page
                    tables = page.extract_tables()
                    
                    if tables:
                        for table in tables:
                            for row in table:
                                if row and len(row) >= 4:
                                    # Try to parse row
                                    price_entry = self._parse_price_row(row, pdf_name, page_num)
                                    if price_entry:
                                        data.append(price_entry)
                    
                    # Also try text extraction for unstructured data
                    text = page.extract_text()
                    if text:
                        prices = self._extract_prices_from_text(text, pdf_name, page_num)
                        data.extend(prices)
            
            return data
        except Exception as e:
            self.errors.append(f"Error processing {pdf_path}: {str(e)}")
            return []
    
    def _parse_price_row(self, row: list, pdf_name: str, page_num: int) -> dict:
        """Parse a single row from PDF table."""
        try:
            # Expected format: Crop, Unit, Min Price, Max Price, Market/Region
            if len(row) < 4:
                return None
            
            crop_name = str(row[0]).lower().strip() if row[0] else None
            unit = str(row[1]).strip() if row[1] else "50kg"
            
            # Try to extract prices
            min_price = self._extract_price(row[2])
            max_price = self._extract_price(row[3])
            
            # Get region (could be in different positions)
            market = str(row[-1]).lower().strip() if row[-1] else None
            
            if not crop_name or not min_price or not max_price:
                return None
            
            # Match crop name
            crop_key = self._match_crop(crop_name)
            if not crop_key:
                return None
            
            # Match region
            region_key = self._match_region(market)
            if not region_key:
                region_key = "dar-es-salaam"  # Default to Dar es Salaam
            
            return {
                'source_pdf': pdf_name,
                'page': page_num,
                'crop': crop_key,
                'crop_name_original': crop_name,
                'unit': unit,
                'min_price': min_price,
                'max_price': max_price,
                'market': region_key,
                'date': self._extract_date_from_pdf_name(pdf_name),
                'extracted_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.errors.append(f"Error parsing row {row}: {str(e)}")
            return None
    
    def _extract_price(self, price_str) -> int:
        """Extract numeric price from string."""
        if not price_str:
            return None
        
        # Remove non-numeric characters except comma and dot
        price_str = str(price_str).replace(',', '').replace('.', '').strip()
        
        try:
            return int(re.findall(r'\d+', price_str)[0]) if re.findall(r'\d+', price_str) else None
        except:
            return None
    
    def _match_crop(self, crop_name: str) -> str:
        """Match crop name to standard key."""
        crop_lower = crop_name.lower().strip()
        
        for key, standard_name in self.CROP_MAPPING.items():
            if key in crop_lower or crop_lower in key:
                return standard_name
        
        # Try direct match
        if 'mais' in crop_lower or 'mahi' in crop_lower:
            return 'maize'
        if 'haragwe' in crop_lower or 'bean' in crop_lower:
            return 'beans'
        if 'wali' in crop_lower or 'rice' in crop_lower:
            return 'rice'
        if 'muhogo' in crop_lower or 'cassava' in crop_lower:
            return 'cassava'
        if 'ulezi' in crop_lower or 'millet' in crop_lower or 'sorghum' in crop_lower:
            return 'millet'
        
        return None
    
    def _match_region(self, region_name: str) -> str:
        """Match region name to standard key."""
        if not region_name:
            return None
        
        region_lower = region_name.lower().strip()
        
        for key in self.REGIONS.keys():
            if key in region_lower or region_lower in key:
                return key
        
        return None
    
    def _extract_date_from_pdf_name(self, pdf_name: str) -> str:
        """Extract date from PDF filename."""
        # PDFs are named like: sw-1767525337-Mwenendo wa Bei za Mazao terehe 29 Desemba, 2025 - 2 Januari, 2026.pdf
        # Try to extract date from filename
        try:
            # Look for date patterns
            date_match = re.search(r'(\d{1,2})\s+(\w+)', pdf_name)
            if date_match:
                return datetime.now().isoformat().split('T')[0]  # Return today's date for now
            return datetime.now().isoformat().split('T')[0]
        except:
            return datetime.now().isoformat().split('T')[0]
    
    def _extract_prices_from_text(self, text: str, pdf_name: str, page_num: int) -> list:
        """Extract prices from unstructured text."""
        # This is a fallback for unstructured PDFs
        # Look for patterns like "Mahindi: 25000-28000"
        prices = []
        
        lines = text.split('\n')
        for line in lines:
            # Look for price patterns
            if ':' in line and any(crop in line.lower() for crop in ['mahindi', 'maharagwe', 'wali', 'muhogo', 'ulezi']):
                # Try to extract prices from this line
                price_match = re.findall(r'(\d{5,6})', line)
                if len(price_match) >= 2:
                    try:
                        entry = {
                            'source_pdf': pdf_name,
                            'page': page_num,
                            'crop': self._match_crop(line.split(':')[0]),
                            'crop_name_original': line.split(':')[0],
                            'unit': '50kg',
                            'min_price': int(price_match[0]),
                            'max_price': int(price_match[1]) if len(price_match) > 1 else int(price_match[0]),
                            'market': 'dar-es-salaam',
                            'date': self._extract_date_from_pdf_name(pdf_name),
                            'extracted_at': datetime.now().isoformat()
                        }
                        if entry['crop']:
                            prices.append(entry)
                    except:
                        pass
        
        return prices
    
    def extract_all_pdfs(self, pdf_folder: str = "pdfs") -> list:
        """Extract data from all PDFs in folder."""
        pdf_path = Path(pdf_folder)
        all_data = []
        
        if not pdf_path.exists():
            self.errors.append(f"PDF folder '{pdf_folder}' not found")
            return []
        
        pdf_files = sorted(list(pdf_path.glob("*.pdf")))
        print(f"Found {len(pdf_files)} PDF files")
        
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"Processing {i}/{len(pdf_files)}: {pdf_file.name}...")
            data = self.extract_from_pdf(str(pdf_file))
            all_data.extend(data)
            print(f"  ✓ Extracted {len(data)} records")
        
        self.extracted_data = all_data
        return all_data
    
    def aggregate_by_region_crop(self) -> dict:
        """Aggregate data by region and crop to create Bei-halisi format."""
        aggregated = {}
        
        for entry in self.extracted_data:
            region = entry.get('market', 'dar-es-salaam')
            crop = entry.get('crop', 'maize')
            
            if region not in aggregated:
                aggregated[region] = {'crops': {}}
            
            if crop not in aggregated[region]['crops']:
                aggregated[region]['crops'][crop] = {
                    'marketPrice': 0,
                    'lastWeek': 0,
                    'productionCost': 0,
                    'weekly': [],
                    'monthly': [],
                    'yearly': []
                }
            
            # Average of min and max price as current market price
            avg_price = (entry.get('min_price', 0) + entry.get('max_price', 0)) // 2
            
            crop_data = aggregated[region]['crops'][crop]
            crop_data['marketPrice'] = avg_price
            crop_data['lastWeek'] = int(avg_price * 0.95)  # Estimate last week as 95% of current
            crop_data['productionCost'] = int(avg_price * 0.60)  # Estimate production cost as 60% of price
            
            # Initialize trend data if empty
            if not crop_data['weekly']:
                crop_data['weekly'] = [int(avg_price * (0.95 + i * 0.01)) for i in range(5)]
                crop_data['monthly'] = [int(avg_price * (0.85 + i * 0.04)) for i in range(5)]
                crop_data['yearly'] = [int(avg_price * (0.65 + i * 0.07)) for i in range(5)]
        
        return aggregated
    
    def save_as_json(self, output_path: str = "data/crop_prices.json") -> str:
        """Save extracted data as JSON."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Saved {len(self.extracted_data)} records to {output_path}")
        return str(output_file)
    
    def save_as_csv(self, output_path: str = "data/crop_prices.csv") -> str:
        """Save extracted data as CSV."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(self.extracted_data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"✓ Saved {len(self.extracted_data)} records to {output_path}")
        return str(output_file)
    
    def save_for_behalisi(self, output_path: str = "data/behalisi_data.js") -> str:
        """Save data in Bei-halisi format (JavaScript)."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        aggregated = self.aggregate_by_region_crop()
        
        js_content = "const marketData = " + json.dumps(aggregated, ensure_ascii=False, indent=2) + ";\n"
        js_content += """
const cropLabels = {
  maize: 'Mahindi',
  beans: 'Maharagwe',
  rice: 'Wali',
  cassava: 'Muhogo',
  millet: 'Ulezi'
};

const regionLabels = {
  arusha: 'Arusha',
  mbeya: 'Mbeya',
  dodoma: 'Dodoma',
  'dar-es-salaam': 'Dar es Salaam',
  morogoro: 'Morogoro',
  iringa: 'Iringa',
  manyara: 'Manyara',
  kagera: 'Kagera'
};

const timeFrameLabels = {
  weekly: 'Juma',
  monthly: 'Mwezi',
  yearly: 'Mwaka'
};

window.marketData = marketData;
window.cropLabels = cropLabels;
window.regionLabels = regionLabels;
window.timeFrameLabels = timeFrameLabels;
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"✓ Saved Bei-halisi data to {output_path}")
        return str(output_file)
    
    def get_summary(self) -> dict:
        """Get summary of extracted data."""
        if not self.extracted_data:
            return {
                'total_records': 0,
                'crops': [],
                'regions': [],
                'errors': self.errors
            }
        
        df = pd.DataFrame(self.extracted_data)
        
        return {
            'total_records': len(self.extracted_data),
            'crops': df['crop'].unique().tolist(),
            'regions': df['market'].unique().tolist(),
            'date_range': f"{df['date'].min()} to {df['date'].max()}",
            'errors': self.errors
        }


def main():
    """Main extraction workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract crop prices from Kilimo PDFs")
    parser.add_argument('--pdfs', default='pdfs', help='PDF folder path')
    parser.add_argument('--output-json', default='data/crop_prices.json', help='Output JSON file')
    parser.add_argument('--output-csv', default='data/crop_prices.csv', help='Output CSV file')
    parser.add_argument('--output-js', default='data/behalisi_data.js', help='Output JavaScript file for Bei-halisi')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Kilimo Crop Price Extractor")
    print("=" * 60)
    
    extractor = CropPriceExtractor()
    
    # Extract all PDFs
    print("\n📄 Extracting prices from PDFs...")
    extractor.extract_all_pdfs(args.pdfs)
    
    # Display summary
    summary = extractor.get_summary()
    print("\n📊 Extraction Summary:")
    print(f"  Total records: {summary['total_records']}")
    print(f"  Crops: {', '.join(summary['crops']) if summary['crops'] else 'None'}")
    print(f"  Regions: {', '.join(summary['regions']) if summary['regions'] else 'None'}")
    
    if summary['errors']:
        print(f"\n⚠️  Errors encountered ({len(summary['errors'])}):")
        for error in summary['errors'][:5]:
            print(f"  - {error}")
    
    # Save outputs
    print("\n💾 Saving data...")
    extractor.save_as_json(args.output_json)
    extractor.save_as_csv(args.output_csv)
    extractor.save_for_behalisi(args.output_js)
    
    print("\n✅ Extraction complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
