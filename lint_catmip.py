#!/usr/bin/env python3
"""
CAT-MIP Terms JSON Linter

Validates the structure and content of the terms.json file to ensure
consistency and compliance with CAT-MIP standards.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
import re
from collections import defaultdict


class CATMIPLinter:
    """Linter for CAT-MIP terms.json file"""
    
    REQUIRED_FIELDS = {
        'id', 'canonical_term', 'definition', 'metadata'
    }
    
    OPTIONAL_FIELDS = {
        'synonyms', 'relationships', 'prompt_examples', 
        'agent_execution', 'recommendation', 'term_type'
    }
    
    METADATA_REQUIRED_FIELDS = {
        'author', 'version', 'date_added', 'registry'
    }
    
    METADATA_OPTIONAL_FIELDS = {
        'source_url', 'term_type'
    }
    
    RELATIONSHIP_PATTERNS = [
        r'^\w+\s+(belongsTo|isConnectedTo|isManagedBy|isInstalledOn|executes|reportsTo|monitors|enables|isExposedBy|isCalledBy|interprets|calls|isPartnerOf|paysFor|isMonitoredFor|serves|broadcasts|enforces)\s+.+',
    ]
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.terms_data: Optional[List[Dict]] = None
        
    def load_json(self) -> bool:
        """Load and parse the JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.terms_data = json.loads(content)
                
            if not isinstance(self.terms_data, list):
                self.errors.append("Root element must be an array")
                return False
                
            self.info.append(f"Successfully loaded {len(self.terms_data)} terms")
            return True
            
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.file_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON parsing error at line {e.lineno}, column {e.colno}: {e.msg}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error loading file: {str(e)}")
            return False
    
    def validate_structure(self) -> None:
        """Validate the structure of each term"""
        if not self.terms_data:
            return
            
        canonical_terms = set()
        ids = set()
        
        for idx, term in enumerate(self.terms_data):
            term_id = f"Term {idx + 1}"
            
            if 'canonical_term' in term:
                term_id = f"'{term['canonical_term']}' (index {idx})"
            
            # Check for required fields
            missing_fields = self.REQUIRED_FIELDS - set(term.keys())
            if missing_fields:
                self.errors.append(f"{term_id}: Missing required fields: {', '.join(missing_fields)}")
            
            # Check for unknown fields
            all_allowed_fields = self.REQUIRED_FIELDS | self.OPTIONAL_FIELDS
            unknown_fields = set(term.keys()) - all_allowed_fields
            if unknown_fields:
                self.warnings.append(f"{term_id}: Unknown fields: {', '.join(unknown_fields)}")
            
            # Validate ID uniqueness
            if 'id' in term:
                if term['id'] in ids:
                    self.errors.append(f"{term_id}: Duplicate ID '{term['id']}'")
                ids.add(term['id'])
            
            # Validate canonical term uniqueness
            if 'canonical_term' in term:
                if term['canonical_term'] in canonical_terms:
                    self.errors.append(f"{term_id}: Duplicate canonical term '{term['canonical_term']}'")
                canonical_terms.add(term['canonical_term'])
                
                # Check canonical term format
                if not re.match(r'^[A-Z]', term['canonical_term']):
                    self.warnings.append(f"{term_id}: Canonical term should start with capital letter")
    
    def validate_metadata(self) -> None:
        """Validate metadata fields"""
        if not self.terms_data:
            return
            
        for idx, term in enumerate(self.terms_data):
            if 'canonical_term' not in term:
                continue
                
            term_id = f"'{term['canonical_term']}'"
            
            if 'metadata' not in term:
                continue
                
            metadata = term['metadata']
            
            # Check required metadata fields
            missing_meta = self.METADATA_REQUIRED_FIELDS - set(metadata.keys())
            if missing_meta:
                self.errors.append(f"{term_id}: Missing required metadata fields: {', '.join(missing_meta)}")
            
            # Validate date format
            if 'date_added' in metadata:
                try:
                    datetime.fromisoformat(metadata['date_added'].replace('Z', '+00:00'))
                except ValueError:
                    self.errors.append(f"{term_id}: Invalid date format in metadata.date_added")
            
            # Validate version format
            if 'version' in metadata:
                if not re.match(r'^\d+\.\d+$', str(metadata['version'])):
                    self.warnings.append(f"{term_id}: Version should be in format X.Y")
            
            # Check registry value
            if 'registry' in metadata and metadata['registry'] != 'cat-mip.org':
                self.warnings.append(f"{term_id}: Non-standard registry value '{metadata['registry']}'")
    
    def validate_relationships(self) -> None:
        """Validate relationship formats"""
        if not self.terms_data:
            return
            
        for idx, term in enumerate(self.terms_data):
            if 'canonical_term' not in term:
                continue
                
            term_id = f"'{term['canonical_term']}'"
            
            if 'relationships' not in term:
                continue
                
            relationships = term.get('relationships', [])
            if not isinstance(relationships, list):
                self.errors.append(f"{term_id}: Relationships must be a list")
                continue
                
            for rel_idx, relationship in enumerate(relationships):
                if not isinstance(relationship, str):
                    self.errors.append(f"{term_id}: Relationship {rel_idx + 1} must be a string")
                    continue
                    
                # Check if relationship follows expected patterns
                valid = any(re.match(pattern, relationship) for pattern in self.RELATIONSHIP_PATTERNS)
                if not valid and not relationship.startswith('Monitor ') and not relationship.startswith('Locate '):
                    self.warnings.append(f"{term_id}: Relationship '{relationship[:50]}...' doesn't follow standard pattern")
    
    def validate_content_quality(self) -> None:
        """Validate content quality and consistency"""
        if not self.terms_data:
            return
            
        for idx, term in enumerate(self.terms_data):
            if 'canonical_term' not in term:
                continue
                
            term_id = f"'{term['canonical_term']}'"
            
            # Check definition quality
            if 'definition' in term:
                definition = term['definition']
                if len(definition) < 50:
                    self.warnings.append(f"{term_id}: Definition seems too short ({len(definition)} chars)")
                if len(definition) > 2000:
                    self.warnings.append(f"{term_id}: Definition is very long ({len(definition)} chars)")
                if not definition[0].isupper():
                    self.warnings.append(f"{term_id}: Definition should start with capital letter")
                if not definition.rstrip().endswith('.'):
                    self.warnings.append(f"{term_id}: Definition should end with period")
            
            # Check for empty lists
            for field in ['synonyms', 'relationships', 'prompt_examples']:
                if field in term and isinstance(term[field], list) and len(term[field]) == 0:
                    self.warnings.append(f"{term_id}: Empty {field} list")
            
            # Check agent_execution structure
            if 'agent_execution' in term:
                exec_data = term['agent_execution']
                if not isinstance(exec_data, dict):
                    self.errors.append(f"{term_id}: agent_execution must be an object")
                elif 'interpretation' not in exec_data and 'actions' not in exec_data:
                    self.warnings.append(f"{term_id}: agent_execution should contain 'interpretation' or 'actions'")
    
    def check_cross_references(self) -> None:
        """Check for cross-references between terms"""
        if not self.terms_data:
            return
            
        # Build a set of all canonical terms
        canonical_terms = {term['canonical_term'] for term in self.terms_data if 'canonical_term' in term}
        
        for term in self.terms_data:
            if 'canonical_term' not in term:
                continue
                
            term_id = f"'{term['canonical_term']}'"
            
            # Check relationships reference valid terms
            for relationship in term.get('relationships', []):
                # Extract referenced terms from relationships
                words = relationship.split()
                for word in words:
                    clean_word = word.strip('(),.')
                    if clean_word in canonical_terms and clean_word != term['canonical_term']:
                        self.info.append(f"{term_id}: References '{clean_word}' in relationships")
    
    def generate_stats(self) -> Dict[str, Any]:
        """Generate statistics about the terms"""
        if not self.terms_data:
            return {}
            
        stats = {
            'total_terms': len(self.terms_data),
            'authors': defaultdict(int),
            'terms_with_synonyms': 0,
            'terms_with_relationships': 0,
            'terms_with_examples': 0,
            'terms_with_execution': 0,
            'average_definition_length': 0,
            'total_synonyms': 0,
            'total_relationships': 0,
        }
        
        definition_lengths = []
        
        for term in self.terms_data:
            # Count by author
            if 'metadata' in term and 'author' in term['metadata']:
                stats['authors'][term['metadata']['author']] += 1
            
            # Count features
            if term.get('synonyms'):
                stats['terms_with_synonyms'] += 1
                stats['total_synonyms'] += len(term['synonyms'])
            
            if term.get('relationships'):
                stats['terms_with_relationships'] += 1
                stats['total_relationships'] += len(term['relationships'])
            
            if term.get('prompt_examples'):
                stats['terms_with_examples'] += 1
            
            if term.get('agent_execution'):
                stats['terms_with_execution'] += 1
            
            if 'definition' in term:
                definition_lengths.append(len(term['definition']))
        
        if definition_lengths:
            stats['average_definition_length'] = sum(definition_lengths) // len(definition_lengths)
        
        return stats
    
    def run(self) -> Tuple[bool, Dict[str, Any]]:
        """Run all validation checks"""
        # Load the JSON file
        if not self.load_json():
            return False, {}
        
        # Run all validations
        self.validate_structure()
        self.validate_metadata()
        self.validate_relationships()
        self.validate_content_quality()
        self.check_cross_references()
        
        # Generate statistics
        stats = self.generate_stats()
        
        # Determine success
        success = len(self.errors) == 0
        
        return success, stats
    
    def print_results(self) -> None:
        """Print validation results"""
        print("=" * 60)
        print("CAT-MIP Terms Linter Results")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10 warnings
                print(f"  • {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")
        
        if self.info and len(self.errors) == 0:
            print(f"\nℹ️  INFO ({len(self.info)}):")
            for info in self.info[:5]:  # Show first 5 info messages
                print(f"  • {info}")
            if len(self.info) > 5:
                print(f"  ... and {len(self.info) - 5} more info messages")
        
        print("\n" + "=" * 60)
        
        if self.errors:
            print("❌ Validation FAILED")
        else:
            print("✅ Validation PASSED")
        
        print("=" * 60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Lint CAT-MIP terms.json file')
    parser.add_argument('file', nargs='?', default='terms.json',
                       help='Path to terms.json file (default: terms.json)')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics about the terms')
    parser.add_argument('--quiet', action='store_true',
                       help='Only show errors')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Create and run linter
    linter = CATMIPLinter(args.file)
    success, stats = linter.run()
    
    if args.json:
        # Output as JSON
        output = {
            'success': success,
            'errors': linter.errors,
            'warnings': linter.warnings,
            'info': linter.info,
            'stats': stats
        }
        print(json.dumps(output, indent=2))
    else:
        # Output as text
        if not args.quiet or linter.errors:
            linter.print_results()
        
        if args.stats and stats:
            print("\n📊 STATISTICS:")
            print(f"  Total terms: {stats['total_terms']}")
            print(f"  Terms with synonyms: {stats['terms_with_synonyms']}")
            print(f"  Terms with relationships: {stats['terms_with_relationships']}")
            print(f"  Terms with examples: {stats['terms_with_examples']}")
            print(f"  Terms with agent execution: {stats['terms_with_execution']}")
            print(f"  Total synonyms: {stats['total_synonyms']}")
            print(f"  Total relationships: {stats['total_relationships']}")
            print(f"  Average definition length: {stats['average_definition_length']} chars")
            print("\n  Authors:")
            for author, count in stats['authors'].items():
                print(f"    • {author}: {count} terms")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()