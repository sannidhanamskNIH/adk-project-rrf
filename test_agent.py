#!/usr/bin/env python3
"""
Simple UMLS RRF File Reader Agent - Test Version
"""

def main():
    import os
    
    file_path = r"C:\Users\sannidhanamsk\workspace\git_lab\adk-project\MRDEF.RRF"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print("UMLS RRF File Agent - Starting Analysis")
    print(f"File: {file_path}")
    
    # Read and parse the file
    concepts = {}
    languages = set()
    total = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        print(f"Total lines in file: {len(lines):,}")
        
        # Parse first few lines
        for i, line in enumerate(lines[:10]):
            parts = line.strip().split('|')
            if len(parts) >= 5:
                cui = parts[0]
                lang = parts[4]
                languages.add(lang)
                if cui not in concepts:
                    concepts[cui] = []
                concepts[cui].append(parts)
                total += 1
        
        print(f"\nFirst 10 records parsed successfully")
        print(f"Unique concepts found: {len(concepts)}")
        print(f"Languages/Types found: {sorted(list(languages))}")
        
        print("\nSample Record:")
        for cui, records in list(concepts.items())[:1]:
            print(f"  CUI: {cui}")
            for rec in records[:2]:
                print(f"    {' | '.join(rec[:6])}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

