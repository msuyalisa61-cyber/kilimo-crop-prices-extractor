#!/usr/bin/env python3
"""
Script to organize and move multiple PDF files to a 'pdfs' folder.
"""

import os
import shutil
from pathlib import Path


def create_pdfs_folder(target_folder: str = "pdfs") -> str:
    """Create the target pdfs folder if it doesn't exist."""
    folder_path = Path(target_folder)
    folder_path.mkdir(exist_ok=True)
    print(f"✓ Created/verified folder: {target_folder}")
    return str(folder_path)


def find_pdf_files(source_directory: str = ".") -> list:
    """Find all PDF files in the source directory (non-recursive)."""
    source_path = Path(source_directory)
    pdf_files = list(source_path.glob("*.pdf"))
    print(f"✓ Found {len(pdf_files)} PDF file(s) in '{source_directory}'")
    return pdf_files


def find_pdf_files_recursive(source_directory: str = ".") -> list:
    """Find all PDF files in the source directory (recursive)."""
    source_path = Path(source_directory)
    pdf_files = list(source_path.rglob("*.pdf"))
    print(f"✓ Found {len(pdf_files)} PDF file(s) in '{source_directory}' (recursive)")
    return pdf_files


def move_pdfs_to_folder(pdf_files: list, target_folder: str = "pdfs") -> None:
    """Move PDF files to the target folder."""
    target_path = Path(target_folder)
    moved_count = 0
    
    for pdf_file in pdf_files:
        try:
            destination = target_path / pdf_file.name
            
            # Handle duplicate filenames
            if destination.exists():
                base_name = pdf_file.stem
                extension = pdf_file.suffix
                counter = 1
                while destination.exists():
                    destination = target_path / f"{base_name}_{counter}{extension}"
                    counter += 1
                print(f"  ⚠ Renamed duplicate: {pdf_file.name} → {destination.name}")
            
            shutil.move(str(pdf_file), str(destination))
            print(f"  ✓ Moved: {pdf_file.name}")
            moved_count += 1
        except Exception as e:
            print(f"  ✗ Error moving {pdf_file.name}: {e}")
    
    print(f"\n✓ Successfully moved {moved_count}/{len(pdf_files)} PDF files to '{target_folder}'")


def copy_pdfs_to_folder(pdf_files: list, target_folder: str = "pdfs") -> None:
    """Copy PDF files to the target folder (instead of moving)."""
    target_path = Path(target_folder)
    copied_count = 0
    
    for pdf_file in pdf_files:
        try:
            destination = target_path / pdf_file.name
            
            # Handle duplicate filenames
            if destination.exists():
                base_name = pdf_file.stem
                extension = pdf_file.suffix
                counter = 1
                while destination.exists():
                    destination = target_path / f"{base_name}_{counter}{extension}"
                    counter += 1
                print(f"  ⚠ Renamed duplicate: {pdf_file.name} → {destination.name}")
            
            shutil.copy2(str(pdf_file), str(destination))
            print(f"  ✓ Copied: {pdf_file.name}")
            copied_count += 1
        except Exception as e:
            print(f"  ✗ Error copying {pdf_file.name}: {e}")
    
    print(f"\n✓ Successfully copied {copied_count}/{len(pdf_files)} PDF files to '{target_folder}'")


def main():
    """Main function to organize PDFs."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Organize PDF files into a dedicated folder"
    )
    parser.add_argument(
        "--source",
        default=".",
        help="Source directory to search for PDFs (default: current directory)",
    )
    parser.add_argument(
        "--target",
        default="pdfs",
        help="Target folder name (default: pdfs)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy PDFs instead of moving them",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search for PDFs recursively in subdirectories",
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("PDF Organizer Script")
    print("=" * 60)
    
    # Create target folder
    create_pdfs_folder(args.target)
    
    # Find PDF files
    if args.recursive:
        pdf_files = find_pdf_files_recursive(args.source)
    else:
        pdf_files = find_pdf_files(args.source)
    
    if not pdf_files:
        print("No PDF files found. Exiting.")
        return
    
    # Move or copy PDFs
    if args.copy:
        copy_pdfs_to_folder(pdf_files, args.target)
    else:
        move_pdfs_to_folder(pdf_files, args.target)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
