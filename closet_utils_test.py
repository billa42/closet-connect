#!/usr/bin/env python3

import unittest
import closet_utils as utils
from pathlib import Path


class TestClosetUtilsMethods(unittest.TestCase):
    def test_embed_text(self):
        self.assertEqual(
            utils.embed_text("share/test_image.png", "out_image.png",
                             "TEST_TEXT"), 0,
            "Embed text exited with non zero error")

        zip_path: Path = Path('closet.temp.zip')
        self.assertTrue(zip_path.exists())
        zip_path.unlink()

        out_img_path: Path = Path('out_image.png')
        self.assertTrue(out_img_path.exists())
        out_img_path.unlink()

    def test_extract_text(self):
        message, exit_code = utils.extract_text(
            "share/test_embedded_image.png")

        self.assertEqual(exit_code, 0,
                         "Extract text exited with non zero error")

        self.assertEqual(message, "TEST_TEXT",
                         f"Incorrect extracted text: {message}")

    def test_end_to_end(self):
        self.assertEqual(
            utils.embed_text("share/test_image.png", "out_image.png",
                             "TEST_TEXT"), 0,
            "Embed text exited with non zero error")

        zip_path: Path = Path('closet.temp.zip')
        self.assertTrue(zip_path.exists())
        zip_path.unlink()

        message, exit_code = utils.extract_text("out_image.png")

        self.assertEqual(exit_code, 0,
                         "Extract text exited with non zero error")

        self.assertEqual(message, "TEST_TEXT",
                         f"Incorrect extracted text: {message}")

        out_img_path: Path = Path('out_image.png')
        self.assertTrue(out_img_path.exists())
        out_img_path.unlink()
