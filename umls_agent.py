"""
UMLS RRF File Reader Agent
Reads and analyzes the MRDEF.RRF file to extract and display medical terminology data.
"""

import os
from collections import defaultdict
from typing import List, Dict, Tuple


class UMLSAgent:
    """Agent for reading and processing UMLS RRF format files."""
    
    def __init__(self, file_path: str):
        """Initialize the agent with the file path."""
        self.file_path = file_path
        self.concepts = defaultdict(list)
        self.total_records = 0
        self.languages = set()
        self.semantic_types = set()
        
    def read_file(self) -> bool:
        """Read and parse the RRF file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        self._parse_line(line.strip())
                        self.total_records += 1
                        
                        # Show progress every 100,000 records
                        if self.total_records % 100000 == 0:
                            print(f"[Progress] Processed {self.total_records:,} records...")
            
            return True
        except FileNotFoundError:
            print(f"Error: File not found - {self.file_path}")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    
    def _parse_line(self, line: str) -> None:
        """Parse a single RRF line."""
        fields = line.split('|')
        if len(fields) >= 5:
            cui = fields[0]           # Concept Unique Identifier
            aui = fields[1]           # Atom Unique Identifier
            attribute_id = fields[2]  # Attribute ID
            language_code = fields[4] # Language/Semantic Type Code
            attribute_value = fields[5] if len(fields) > 5 else ""  # Definition/Value
            
            self.concepts[cui].append({
                'aui': aui,
                'attribute_id': attribute_id,
                'language_code': language_code,
                'attribute_value': attribute_value[:100]  # First 100 chars
            })
            
            self.languages.add(language_code)
    
    def get_statistics(self) -> Dict:
        """Get statistics about the file."""
        return {
            'total_records': self.total_records,
            'unique_concepts': len(self.concepts),
            'languages': sorted(list(self.languages)),
            'language_count': len(self.languages),
            'average_records_per_concept': round(self.total_records / max(len(self.concepts), 1), 2)
        }
    
    def get_sample_records(self, limit: int = 5) -> List[Tuple[str, List]]:
        """Get sample records from the file."""
        items = list(self.concepts.items())[:limit]
        return items
    
    def print_report(self) -> None:
        """Print a comprehensive report of the file analysis."""
        print("\n" + "="*80)
        print("UMLS RRF FILE ANALYSIS REPORT")
        print("="*80)
        
        stats = self.get_statistics()
        
        print(f"\n📊 STATISTICS:")
        print(f"  • Total Records: {stats['total_records']:,}")
        print(f"  • Unique Concepts (CUIs): {stats['unique_concepts']:,}")
        print(f"  • Languages/Semantic Types: {stats['language_count']}")
        print(f"  • Average Records per Concept: {stats['average_records_per_concept']}")
        
        print(f"\n🌍 Languages/Semantic Types Detected:")
        for lang in stats['languages'][:20]:  # Show first 20
            print(f"  • {lang}")
        if len(stats['languages']) > 20:
            print(f"  • ... and {len(stats['languages']) - 20} more")
        
        print(f"\n📋 SAMPLE RECORDS (First 5 Concepts):")
        print("-" * 80)
        
        samples = self.get_sample_records(5)
        for idx, (cui, records) in enumerate(samples, 1):
            print(f"\n{idx}. Concept ID: {cui}")
            print(f"   Records: {len(records)}")
            if records:
                for i, record in enumerate(records[:3], 1):
                    print(f"   [{i}] Lang: {record['language_code']:<8} | {record['attribute_value'][:60]}...")
                if len(records) > 3:
                    print(f"   ... and {len(records) - 3} more records")
        
        print("\n" + "="*80)


def main():
    """Main execution function."""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'MRDEF.RRF')
    
    print(f"UMLS Agent - File Reader")
    print(f"Reading file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if not os.path.exists(file_path):
        print("Error: MRDEF.RRF file not found!")
        return
    
    # Create and run the agent
    agent = UMLSAgent(file_path)
    
    print("\n[Agent] Starting file analysis...")
    if agent.read_file():
        agent.print_report()
        print("\n✅ Agent completed successfully!")
    else:
        print("\n❌ Agent failed to process file")


if __name__ == "__main__":
    main()

