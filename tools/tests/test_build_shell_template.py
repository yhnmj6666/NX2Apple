import importlib.util
import plistlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_shell_template', TOOLS / 'build_shell_template.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ShellTemplateDeploymentTest(unittest.TestCase):
    def build(self, ios18, built_minimum=None):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            engine = root / 'engine'
            ios = engine / 'dm' / 'ios'
            ios.mkdir(parents=True)
            (ios / 'project-shell.yml').write_text(
                'deploymentTarget:\n  iOS: "26.0"\nOTHER_CFLAGS: -mcpu=apple-a18\n',
                encoding='ascii')
            package = engine / 'frontend-ios'
            package.mkdir()
            (package / 'Package.swift').write_text('// fixture\n', encoding='ascii')
            generated = {}

            def run(command, **kwargs):
                cwd = kwargs.get('cwd')
                if command[0] == 'git':
                    return subprocess.CompletedProcess(command, 0, 'abc123\n', '')
                if command[0] == 'xcodegen':
                    generated['project'] = (cwd / 'project.yml').read_text(encoding='ascii')
                    (cwd / 'Gen' / 'Info.plist').write_bytes(plistlib.dumps({}))
                if command[0] == 'xcodebuild':
                    generated['command'] = command
                    dd = Path(command[command.index('-derivedDataPath') + 1])
                    app = dd / 'Build' / 'Products' / 'Release-iphoneos' / 'DmShell.app'
                    app.mkdir(parents=True)
                    (app / 'DmShell').write_bytes(b'executable fixture')
                    minimum = built_minimum or ('18.0' if ios18 else '26.0')
                    (app / 'Info.plist').write_bytes(plistlib.dumps({'MinimumOSVersion': minimum}))
                return subprocess.CompletedProcess(command, 0, '', '')

            with mock.patch.object(builder, '_chain_version', return_value='test-chain'), \
                    mock.patch.object(builder.os, 'symlink'), \
                    mock.patch.object(builder.subprocess, 'run', side_effect=run):
                out = builder.build_template(root / 'out' / 'DmShell.app', engine, ios18=ios18)
            self.assertTrue((out / 'DmShell').is_file())
            return generated

    def test_ios18_changes_project_target_cpu_and_build_override(self):
        generated = self.build(True)
        self.assertIn('iOS: "18.0"', generated['project'])
        self.assertIn('-mcpu=apple-a14', generated['project'])
        self.assertIn('IPHONEOS_DEPLOYMENT_TARGET=18.0', generated['command'])

    def test_default_preserves_metal4_shell_target(self):
        generated = self.build(False)
        self.assertIn('iOS: "26.0"', generated['project'])
        self.assertIn('-mcpu=apple-a18', generated['project'])
        self.assertNotIn('IPHONEOS_DEPLOYMENT_TARGET=18.0', generated['command'])

    def test_ios18_refuses_a_mislabeled_build(self):
        with self.assertRaisesRegex(SystemExit, 'did not produce an iOS 18 app'):
            self.build(True, built_minimum='26.0')
