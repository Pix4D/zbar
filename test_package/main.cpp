#include <stdio.h>
#include <stdlib.h>
#ifdef _WIN32
#include <fcntl.h>
#include <io.h>
#endif

#include <zbar/zbar.h>

#include <fstream>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

namespace
{
    std::unique_ptr<uint8_t[]> readBinary(const char* filename, uint64_t& rows, uint64_t& cols)
    {
        std::ifstream in(filename, std::ios::in | std::ios::binary);
        in.read(reinterpret_cast<char*>(&rows), sizeof(uint64_t));
        in.read(reinterpret_cast<char*>(&cols), sizeof(uint64_t));

        std::unique_ptr<uint8_t[]> matrixBuffer{ new uint8_t[rows * cols] };
        in.read(reinterpret_cast<char*>(&matrixBuffer[0]), rows * cols * sizeof(uint8_t));
        return matrixBuffer;
    }
}  // namespace

int main(int ac, char** av)
{
    using namespace zbar;
    const std::vector<std::string> imagePaths(av + 1, av + ac);

    auto processor = std::unique_ptr<zbar_processor_t, decltype(&zbar_processor_destroy)>(zbar_processor_create(0),
                                                                                          zbar_processor_destroy);
    if (zbar_processor_init(processor.get(), NULL, 0))
    {
        std::cout << "Could not init processor " << std::endl;
    }

    for (const auto& path : imagePaths)
    {
        std::cout << "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" << std::endl;
        std::cout << "Detecting QR code in image " << path << std::endl;

        uint64_t rows = 0, cols = 0;
        auto myMatrix = readBinary(path.c_str(), rows, cols);

        auto zimage =
            std::unique_ptr<zbar_image_t, decltype(&zbar_image_destroy)>(zbar_image_create(), zbar_image_destroy);
        zbar_image_set_size(zimage.get(), cols, rows);
        zbar_image_set_format(zimage.get(), zbar_fourcc('Y', '8', '0', '0'));

        zbar_image_set_data(zimage.get(), &myMatrix[0], cols * rows, NULL);
        std::cout << "Cols " << cols << " Rows " << rows << std::endl;

        zbar_process_image(processor.get(), zimage.get());

        const zbar_symbol_t* sym = zbar_image_first_symbol(zimage.get());
        for (; sym; sym = zbar_symbol_next(sym))
        {
            zbar_symbol_type_t typ = zbar_symbol_get_type(sym);
            if (typ == ZBAR_QRCODE)
            {
                const char* data = zbar_symbol_get_data(sym);
                std::cout << "QR code text: " << data << std::endl;
                return 0;
            }
        }
    }

    return 1;
}
