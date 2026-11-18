import argparse
import subprocess
import sys
from pathlib import Path

def compress_video(input_path: Path, output_path: Path, crf: int) -> bool:
    """Runs FFmpeg on a single video file."""
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-crf", str(crf),
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path)
    ]

    print(f"\n[Processing] {input_path.name} -> {output_path.name}")
    try:
        subprocess.run(cmd, check=True)
        original_size = input_path.stat().st_size / (1024 * 1024)
        new_size = output_path.stat().st_size / (1024 * 1024)
        reduction = ((original_size - new_size) / original_size) * 100
        print(f"[Success] {original_size:.1f} MB -> {new_size:.1f} MB (Reduced by {reduction:.1f}%)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to compress {input_path.name} (exit code {e.returncode})", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Compress GoPro 4K videos for YouTube (supports individual files or folders).")
    parser.add_argument("input", type=str, help="Path to a single .mp4 file OR a folder containing videos.")
    parser.add_argument("-o", "--output", type=str, default=None, help="Optional output path (file or directory). Defaults to auto-generated names.")
    parser.add_argument("--crf", type=int, default=22, help="Quality CRF value (default: 22. Lower = better quality/larger file).")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: Path '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Scenario 1: Input is a single file
    if input_path.is_file():
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_name(f"compressed_{input_path.name}")

        compress_video(input_path, output_path, args.crf)

    # Scenario 2: Input is a directory/folder
    elif input_path.is_dir():
        if args.output:
            out_dir = Path(args.output)
        else:
            out_dir = input_path / "compressed_output"

        out_dir.mkdir(parents=True, exist_ok=True)

        # Find all MP4 files (case-insensitive search for .mp4/.MP4)
        video_files = sorted(list(input_path.glob("*.MP4")) + list(input_path.glob("*.mp4")))

        # Exclude files already residing inside the output folder to avoid loops
        video_files = [f for f in video_files if out_dir not in f.parents and f.parent != out_dir]

        if not video_files:
            print(f"No .mp4 files found in directory: {input_path}")
            return

        print(f"Found {len(video_files)} video(s) to process in folder: {input_path}")
        for video in video_files:
            output_path = out_dir / f"compressed_{video.name}"
            compress_video(video, output_path, args.crf)

        print(f"\nBatch processing complete! All files saved to: {out_dir}")

if __name__ == "__main__":
    main()