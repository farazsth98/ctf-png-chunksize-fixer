# CTF PNG Critical Chunk Size Fixer

This is a tool I created intended to be used in forensics challenges for CTFs where you are given a corrupted PNG file. After using a tool such as `pngcheck`, if there are critical chunks with incorrect sizes defined, then this tool will automatically go through each critical chunk and fix their sizes automatically for you.

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