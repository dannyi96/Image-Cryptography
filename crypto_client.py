import argparse
from rubikencryptor.rubikencryptor import RubikCubeCrypto
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="<encrypt/decrypt>")
parser.add_argument("--image", type=str, help="input image name")
parser.add_argument("--alpha", type=int, help="alpha value(in case of encryption)")
parser.add_argument("--iter_max", type=int, help="max iterations value(in case of encryption)")
parser.add_argument("--key", type=str, help="key file name(to store key in case of encryption/ to use in case of decryption)")
parser.add_argument("--output_image", type=str, help="output image name")

args = parser.parse_args() 

# Validation checks
if args.type == None:
    print("ERROR: supply --type")
    exit()

if args.type not in ("encrypt", "decrypt"):
    print("ERROR: --type should either be encrypt or decrypt")
    exit()

if args.image == None or args.output_image == None or args.key == None:
    print("ERROR: supply --image, --output_image & --key")
    exit()

if args.type == "encrypt":
    if args.alpha == None or args.iter_max == None:
        print("ERROR: please supply --alpha and --iter_max")
        exit()

input_image = Image.open(args.image)
rubixCrypto = RubikCubeCrypto(input_image)

if args.type == "encrypt":
    encrypted_image = rubixCrypto.encrypt(alpha=args.alpha, iter_max=args.iter_max, key_filename=args.key)
    encrypted_image.save(args.output_image)
else:
    decrypted_image = rubixCrypto.decrypt(key_filename=args.key)
    decrypted_image.save(args.output_image)
