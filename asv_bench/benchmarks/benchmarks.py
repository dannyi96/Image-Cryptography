import os
from PIL import Image
from rubikencryptor.rubikencryptor import RubikCubeCrypto

class BenchRubikEncryptCrypto:
    params = [(1, 10), (1, 10)]

    def setup(self, alpha, iter_max):
        # Create a solid green image
        width, height = 300, 200
        green_color = (0, 255, 0)
        self.image = Image.new("RGB", (width, height), green_color)
        self.alpha = alpha
        self.iter_max = iter_max
        self.key_filename = "test_key.txt"
        self.output_image_name = "crypt_image.png"


    def time_rubik_crypto(self, alpha, iter_max):
        self.rubik_crypto = RubikCubeCrypto(self.image)
        result = self.rubik_crypto.encrypt(alpha, iter_max, self.key_filename)
        result.save(self.output_image_name)


    def teardown(self, alpha, iter_max):
        # Clean up generated files
        os.remove(self.key_filename)
        os.remove(self.output_image_name)
