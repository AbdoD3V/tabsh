#!/usr/bin/env python3
```python
#!/usr/bin/env python3
import re
import os
import json
import subprocess
import tempfile


def _python_replace(code, replacements):
    string_re = r'(""".*?"""|\'\'\'.*?\'\'\'|".*?(?<!\\)"|\'.*?(?<!\\)\')'
    parts = re.split(string_re, code, flags=re.DOTALL)

    for i in range(len(parts)):
        if i % 2 == 0:
            for key, val in sorted(replacements.items(), key=lambda x: -len(x[0])):
                pattern = re.escape(key)
                parts[i] = re.sub(pattern, val, parts[i])
    return ''.join(parts)


def replace_all_keywords(code, replacements):
    # Try C# keyword replacer if available (dotnet present and project exists or built dll exists).
    proj_dir = os.path.join(os.path.dirname(__file__), 'native', 'csharp')
    proj_file = os.path.join(proj_dir, 'keyword_replacer.csproj')
    tf_path = None
    try:
        # write mapping to temp file
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.json') as tf:
            json.dump(replacements, tf)
            tf_path = tf.name

        # prefer running built dll if present
        candidate_dll = os.path.join(proj_dir, 'bin', 'Release', 'net7.0', 'keyword_replacer.dll')
        if os.path.exists(candidate_dll):
            cmd = ['dotnet', candidate_dll, '--map', tf_path, '--cmd', code]
            p = subprocess.run(cmd, capture_output=True, text=True)
            if p.returncode == 0:
                return p.stdout

        # else, try `dotnet run --project native/csharp` if dotnet is available
        if os.path.exists(proj_file):
            cmd = ['dotnet', 'run', '--project', proj_dir, '--configuration', 'Release', '--', '--map', tf_path, '--cmd', code]
            p = subprocess.run(cmd, capture_output=True, text=True)
            if p.returncode == 0:
                return p.stdout

    except Exception:
        pass
    finally:
        try:
            if tf_path and os.path.exists(tf_path):
                os.unlink(tf_path)
        except Exception:
            pass

    # fallback to Python implementation
    return _python_replace(code, replacements)


def format_list(li: list):
    def strip_outer_quotes(s):
        if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
            return s[1:-1]
        return s

    return ' '.join(strip_outer_quotes(item) for item in li)

``` 
