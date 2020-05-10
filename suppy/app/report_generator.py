import os
import json
from pathlib import Path
from distutils.dir_util import copy_tree
import webbrowser

class ReportGenerator:

    def __init__(self, report_namespace, stats):
        self._data_path = Path(__file__).parent / '../data'
        self._path_to_report = (self._data_path / ('tmp/export/' + report_namespace))
        self._path_to_template = (self._data_path / 'template')
        self._report_namespace = report_namespace
        self._stats = stats
        self._path_to_html = (self._path_to_report / 'report.html')


        os.mkdir(str(self._path_to_report.resolve()))
        copy_tree(str(self._path_to_template.resolve()), str(self._path_to_report.resolve()))

        json_data = json.dumps(stats, default=lambda o: o.__dict__, sort_keys=True)
        code = 'var data = \'' + json_data + '\';'

        json_path = (self._path_to_report / 'data.js').resolve()
        with open(json_path, 'w') as outfile:
            outfile.write(code)

        webbrowser.open_new(str(self._path_to_html.resolve()))