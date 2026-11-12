# Installing on Windows

These instructions assume Windows with Python 3.10+ (3.13 is fine) and git
already installed. Run all commands in PowerShell.

We use [pipx](https://pipx.pypa.io/), which installs a Python command-line
tool into its own isolated environment and puts the command on your PATH.

## 1. Check prerequisites

The Windows Python launcher is `py`, which is more reliable than `python`.

```powershell
py --version
git --version
```

## 2. Install pipx

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

Close PowerShell and open a new window. PATH changes only apply to new
sessions.

## 3. Clone and install

Use the HTTPS URL, since SSH keys are probably not set up on this machine. If
the repo is private, git will prompt you to sign in through the browser (Git
for Windows includes Git Credential Manager).

```powershell
git clone https://github.com/uchicago-library/syllabus-to-metadata.git
pipx install .\syllabus-to-metadata
```

Check that it worked:

```powershell
syllabus-metadata --help
```

## 4. Configure the OpenAI API key

The tool reads the key from a dotenv-style file at `~/.openai`, which on
Windows is `C:\Users\<name>\.openai`. Create it with:

```powershell
Set-Content "$HOME\.openai" 'OPENAI_API_KEY=sk-...'
```

If you use Notepad instead, make sure it doesn't save the file as
`.openai.txt`.

## 5. Run it

The first argument is a prompt file; a sample is included in the repo at
`prompts\citations.txt`.

```powershell
syllabus-metadata .\syllabus-to-metadata\prompts\citations.txt C:\path\to\syllabus.pdf --backend openai
```

## Updating

After a `git pull` in the cloned repo:

```powershell
pipx install --force .\syllabus-to-metadata
```

## Alternative: virtual environment

This skips the PATH setup, but the command is only available while the
environment is activated.

```powershell
cd syllabus-to-metadata
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install .
```

If activation is blocked by the execution policy, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

pipx does not need this.
