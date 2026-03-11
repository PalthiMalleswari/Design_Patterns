# Reference - https://algomaster.io/learn/lld/template-method

# Problem - Exporting Reports
"""
Let’s say you’re building an analytics platform that lets users export reports in different formats.
Right now, the product needs CSV and PDF support, with Excel coming soon.

Each exporter follows the same high-level workflow:

Prepare Data: Gather and organize the report data.
Open File: Create the output file in the target format.
Write Header: Output column headers or metadata (format-specific).
Write Data Rows: Iterate through the dataset and write each row (format-specific).
Write Footer: Add optional summary or footer information.
Close File: Finalize and close the output file.
"""

# Naive Implementation

class ReportData:
    def get_headers(self):
        return ["ID", "Name", "Value"]
    
    def get_rows(self):
        return [
            {"ID": 1, "Name": "Item A", "Value": 100.0},
            {"ID": 2, "Name": "Item B", "Value": 150.5},
            {"ID": 3, "Name": "Item C", "Value": 75.25}
        ]

class CSVExporterNaive:

    def export(self,data:ReportData,file_path):

        print("CSV Exporter: Preparing data (common)...")
        # ... data preparation logic ...

        print(f"CSV Exporter: Opening file '{file_path}.csv' (common)...")
        # ... file opening logic ...

        print("CSV Exporter: Writing CSV header (specific)...")
        # ",".join(data.get_headers())
        # ... write header to file ...

        print("CSV Exporter: Writing CSV data rows (specific)...")
        # for row in data.get_rows(): ... format and write row ...

        print("CSV Exporter: Writing CSV footer (if any) (common)...")

        print(f"CSV Exporter: Closing file '{file_path}.csv' (common)...")
        # ... file closing logic ...
        print(f"CSV Report exported to {file_path}.csv")

class PdfReportExporterNaive:
    def export(self, data, file_path):
        print("PDF Exporter: Preparing data (common)...")
        # ... data preparation logic ...

        print(f"PDF Exporter: Opening file '{file_path}.pdf' (common)...")
        # ... PDF library specific file opening ...

        print("PDF Exporter: Writing PDF header (specific)...")
        # ... PDF library specific header writing ...

        print("PDF Exporter: Writing PDF data rows (specific)...")
        # ... PDF library specific data row writing ...

        print("PDF Exporter: Writing PDF footer (if any) (common)...")

        print(f"PDF Exporter: Closing file '{file_path}.pdf' (common)...")
        # ... PDF library specific file closing ...
        print(f"PDF Report exported to {file_path}.pdf")

# Problems With This Design

"""
1. Code Duplication : Common Logic like gathering data,opening a specific file type,closing a file
2. Poor Extensibility : Adding New Type Needs to implement all the common logic again rather performing it's spefic actions
3. Maintainance Overhead : Lets say user want to log before writing data, for this we need to modify in all the Child classes, leads to overhead
4. Inconsistent Behaviour : If each type is a independent class then there might be chances the deveoper may miss few steps leads to unexpected results
"""


# =========================== Template Method =====================
# The Method pattern defines the skeleton of an algorithm in a method, deferring some steps to subclasses.
# It allows you to keep the overall structure of the process consistent, while giving subclasses the flexibility to customize specific parts of the algorithm.

"""
Characterstics:
1. Algorithm skelton in the base class: The base class contains a method (the template method) that defines the sequence of steps.
2. Subclasses override specific steps: The base class declares abstract methods for the steps that vary. Subclasses implement
 these methods to provide format-specific or context-specific behavior, 
"""  
from abc import ABC,abstractmethod

# Abstract Class

class AbstractReportExporter:

    def template(self,data,file_path):
        self.prepare_data(data)
        file = self.open_file(file_path)
        # print(file)
        self.write_header(file,data)
        self.write_data_rows(file,data)
        self.write_footer(file,data)
        self.close_file(file)
        print(f"Export Completed for {file}")
    
    def prepare_data(self,data):
        print("Preparing Data for Report, Remove Unnecessary Info and Normalize")
    
    def open_file(self,file_path):
        print(f"Opening a File From Path: {file_path}")
        return "Test"
    
    @abstractmethod
    def write_header(self,file,data):
        pass

    @abstractmethod
    def write_data_rows(self,file,data):
        pass
    
    # Hook method - optional override with sensible default
    def write_footer(self,file,data):
        print(f"Adding Footer to file : {file}")
    
    def close_file(self,file):
        print(f"Closing {file} file")

class CSVExporter(AbstractReportExporter):

    def write_header(self, file, data):
        print(f"Adding Header to CSV File - {file}")
        print("CSV Header: "+",".join(data.get_headers()))
    
    def write_data_rows(self, file,data):
        for row in data.get_rows():
            values = [str(row[h]) for h in data.get_headers()]
            print("CSV: " + ",".join(values))

class PdfReportExporter(AbstractReportExporter):
    def write_header(self, file, data):
        print("PDF: | " + " | ".join(data.get_headers()) + " |")
        print("PDF: " + "-" * 40)

    def write_data_rows(self, file,data):
        for row in data.get_rows():
            values = [str(row[h]) for h in data.get_headers()]
            print("PDF: | " + " | ".join(values) + " |")

    def write_footer(self, file, data):

        print(f"{file}.PDF: --- Page 1 of 1 ---")

data = ReportData()
csv_export = CSVExporter()
csv_export.template(data,"Home/Downloads")
print("\n-----------------------------------------")
pdf_exporter = PdfReportExporter()
pdf_exporter.template(data,"Home/Documents")

"""
| Template Method           | Strategy                        |
| ------------------------- | ------------------------------- |
| Algorithm skeleton fixed  | Algorithm interchangeable       |
| Uses inheritance          | Uses composition                |
| Compile time behavior     | Runtime behavior                |
| Frameworks use it heavily | Systems with dynamic algorithms |

Ask yourself: Is the algorithm structure fixed?
If yes → Template Method
Is the algorithm interchangeable?
If yes → Strategy
🚀 Final Takeaway :: 
Template Method is heavily used in frameworks because:
Framework wants to control flow, but allow developers to customize steps.

"""
