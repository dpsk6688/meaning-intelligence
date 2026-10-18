@echo off
setlocal
python -c "from pathlib import Path; p = Path.home() / 'Desktop' / 'gh_token.txt'; b = p.read_bytes(); print('exists:', p.exists()); print('size:', len(b)); print('prefix:', b[:4].decode('ascii', 'replace')); print('has_newline:', b'\n' in b or b'\r' in b); print('has_bom:', b[:3] == b'\xef\xbb\xbf')"
if errorlevel 1 echo FAIL
endlocal