# -*- coding: utf-8 -*-

import json
import os

# {
#     'args':           required, list of strings,  args array
#     'returncode':     required, int,              expected return code
#     'setup':          optional, lambda,           callable for setup
#     'teardown':       optional, lambda,           callable for teardown
#     'description':    optional, string,           description sentence starting with 'should'
#     'stdout':         optional, string,           expected stdout
#     'stderr':         optional, string,           expected stderr
#     'stdlog':         optional, list of 3-tuples, expected log statements
# },
tests = [
    {
        'description': 'should fail and print usage by default',
        'args': [],
        'returncode': 2
    },
    {
        'description': 'should print help with -h flag',
        'args': ['-h'],
        'returncode': 0,
        'stderr': '',
        'stdlog': None,
    },
    {
        'description': 'should print help with --help flag',
        'args': ['--help'],
        'returncode': 0,
        'stderr': '',
        'stdlog': None,
    },
    {
        'args': ['./static'],
        'returncode': 0,
        'stderr': '',
        'stdlog': None,
    },
    {
        'description': 'should return 22 whenever a non-existing path is provided mixed with existing',
        'args': ['./static', 'moogoescow'],
        'returncode': 22,
        'stdout': None,
        'stdlog': [
            ('fdedup', 'ERROR', '[Errno 2] No such file or directory: \'moogoescow\'')
        ],
    },
    {
        'description': 'should return 22 whenever a non-existing path is provided',
        'args': ['moogoescow'],
        'returncode': 22,
        'stdout': None,
        'stdlog': [('fdedup', 'ERROR', '[Errno 2] No such file or directory: \'moogoescow\'')]
    },
    {
        'description': 'should return 22 whenever a non-existing path is provided and quiet is set',
        'args': ['--quiet', 'moogoescow'],
        'returncode': 22,
        'stdout': '',
        'stderr': '',
        'stdlog': None
    },
    {
        'args': ['--json', 'static/chaplain', 'static/chaplain.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/chaplain', 'static/chaplain.copy']
        ]),
        'stderr': '',
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/chaplain', 'static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stderr': '',
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/chaplain', 'static/chaplain.copy', 'static/chaplain.modified'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/chaplain', 'static/chaplain.copy']
        ]),
        'stderr': '',
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/issue_9/ydg2DF', 'static/issue_9/A2VcHL'],
        'returncode': 0,
        'stdout': json.dumps([]),
        'stderr': '',
        'stdlog': None,
    },
    {
        'args': ['--json', 'static/empty', 'static/empty.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/empty', 'static/empty.copy']
        ]),
        'stderr': '',
        'stdlog': None,
    },
    {
        'setup': lambda: os.chmod('static/issue_37/kawabanga', 0000),
        'teardown': lambda: os.chmod('static/issue_37/kawabanga', 0644),
        'description': 'should complain if permission denied',
        'args': ['--json', 'static/issue_37'],
        'returncode': 1,
        'stdout': json.dumps([
            ['static/issue_37/kawabanga.copy', 'static/issue_37/kawabanga.copy2']
        ]),
        'stdlog': [('fdedup', 'ERROR', '[Errno 13] Permission denied: \'static/issue_37/kawabanga\'')],
    },
    {
        'description': 'should not duplicate duplicates if path is listed several times',
        'args': ['--json', 'static/empty', 'static/empty', 'static/empty', 'static/empty.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/empty', 'static/empty.copy']
        ]),
        'stderr': '',
        'stdlog': None
    },
    {
        'description': 'should work on normalized paths and understand redundant separators',
        'args': ['--json', 'static/empty', './static/empty', '././static/empty', './static/issue_37/../empty', './static/empty.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/empty', 'static/empty.copy']
        ]),
        'stderr': '',
        'stdlog': None
    },
    {
        'setup': lambda: os.link('static/issue_26/quote', 'static/issue_26/quote.hardlink'),
        'teardown': lambda: os.remove('static/issue_26/quote.hardlink'),
        'description': 'should treat hardlinks as separate files',
        'args': ['--json', 'static/issue_26'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/issue_26/quote', 'static/issue_26/quote.copy', 'static/issue_26/quote.hardlink']
        ]),
        'stderr': '',
        'stdlog': None,
    },
    {
        'description': 'should incorrectly report duplicates on md5 collision',
        'args': ['--hash', 'md5', '--json', 'static/issue_16'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/issue_16/hello', 'static/issue_16/erase']
        ]),
        'stderr': '',
        'stdlog': None,
    },
    {
        'description': 'should binary differentiate files with hash collision',
        'args': ['--verify', '--hash', 'md5', '--json', 'static/issue_16'],
        'returncode': 1,
        'stdout': json.dumps([]),
        'stdlog': [
            ('fdedup', 'ERROR', 'Hash collision detected: static/issue_16/hello, static/issue_16/erase')
        ],
    },
    {
        'description': 'should not affect true duplicates by verification',
        'args': ['--verify', '--json', 'static/chaplain', 'static/chaplain.copy'],
        'returncode': 0,
        'stdout': json.dumps([
            ['static/chaplain', 'static/chaplain.copy']
        ]),
        'stderr': '',
        'stdlog': None
    },
]
