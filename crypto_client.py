import argparse
import rubikencryptor

parser = argparse.ArgumentParser()
parser.add_argument("--type", help="indicate whether to encrypt or decrypt image")
parser.add_argument("--image", help="indicate input image path")
parser.add_argument("--output_image", help="indicate output image path")
parser.add_argument("--Krfile", help="indicate kr file path(in case of decryption)")
parser.add_argument("--Kcfile", help="indicate kc file path(in case of encryption)")

args = parser.parse_args() 
type = args.type
image = args.image
output_image = args.output_image
Krfile = args.Krfile
Kcfile = args.Kcfile
# Validation checks
if type == None:
    print("ERROR: please supply --type")
    exit()

if type not in ("encrypt", "decrypt"):
    print("ERROR: --type should either be encrypt or decrypt")
    exit()

if image == None:
    print("ERROR: please supply --image")
    exit()

if output_image == None:
    output_image = 'output.png'

if type == "decrypt":
    if Krfile == None or Kcfile == None:
        print("ERROR: please supply --Krfile and --Kcfile")
        exit()


input_image = args.image
if args.type == "encrypt":		
    encryptor = rubikencryptor.RubikCubeEncryptor(input_image)
    encryptor.encrypt(iter_max=10)
else:
    Krfile = args.Krfile
    Kcfile = args.Kcfile
    decryptor = rubikencryptor.RubikCubeEncryptor(input_image)
    decryptor.decrypt(Krfile,Kcfile,10)
