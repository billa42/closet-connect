#!/usr/bin/env python3

import subprocess
import logging
from pathlib import Path


def embed_text(img_file: str, img_outfile: str, text: str) -> int:
    tmp_filename = "closet.temp"

    with open(tmp_filename, "w") as tmp_file:
        tmp_file.write(text)

    tmp_path: Path = Path(tmp_filename)
    assert tmp_path.exists()

    exit_code: int = subprocess.run(
        ["zip", "-r", f"{tmp_filename}.zip", tmp_filename]).returncode

    if exit_code != 0:
        logging.error(f"Could not zip text file: {exit_code}")
        return exit_code

    zip_path: Path = Path(f"{tmp_filename}.zip")
    assert zip_path.exists()

    tmp_path.unlink()

    # TODO(billa42): Running with shell=True is a security issue.
    # The user can use well-chosen values of img_file and
    # img_outfile to create an exploit. Fix it.
    exit_code = subprocess.run(
        f"cat {img_file} {tmp_filename}.zip > {img_outfile}",
        shell=True).returncode

    if exit_code != 0:
        logging.error(f"Could not embed text into image: {exit_code}")
        return exit_code

    img_out_path: Path = Path(img_outfile)
    assert img_out_path.exists()

    zip_path.unlink()

    return 0


def extract_text(img_file: str) -> tuple[str, int]:
    tmp_filename = "closet.temp"

    input_img_path: Path = Path(img_file)
    assert input_img_path.exists()

    exit_code: int = subprocess.run(["cp", img_file,
                                     f"{tmp_filename}.img"]).returncode

    if exit_code != 0:
        logging.error(
            f"Could not move {img_file} to local folder: {exit_code}")
        return exit_code

    local_img_path: Path = Path(f"{tmp_filename}.img")
    assert local_img_path.exists()

    subprocess.run(["unzip", f"{tmp_filename}.img"]).returncode

    if exit_code != 0:
        logging.error(f"Could not unzip {img_file}: {exit_code}")
        return exit_code

    local_img_path.unlink()

    tmp_path: Path = Path(tmp_filename)
    assert tmp_path.exists()

    with open(tmp_filename, "r") as tmp_file:
        message: str = tmp_file.read()

    tmp_path.unlink()

    return (message, 0)
