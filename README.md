# Compress-GoPro

A Python command-line tool that uses FFmpeg to compress 4K GoPro videos for
YouTube.

## Requirements

- Python 3
- FFmpeg available on the system `PATH`

Check that FFmpeg is installed:

```bash
ffmpeg -version
```

## Usage

### Compress one video

```bash
python3 compress_gopro.py input.mp4
```

By default, the compressed video is saved next to the source with a
`compressed_` prefix. For example, `input.mp4` becomes
`compressed_input.mp4`.

Specify an output file with `-o` or `--output`:

```bash
python3 compress_gopro.py input.mp4 -o output.mp4
```

### Compress all MP4 files in a folder

```bash
python3 compress_gopro.py /path/to/videos
```

By default, the script searches the folder's top level for `.mp4` and `.MP4`
files and saves them to a `compressed_output` subdirectory.

Specify a custom output directory:

```bash
python3 compress_gopro.py /path/to/videos -o /path/to/output
```

The script does not currently process subfolders recursively.

## Options

```text
usage: compress_gopro.py [-h] [-o OUTPUT] [--crf CRF] input

positional arguments:
  input                 Path to a single .mp4 file or a folder containing videos.

options:
  -h, --help            Show this help message and exit.
  -o, --output OUTPUT   Optional output file or directory.
  --crf CRF             Quality CRF value (default: 22). Lower values improve
                        quality but produce larger files.
```

Example with a custom CRF:

```bash
python3 compress_gopro.py input.mp4 --crf 20
```
