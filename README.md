# Prey DDS Converter

Python script to let the user quickly reformat DDS files from the game Prey (2017) into standard DDS files for use in all programs capable of opening DDS files.

Most DDS files in Prey are split into several files with different quality levels and headers for each, making other software incapable of simply opening these DDS files. This script ammends the needed headers to the largest available quality level of specified files, making them able to be used as any normal DDS file is.

Method originally devised by HeliosAI and not a russian spy on the XeNTaX forums.

## Usage
- if not yet done: unpack game files, for example with [Evil Extractor](https://github.com/evilvasile/EvilExtractor) and the [pak decryption tool](https://sirkane.io/PreyConvert_003.7z) (direct link to .7z file, no guarantee for contents)
- open the file with Python 3.0+
- specify input directory where unconverted DDS files are located
- specify output directory (outside the input directory)
- specify whether you want DDS files that are already normal DDS files to be copied over to your output directory too. This includes things like keypad graphics which only have one quality level.
- if files with the same name are already found in the output directory, specify whether you want them to be overwritten or not
