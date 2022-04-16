import os
from image import Image
import argparse
from colors import Colors

if __name__ == "__main__":
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(
        description='Alışverişlio Resim Optimizasyon Aracı')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')
    parser.add_argument('-i', '--input', dest='input', action='store',
                        help='kaynak dosyalarının bulunduğu klasör')

    parser.add_argument('-o', '--output', required=False, default=f'{cwd}/outputs', action='store',
                        help='çıktı dosyalarının bulunacağı klasör')

    args = parser.parse_args()

    input_dir = args.input

    if input_dir is None:
        parser.print_help()

    if not os.path.exists(input_dir):
        print("Klasor bulunamadı")
        exit(1)

    max_allowed = 2000

    output_path = args.output

    isOutputExist = os.path.exists(output_path)

    if not isOutputExist:
        os.mkdir(output_path)

    for file in os.listdir(input_dir):
        try:
            image = Image(os.path.join(input_dir, file))
            image.delete_bg()
            output_file_path = os.path.join(output_path, file)
            image.save(output_file_path)
            print(f'{Colors.OKGREEN}basarılı : {file}{Colors.FAIL}')
        except:
            print(f"{Colors.FAIL}basarısız: {file}{Colors.ENDC}",)
