import torch
import io
import base64
from PIL import Image
import logging


from torchvision import datasets, transforms
from ts.torch_handler.base_handler import BaseHandler

from utils import run_style_transfer

logger = logging.getLogger(__name__)


class ModelHandler(BaseHandler):

    def handle(self, data, context):
        """
        Invoke by TorchServe for prediction request.
        Do pre-processing of data, prediction using model and postprocessing of prediction output
        :param data: Input data for prediction
        :param context: Initial context contains model server system properties.
        :return: prediction output
        """
        model_input = self.preprocess(data)
        model_output = self.inference(model_input)
        return self.postprocess(model_output)

    def initialize(self, context):
        """
        Initialize model. This will be called during model loading time
        :param context: Initial context contains model server system properties.
        :return:
        """
        super().initialize(context)

    def preprocess(self, data):
        """
        Preprocess function to convert the request input to a tensor(Torchserve supported format).
        Args :
            data (list): List of the data from the request input.
        Returns:
            tensor: Returns the tensor data of the input
        """

        images = []
        for item in data[0]:
            logging.info(item)
            image = data[0][item]

            if isinstance(image, str):
                # if the image is a string of bytesarray.
                image = base64.b64decode(image)
            if isinstance(image, (bytearray, bytes)):
                image = Image.open(io.BytesIO(image))

            data_transform = transforms.Compose([
                transforms.Resize(size=(128, 128)),
                transforms.ToTensor()])

            transformed_data = data_transform(image)
            images.append(transformed_data)

        return torch.stack(images).to(self.device)

    def inference(self, data):
        content_img, style_img = data.split(1, dim=0)
        input_img = content_img.clone()

        cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406])
        cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225])
        out_image = run_style_transfer(self.model.features, cnn_normalization_mean, cnn_normalization_std,
                                       content_img, style_img, input_img)
        return out_image

    def postprocess(self, data):
        transform = transforms.ToPILImage()
        image = transform(data.squeeze(dim=0))

        imb = io.BytesIO()
        image.save(imb, format='PNG')

        return [imb.getvalue()]

