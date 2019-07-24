# CTF PNG Critical Chunk Size Fixer

This is a tool I created intended to be used in forensics challenges for CTFs where you are given a corrupted PNG file. After using a tool such as `pngcheck`, if there are critical chunks with incorrect sizes defined, then this tool will automatically go through each critical chunk and fix their sizes for you.

Note that this tool assumes that it is only the chunksizes that are incorrect. If the CRCs are incorrect as well, then you will have to manually go through the output file and calculate the CRCs yourself and replace them in the file.

## Getting Started

To use the tool, simply do the following:
```shell
git clone https://github.com/farazsth98/ctf-png-chunksize-fixer.git
cd ctf-png-chunksize-fixer
chmod +x ./png-chunksize-fixer.py
./png-chunksize-fixer -i input_file.png -o output_file.png
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details