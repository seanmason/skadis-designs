"""Fusion entry point for the complete v0.2 assembly and exports.
Creates a new document; does not alter other open documents.
For panel library variants, run ExportPanelLibraryV02.py afterward.
"""
import os,runpy

def run(_context: str):
    folder=os.path.dirname(os.path.abspath(__file__))
    for filename in ['FrameSystemV02.py','CompleteFrameV02.py','WallBracketsV02.py','ValidateFrameV02.py','CheckInterferenceV02.py','ExportFrameV02.py','FinalHealthV02.py']:
        print('Running '+filename)
        runpy.run_path(os.path.join(folder,filename))['run'](_context)
